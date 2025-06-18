from rest_framework import viewsets
from django.db.models import Q
from .models import Subject
from .serializers import SubjectSerializer
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Subjects"])
class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Subject.objects.none()

        if self.request.user.is_authenticated:
            filters = Q()

            search_term = self.request.query_params.get("searchTerm", "")
            status_filter = self.request.query_params.get("status", "")
            department_filter = self.request.query_params.get("department", "")
            semester_filter = self.request.query_params.get("semester", "")

            status_list = status_filter.split(",") if status_filter else ["active", "pending"]
            department_list = [int(id) for id in department_filter.split(",") if id.isdigit()]
            semester_list = semester_filter.split(",") if semester_filter else []

            filters &= Q(status__in=status_list)

            if search_term:
                filters &= (
                    Q(subject_id__icontains=search_term)
                    | Q(name__icontains=search_term)
                    | Q(description__icontains=search_term)
                )

            if department_list:
                filters &= Q(department__id__in=department_list)

            if semester_list:
                filters &= Q(semester__semester_id__in=semester_list)

            queryset = Subject.objects.filter(filters).distinct().order_by("name")

        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])
