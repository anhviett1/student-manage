from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Semester
from .serializers import SemesterSerializer
from ..app_home.permissions import SemesterPermission
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=["Semesters"])
class SemesterViewSet(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    permission_classes = [SemesterPermission]
    lookup_field = "semester_id"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Semester.objects.none()

        query = self.request.query_params
        filters = Q()

        # Lấy các filter
        search_term = query.get("search", "")
        status_filter = query.get("status", "")
        academic_year_filter = query.get("academic_year", "")
        start_date = query.get("start_date")
        end_date = query.get("end_date")

        if status_filter:
            status_list = status_filter.split(",")
            filters &= Q(status__in=status_list)
        else:
            filters &= Q(status__in=["upcoming", "current"])

        if search_term:
            filters &= (
                Q(semester_name__icontains=search_term)
                | Q(academic_year__icontains=search_term)
                | Q(description__icontains=search_term)
                | Q(notes__icontains=search_term)
            )

        if academic_year_filter:
            academic_year_list = academic_year_filter.split(",")
            filters &= Q(academic_year__in=academic_year_list)

        if start_date and end_date:
            filters &= Q(start_date__gte=start_date) & Q(end_date__lte=end_date)

        return Semester.objects.filter(filters).distinct().order_by("-start_date")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_semester(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_semester(instance)
        return instance

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])

    def _validate_semester(self, instance):
        """Kiểm tra logic ngày tháng hợp lệ."""
        if instance.start_date > instance.end_date:
            raise ValueError("Ngày bắt đầu không thể lớn hơn ngày kết thúc.")
        if instance.registration_start > instance.registration_end:
            raise ValueError("Ngày bắt đầu đăng ký không thể lớn hơn ngày kết thúc đăng ký.")
        if instance.add_drop_deadline < instance.registration_start:
            raise ValueError("Hạn chót thêm/xóa môn không thể trước ngày bắt đầu đăng ký.")
        if instance.tuition_deadline < instance.start_date:
            raise ValueError("Hạn nộp học phí không thể trước ngày bắt đầu học kỳ.")
        if instance.late_fee_start < instance.tuition_deadline:
            raise ValueError("Ngày bắt đầu tính phí trễ không thể trước hạn nộp học phí.")

    @extend_schema(
        summary="Export semesters to Excel",
        responses={200: None},
    )
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        try:
            queryset = self.get_queryset()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Semesters"

            headers = [
                "Mã học kỳ",
                "Tên học kỳ",
                "Năm học",
                "Ngày bắt đầu",
                "Ngày kết thúc",
                "Ngày bắt đầu đăng ký",
                "Ngày kết thúc đăng ký",
                "Hạn thêm/xóa môn",
                "Hạn nộp học phí",
                "Ngày tính phí trễ",
                "Phí trễ hạn",
                "Tổng tín chỉ",
                "Tín chỉ tối thiểu",
                "Tín chỉ tối đa",
                "Trạng thái",
                "Mô tả",
                "Ghi chú",
                "Hoạt động",
                "Ngày tạo",
                "Ngày cập nhật",
            ]
            sheet.append(headers)

            for semester in queryset:
                sheet.append(
                    [
                        semester.semester_id,
                        semester.semester_name,
                        semester.academic_year,
                        semester.start_date,
                        semester.end_date,
                        semester.registration_start,
                        semester.registration_end,
                        semester.add_drop_deadline,
                        semester.tuition_deadline,
                        semester.late_fee_start,
                        str(semester.late_fee_amount),
                        semester.total_credits,
                        semester.min_credits,
                        semester.max_credits,
                        semester.get_status_display(),
                        semester.description or "",
                        semester.notes or "",
                        "Có" if semester.is_active else "Không",
                        semester.created_at,
                        semester.updated_at,
                    ]
                )

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="semesters_{timezone.now().strftime("%Y%m%d")}.xlsx"'
            )
            workbook.save(response)
            return response
        except Exception as e:
            logger.error(f"Error exporting semesters: {str(e)}")
            return Response(
                {"detail": "Không thể xuất danh sách học kỳ."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
