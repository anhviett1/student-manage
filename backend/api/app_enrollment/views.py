from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Enrollment
from .serializers import EnrollmentSerializer
from ..app_home.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=["Enrollments"])
class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "enrollment_id"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Enrollment.objects.none()

        query = self.request.query_params
        filters = Q()

        # Lấy các filter
        search_term = query.get("search", "")
        status_filter = query.get("status", "")
        academic_year_filter = query.get("academic_year", "")
        semester_id = query.get("semester_id", "")
        student_id = query.get("student_id", "")
        subject_id = query.get("subject_id", "")

        if status_filter:
            status_list = status_filter.split(",")
            filters &= Q(status__in=status_list)
        else:
            filters &= Q(status__in=["pending", "approved"])

        if search_term:
            filters &= (
                Q(enrollment_id__icontains=search_term)
                | Q(student__full_name__icontains=search_term)
                | Q(subject__name__icontains=search_term)
                | Q(semester__semester_name__icontains=search_term)
                | Q(academic_year__icontains=search_term)
                | Q(notes__icontains=search_term)
            )

        if academic_year_filter:
            academic_year_list = academic_year_filter.split(",")
            filters &= Q(academic_year__in=academic_year_list)

        if semester_id:
            filters &= Q(semester__semester_id=semester_id)

        if student_id:
            filters &= Q(student__student_id=student_id)

        if subject_id:
            filters &= Q(subject__subject_id=subject_id)

        return Enrollment.objects.filter(filters).distinct().order_by("-enrollment_date")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_enrollment(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_enrollment(instance)
        return instance

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])

    def _validate_enrollment(self, instance):
        """Kiểm tra logic đăng ký hợp lệ."""
        if not instance.student or not instance.subject or not instance.semester or not instance.class_obj:
            raise ValueError("Sinh viên, môn học, học kỳ và lớp học phải được cung cấp.")
        if instance.enrollment_date > instance.semester.end_date:
            raise ValueError("Ngày đăng ký không thể sau ngày kết thúc học kỳ.")
        if instance.enrollment_date < instance.semester.registration_start:
            raise ValueError("Ngày đăng ký không thể trước ngày bắt đầu đăng ký học kỳ.")

    @extend_schema(
        #summary="Export enrollments to Excel",
        responses={200: None},
    )
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        try:
            queryset = self.get_queryset()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Enrollments"

            headers = [
                "Mã đăng ký", "Sinh viên", "Môn học", "Học kỳ", "Lớp học",
                "Ngày đăng ký", "Năm học", "Trạng thái", "Ghi chú",
                "Hoạt động", "Ngày tạo", "Ngày cập nhật"
            ]
            sheet.append(headers)

            for enrollment in queryset:
                sheet.append([
                    enrollment.enrollment_id,
                    str(enrollment.student),
                    str(enrollment.subject),
                    str(enrollment.semester),
                    str(enrollment.class_obj),
                    enrollment.enrollment_date,
                    enrollment.academic_year,
                    enrollment.get_status_display(),
                    enrollment.notes or "",
                    "Có" if enrollment.is_active else "Không",
                    enrollment.created_at,
                    enrollment.updated_at
                ])

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = f'attachment; filename="enrollments_{timezone.now().strftime("%Y%m%d")}.xlsx"'
            workbook.save(response)
            return response
        except Exception as e:
            logger.error(f"Error exporting enrollments: {str(e)}")
            return Response(
                {"detail": "Không thể xuất danh sách đăng ký."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )