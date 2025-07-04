from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Schedule
from .serializers import ScheduleSerializer
from ..app_home.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=["Schedules"])
class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "schedule_id"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Schedule.objects.none()

        query = self.request.query_params
        filters = Q()

        # Lấy các filter
        search_term = query.get("search", "")
        status_filter = query.get("status", "")
        semester_id = query.get("semester_id", "")
        department_id = query.get("department_id", "")
        class_id = query.get("class_id", "")
        teacher_id = query.get("teacher_id", "")
        day_of_week = query.get("day_of_week", "")

        if status_filter:
            status_list = status_filter.split(",")
            filters &= Q(status__in=status_list)
        else:
            filters &= Q(status__in=["active", "pending"])

        if search_term:
            filters &= (
                Q(schedule_id__icontains=search_term)
                | Q(class_assigned__class_name__icontains=search_term)
                | Q(teacher__full_name__icontains=search_term)
                | Q(semester__semester_name__icontains=search_term)
                | Q(department__department_name__icontains=search_term)
                | Q(room__icontains=search_term)
            )

        if semester_id:
            filters &= Q(semester__semester_id=semester_id)

        if department_id:
            filters &= Q(department__department_id=department_id)

        if class_id:
            filters &= Q(class_assigned__class_id=class_id)

        if teacher_id:
            filters &= Q(teacher__id=teacher_id)

        if day_of_week:
            filters &= Q(day_of_week=day_of_week)

        return Schedule.objects.filter(filters).distinct().order_by("day_of_week", "start_time")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_schedule(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_schedule(instance)
        return instance

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])

    def _validate_schedule(self, instance):
        """Kiểm tra logic hợp lệ."""
        if not instance.class_assigned or not instance.semester:
            raise ValueError("Lớp học và học kỳ phải được cung cấp.")
        if instance.start_time >= instance.end_time:
            raise ValueError("Giờ bắt đầu phải nhỏ hơn giờ kết thúc.")
        if not instance.room:
            raise ValueError("Phòng học không được để trống.")

    @extend_schema(
        #summary="Export schedules to Excel",
        responses={200: None},
    )
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        try:
            queryset = self.get_queryset()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Schedules"

            headers = [
                "Mã lịch học", "Lớp học", "Giảng viên", "Học kỳ", "Khoa",
                "Ngày trong tuần", "Giờ bắt đầu", "Giờ kết thúc", "Phòng học",
                "Trạng thái", "Hoạt động", "Ngày tạo", "Ngày cập nhật"
            ]
            sheet.append(headers)

            for schedule in queryset:
                sheet.append([
                    schedule.schedule_id,
                    str(schedule.class_assigned),
                    str(schedule.teacher) if schedule.teacher else "",
                    str(schedule.semester),
                    schedule.department.department_name if schedule.department else "",
                    schedule.get_day_of_week_display(),
                    str(schedule.start_time),
                    str(schedule.end_time),
                    schedule.room,
                    schedule.get_status_display(),
                    "Có" if schedule.is_active else "Không",
                    schedule.created_at,
                    schedule.updated_at
                ])

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = f'attachment; filename="schedules_{timezone.now().strftime("%Y%m%d")}.xlsx"'
            workbook.save(response)
            return response
        except Exception as e:
            logger.error(f"Error exporting schedules: {str(e)}")
            return Response(
                {"detail": "Không thể xuất danh sách lịch học."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )