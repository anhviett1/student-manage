from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Department
from .serializers import DepartmentSerializer
from ..app_home.permissions import DepartmentPermission
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=["Departments"])
class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [DepartmentPermission]
    lookup_field = "department_id"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Department.objects.none()

        query = self.request.query_params
        filters = Q()

        # Lấy các filter
        search_term = query.get("search", "")
        is_active_filter = query.get("is_active", "")

        if is_active_filter:
            is_active = is_active_filter.lower() == "true"
            filters &= Q(is_active=is_active)
        else:
            filters &= Q(is_active=True)

        if search_term:
            filters &= (
                Q(department_name__icontains=search_term)
                | Q(description__icontains=search_term)
                | Q(head__full_name__icontains=search_term)
            )

        return Department.objects.filter(filters).distinct().order_by("department_name")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_department(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_department(instance)
        return instance

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])

    def _validate_department(self, instance):
        """Kiểm tra logic hợp lệ."""
        if not instance.department_name:
            raise ValueError("Tên khoa không được để trống.")

    @extend_schema(
        summary="Export departments to Excel",
        responses={200: None},
    )
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        try:
            queryset = self.get_queryset()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Departments"

            headers = [
                "ID khoa",
                "Tên khoa",
                "Mô tả",
                "Trưởng khoa",
                "Hoạt động",
                "Ngày tạo",
                "Ngày cập nhật",
            ]
            sheet.append(headers)

            for department in queryset:
                sheet.append(
                    [
                        department.department_id,
                        department.department_name,
                        department.description or "",
                        str(department.head) if department.head else "",
                        "Có" if department.is_active else "Không",
                        department.created_at,
                        department.updated_at,
                    ]
                )

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="departments_{timezone.now().strftime("%Y%m%d")}.xlsx"'
            )
            workbook.save(response)
            return response
        except Exception as e:
            logger.error(f"Error exporting departments: {str(e)}")
            return Response(
                {"detail": "Không thể xuất danh sách khoa."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
