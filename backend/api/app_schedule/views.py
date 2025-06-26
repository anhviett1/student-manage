from rest_framework import viewsets
from django.db.models import Q
from .models import Schedule
from .serializers import ScheduleSerializer
from ..app_home.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Schedules"])
class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "schedule_id"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Schedule.objects.none()

        filters = self._build_filters(user)
        return Schedule.objects.filter(filters).distinct().order_by('day_of_week', 'start_time')

    def _build_filters(self, user):
        """Tạo bộ lọc tùy theo role và query params."""
        filters = Q()

        # Filter theo role
        if user.is_student:
            filters &= Q(class_assigned__student_classes__user=user)
        elif user.is_teacher:
            filters &= Q(teacher=user)

        # Lọc theo query param
        query_params = self.request.query_params
        search_term = query_params.get('searchTerm', '')
        status_filter = query_params.get('status', '')
        semester_filter = query_params.get('semester', '')
        department_filter = query_params.get('department', '')

        status_list = status_filter.split(',') if status_filter else ['active']
        semester_list = semester_filter.split(',') if semester_filter else []
        department_list = [int(d) for d in department_filter.split(',') if d.isdigit()]

        filters &= Q(status__in=status_list)
        if search_term:
            filters &= Q(class_assigned__name__icontains=search_term) | Q(room__icontains=search_term)
        if semester_list:
            filters &= Q(semester__semester_id__in=semester_list)
        if department_list:
            filters &= Q(department__id__in=department_list)

        return filters

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=['is_deleted', 'is_active'])

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_schedule(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_schedule(instance)
        return instance

    def _validate_schedule(self, instance):
        """Kiểm tra tính hợp lệ của lịch học."""
        if instance.start_time >= instance.end_time:
            raise ValueError("Thời gian bắt đầu không thể lớn hơn hoặc bằng thời gian kết thúc.")
        if instance.day_of_week not in range(0, 7):
            raise ValueError("Ngày trong tuần phải nằm trong khoảng từ 0 (Chủ nhật) đến 6 (Thứ bảy).")