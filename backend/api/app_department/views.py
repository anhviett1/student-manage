from rest_framework import viewsets
from django.db.models import Q
from .models import Department
from .serializers import DepartmentSerializer
from ..app_home.permissions import IsAdmin, IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import csv
from django.http import HttpResponse

@extend_schema(tags=["Departments"])
class DepartmentViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = DepartmentSerializer
    lookup_field = "department_id"
    
    def get_queryset(self):
        queryset = Department.objects.none()

        if self.request.user.is_authenticated:
            filters = Q()

            search_term = self.request.query_params.get("searchTerm", "")
            status_filter = self.request.query_params.get("status", "")
            head_filter = self.request.query_params.get("head", "")

            status_list = status_filter.split(",") if status_filter else ["active"]
            head_list = [int(id) for id in head_filter.split(",") if id.isdigit()]

            if status_list:
                filters &= Q(is_active__in=[s == "active" for s in status_list])

            if search_term:
                filters &= (
                    Q(department_name__icontains=search_term)
                    | Q(code__icontains=search_term)
                    | Q(description__icontains=search_term)
                )

            if head_list:
                filters &= Q(head__id__in=head_list)

            queryset = Department.objects.filter(filters).distinct().order_by("department_name")

        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])
        return instance
    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.head and not instance.head.is_active:
            raise ValueError("Trưởng khoa phải là người dùng đang hoạt động.")
        if instance.code and Department.objects.filter(code=instance.code).exclude(pk=instance.pk).exists():
            raise ValueError("Mã khoa phải là duy nhất.")
        return instance
    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.head and not instance.head.is_active:
            raise ValueError("Trưởng khoa phải là người dùng đang hoạt động.")
        if instance.code and Department.objects.filter(code=instance.code).exists():
            raise ValueError("Mã khoa phải là duy nhất.")
        return instance

@extend_schema(tags=["Departments"]) 
class DepartmentExportAPIView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = DepartmentSerializer
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="departments.csv"'

        writer = csv.writer(response)

        # Write header row
        writer.writerow([
            'department_id', 'department_name', 'code', 'description', 
            'is_active', 'created_at', 'updated_at', 'is_deleted', 'head_id', 'head_username'
        ])

        # Write data rows
        departments = Department.objects.filter(is_deleted=False).order_by('department_name')
        for department in departments:
            writer.writerow([
                department.department_id,
                department.department_name,
                department.code,
                department.description,
                department.is_active,
                department.created_at.isoformat() if department.created_at else '',
                department.updated_at.isoformat() if department.updated_at else '',
                department.is_deleted,
                department.head.id if department.head else '',
                department.head.username if department.head else ''
            ])
        return response


    



    