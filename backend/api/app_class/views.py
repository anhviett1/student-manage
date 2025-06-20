from rest_framework import viewsets
from django.db.models import Q
from .models import Class
from .serializers import ClassSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Classes"])
class ClassViewSet(viewsets.ModelViewSet):
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Class.objects.none()  # Empty default queryset

        if self.request.user.is_authenticated:
            # Base filter without any condition
            filters = Q()

            # Get request parameters for filtering
            search_term = self.request.query_params.get("searchTerm", "")
            status_filter = self.request.query_params.get("status", "")
            department_filter = self.request.query_params.get("department", "")
            semester_filter = self.request.query_params.get("semester", "")
            subject_filter = self.request.query_params.get("subject", "")
            teacher_filter = self.request.query_params.get("teacher", "")

            # Split comma-separated values into lists (if applicable)
            status_list = status_filter.split(",") if status_filter else ["active", "pending"]
            department_list = [int(id) for id in department_filter.split(",") if id.isdigit()]
            semester_list = semester_filter.split(",") if semester_filter else []
            subject_list = subject_filter.split(",") if subject_filter else []
            teacher_list = [int(id) for id in teacher_filter.split(",") if id.isdigit()]

            # Apply filters using Q objects
            filters &= Q(status__in=status_list)

            if search_term:
                filters &= (
                    Q(name__icontains=search_term)
                    | Q(description__icontains=search_term)
                    | Q(class_id__icontains=search_term)
                )

            if department_list:
                filters &= Q(department__id__in=department_list)

            if semester_list:
                filters &= Q(semester__semester_id__in=semester_list)

            if subject_list:
                filters &= Q(subject__subject_id__in=subject_list)

            if teacher_list:
                filters &= Q(teacher__id__in=teacher_list)

            # Return the filtered queryset
            queryset = Class.objects.filter(filters).distinct().order_by("name")

        return queryset
