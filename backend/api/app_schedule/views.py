from rest_framework import viewsets
from django.db.models import Q
from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Schedules"])
class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Schedule.objects.none()
        if self.request.user.is_authenticated:
            filters = Q()
            if self.request.user.is_student:
                filters &= Q(class_assigned__student_classes__user=self.request.user)
            elif self.request.user.is_teacher:
                filters &= Q(teacher=self.request.user)
            search_term = self.request.query_params.get('searchTerm', '')
            status_filter = self.request.query_params.get('status', '')
            semester_filter = self.request.query_params.get('semester', '')
            department_filter = self.request.query_params.get('department', '')
            status_list = status_filter.split(',') if status_filter else ['active']
            semester_list = semester_filter.split(',') if semester_filter else []
            department_list = [int(id) for id in department_filter.split(',') if id.isdigit()]
            filters &= Q(status__in=status_list)
            if search_term: filters &= (Q(class_assigned__name__icontains=search_term) | Q(room__icontains=search_term))
            if semester_list: filters &= Q(semester__semester_id__in=semester_list)
            if department_list: filters &= Q(department__id__in=department_list)
            queryset = Schedule.objects.filter(filters).distinct().order_by('day_of_week', 'start_time')
        return queryset
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=['is_deleted', 'is_active'])
