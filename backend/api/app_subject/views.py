from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Subject
from .serializers import SubjectSerializer
from ..app_home.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=["Subjects"])
class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "subject_id"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Subject.objects.none()

        query = self.request.query_params
        filters = Q()

        # Lấy các filter
        search_term = query.get("search", "")
        status_filter = query.get("status", "")
        semester_id = query.get("semester_id", "")
        department_id = query.get("department_id", "")

        if status_filter:
            status_list = status_filter.split(",")
            filters &= Q(status__in=status_list)
        else:
            filters &= Q(status__in=["active", "pending"])

        if search_term:
            filters &= (
                Q(subject_id__icontains=search_term)
                | Q(subject_name__icontains=search_term)
                | Q(description__icontains=search_term)
                | Q(department__department_name__icontains=search_term)
                | Q(semester__semester_name__icontains=search_term)
            )

        if semester_id:
            filters &= Q(semester__semester_id=semester_id)

        if department_id:
            filters &= Q(department__department_id=department_id)

        return Subject.objects.filter(filters).distinct().order_by("subject_name")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_subject(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_subject(instance)
        return instance

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])

    def _validate_subject(self, instance):
        """Kiểm tra logic hợp lệ."""
        if not instance.subject_name:
            raise ValueError("Tên môn học không được để trống.")
        if instance.credits <= 0:
            raise ValueError("Số tín chỉ phải lớn hơn 0.")

    @extend_schema(
        #summary="Export subjects to Excel",
        responses={200: None},
    )
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        try:
            queryset = self.get_queryset()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Subjects"

            headers = [
                "Mã môn học", "Tên môn học", "Mô tả", "Số tín chỉ",
                "Học kỳ", "Khoa", "Trạng thái", "Hoạt động",
                "Ngày tạo", "Ngày cập nhật"
            ]
            sheet.append(headers)

            for subject in queryset:
                sheet.append([
                    subject.subject_id,
                    subject.subject_name,
                    subject.description or "",
                    subject.credits,
                    str(subject.semester) if subject.semester else "",
                    subject.department.department_name if subject.department else "",
                    subject.get_status_display(),
                    "Có" if subject.is_active else "Không",
                    subject.created_at,
                    subject.updated_at
                ])

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = f'attachment; filename="subjects_{timezone.now().strftime("%Y%m%d")}.xlsx"'
            workbook.save(response)
            return response
        except Exception as e:
            logger.error(f"Error exporting subjects: {str(e)}")
            return Response(
                {"detail": "Không thể xuất danh sách môn học."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )