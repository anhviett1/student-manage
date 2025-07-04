from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Activity
from .serializers import ActivitySerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
import logging

logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        tags=["Activities"],
        parameters=[
            OpenApiParameter(name="activity_type", type=str, description="Lọc theo loại hoạt động (login, logout, create, update, delete, view)"),
            OpenApiParameter(name="start_date", type=str, description="Lọc theo ngày bắt đầu (YYYY-MM-DD)"),
            OpenApiParameter(name="end_date", type=str, description="Lọc theo ngày kết thúc (YYYY-MM-DD)"),
            OpenApiParameter(name="search", type=str, description="Tìm kiếm theo mô tả hoặc tên người dùng"),
        ],
    ),
    retrieve=extend_schema(tags=["Activities"]),
)
class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all().order_by("-created_at")
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Activity.objects.none()

        query = self.request.query_params
        filters = Q()

        # Lọc theo quyền: admin/staff thấy tất cả, người dùng thường thấy của họ
        if not (user.is_staff or user.is_superuser):
            filters &= Q(user=user)

        # Lọc nâng cao
        activity_type = query.get("activity_type", "")
        start_date = query.get("start_date")
        end_date = query.get("end_date")
        search_term = query.get("search", "")

        if activity_type:
            activity_type_list = activity_type.split(",")
            filters &= Q(activity_type__in=activity_type_list)

        if start_date and end_date:
            filters &= Q(created_at__range=[start_date, end_date])

        if search_term:
            filters &= (
                Q(description__icontains=search_term)
                | Q(user__username__icontains=search_term)
                | Q(user__first_name__icontains=search_term)
                | Q(user__last_name__icontains=search_term)
            )

        return Activity.objects.filter(filters).order_by("-created_at")

    @extend_schema(
        summary="Xuất danh sách hoạt động",
        description="Xuất danh sách hoạt động dưới dạng file Excel.",
        responses={200: None},
        tags=["Activities"],
    )
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        try:
            queryset = self.get_queryset()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Activities"

            headers = [
                "ID", "Người dùng", "Loại hoạt động", "Mô tả",
                "IP Address", "Ngày tạo", "Ngày cập nhật"
            ]
            sheet.append(headers)

            for activity in queryset:
                sheet.append([
                    activity.id,
                    activity.user.username,
                    activity.get_activity_type_display(),
                    activity.description or "",
                    activity.ip_address or "",
                    activity.created_at,
                    activity.updated_at
                ])

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = f'attachment; filename="activities_{timezone.now().strftime("%Y%m%d")}.xlsx'
            workbook.save(response)
            logger.info("Exported activity list to Excel")
            return response
        except Exception as e:
            logger.error(f"Error exporting activities: {str(e)}")
            return Response(
                {"detail": "Không thể xuất danh sách hoạt động."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )