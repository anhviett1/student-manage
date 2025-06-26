from rest_framework import viewsets
from django.db.models import Q
from django.utils import timezone
from .models import Teacher
from .serializers import TeacherSerializer
from ..app_home.permissions import IsAdmin, IsAdminOrTeacher, IsOwnerOrAdmin
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Teachers"])
class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin]
    lookup_field = "teacher_id"

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminOrTeacher()]
        if self.action == "retrieve":
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Teacher.objects.none()
        if self.request.user.is_authenticated:
            filters = Q()
            search_term = self.request.query_params.get("searchTerm", "")
            status_filter = self.request.query_params.get("status", "")
            department_filter = self.request.query_params.get("department", "")
            degree_filter = self.request.query_params.get("degree", "")
            gender_filter = self.request.query_params.get("gender", "")
            
            status_list = status_filter.split(",") if status_filter else ["active"]
            department_list = [int(id) for id in department_filter.split(",") if id.isdigit()]
            degree_list = degree_filter.split(",") if degree_filter else []
            gender_list = gender_filter.split(",") if gender_filter else []
            
            filters &= Q(status__in=status_list)

            if search_term:
                filters &= (
                    Q(teacher_id__icontains=search_term) | 
                    Q(first_name__icontains=search_term) |                     
                    Q(last_name__icontains=search_term) |                   
                    Q(email__icontains=search_term) | 
                    Q(specialization__icontains=search_term)
                )

            if department_list:
                filters &= Q(department__id__in=department_list)

            if degree_list:
                filters &= Q(degree__in=degree_list)
            if gender_list:
                filters &= Q(gender__in=gender_list)
            queryset = (
                Teacher.objects.filter(filters).distinct().order_by("last_name", "first_name")
            )
        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])
    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.email and Teacher.objects.filter(email=instance.email).exclude(pk=instance.pk).exists():
            raise ValueError("Email must be unique.")
        return instance
    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.email and Teacher.objects.filter(email=instance.email).exists():
            raise ValueError("Email must be unique.")
        return instance
