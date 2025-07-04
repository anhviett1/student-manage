from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Class
from .serializers import ClassSerializer
from ..app_home.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=["Classes"])
class ClassViewSet(viewsets.ModelViewSet):
    serializer_class = ClassSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "class_id"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Class.objects.none()

        query = self.request.query_params
        filters = Q()

        # Lấy các filter
        search_term = query.get("search", "")
        status_filter = query.get("status", "")
        semester_id = query.get("semester_id", "")
        department_id = query.get("department_id", "")
        subject_id = query.get("subject_id", "")
        teacher_id = query.get("teacher_id", "")

        if status_filter:
            status_list = status_filter.split(",")
            filters &= Q(status__in=status_list)
        else:
            filters &= Q(status__in=["active", "pending"])

        if search_term:
            filters &= (
                Q(class_id__icontains=search_term)
                | Q(class_name__icontains=search_term)
                | Q(description__icontains=search_term)
                | Q(subject__name__icontains=search_term)
                | Q(semester__semester_name__icontains=search_term)
                | Q(department__department_name__icontains=search_term)
                | Q(teacher__last_name__icontains=search_term)
                | Q(teacher__first_name__icontains=search_term)
            )

        if semester_id:
            filters &= Q(semester__semester_id=semester_id)

        if department_id:
            filters &= Q(department__department_id=department_id)

        if subject_id:
            filters &= Q(subject__subject_id=subject_id)

        if teacher_id:
            filters &= Q(teacher__teacher_id=teacher_id)

        return Class.objects.filter(filters).distinct().order_by("class_name")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_class(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_class(instance)
        return instance

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])

    def _validate_class(self, instance):
        """Kiểm tra logic hợp lệ."""
        if not instance.class_name:
            raise ValueError("Tên lớp không được để trống.")
        if not instance.semester or not instance.subject:
            raise ValueError("Học kỳ và môn học phải được cung cấp.")
        if instance.credits <= 0:
            raise ValueError("Số tín chỉ phải lớn hơn 0.")

    @extend_schema(
        #summary="Export classes to Excel",
        responses={200: None},
    )
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        try:
            queryset = self.get_queryset()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Classes"

            headers = [
                "Mã lớp", "Tên lớp", "Mô tả", "Khoa", "Số tín chỉ",
                "Trạng thái", "Học kỳ", "Môn học", "Giảng viên",
                "Hoạt động", "Ngày tạo", "Ngày cập nhật"
            ]
            sheet.append(headers)

            for class_obj in queryset:
                sheet.append([
                    class_obj.class_id,
                    class_obj.class_name,
                    class_obj.description or "",
                    class_obj.department.department_name if class_obj.department else "",
                    class_obj.credits,
                    class_obj.get_status_display(),
                    str(class_obj.semester),
                    str(class_obj.subject),
                    f"{class_obj.teacher.last_name} {class_obj.teacher.first_name}" if class_obj.teacher else "",
                    "Có" if class_obj.is_active else "Không",
                    class_obj.created_at,
                    class_obj.updated_at
                ])

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = f'attachment; filename="classes_{timezone.now().strftime("%Y%m%d")}.xlsx"'
            workbook.save(response)
            return response
        except Exception as e:
            logger.error(f"Error exporting classes: {str(e)}")
            return Response(
                {"detail": "Không thể xuất danh sách lớp học."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )