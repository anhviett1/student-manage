from rest_framework import viewsets
from django.db.models import Q
from .models import User, Department
from .serializers import UserSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Users"])
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.none()

        if self.request.user.is_authenticated:
            filters = Q()

            search_term = self.request.query_params.get("searchTerm", "")
            role_filter = self.request.query_params.get("role", "")
            department_filter = self.request.query_params.get("department", "")
            status_filter = self.request.query_params.get("status", "")

            role_list = role_filter.split(",") if role_filter else []
            department_list = [int(id) for id in department_filter.split(",") if id.isdigit()]
            status_list = status_filter.split(",") if status_filter else ["active"]

            if status_list:
                filters &= Q(is_active__in=[s == "active" for s in status_list])

            if search_term:
                filters &= (
                    Q(username__icontains=search_term)
                    | Q(first_name__icontains=search_term)
                    | Q(last_name__icontains=search_term)
                    | Q(email__icontains=search_term)
                )

            if role_list:
                filters &= Q(role__in=role_list)

            if department_list:
                filters &= Q(department__id__in=department_list)

            queryset = User.objects.filter(filters).distinct().order_by("-created_at")

        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        if "last_login_ip" in self.request.data:
            instance.update_last_login_ip(self.request.data["last_login_ip"])

    def perform_destroy(self, instance):
        instance.soft_delete()


@extend_schema(tags=["Departments"])
class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

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
                    Q(name__icontains=search_term)
                    | Q(code__icontains=search_term)
                    | Q(description__icontains=search_term)
                )

            if head_list:
                filters &= Q(head__id__in=head_list)

            queryset = Department.objects.filter(filters).distinct().order_by("name")

        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])
