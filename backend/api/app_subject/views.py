from rest_framework import viewsets
from django.db.models import Q
from .models import Subject
from .serializers import SubjectSerializer
from ..app_home.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Subjects"])
class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "subject_id"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Subject.objects.none()

        filters = self._build_filters()
        return Subject.objects.filter(filters).distinct().order_by("subject_name")

    def _build_filters(self):
        query = self.request.query_params
        filters = Q()

        # Params
        search_term = query.get("searchTerm", "")
        status_filter = query.get("status", "")
        department_filter = query.get("department", "")
        semester_filter = query.get("semester", "")

        # List
        status_list = status_filter.split(",") if status_filter else ["active", "pending"]
        department_list = [int(i) for i in department_filter.split(",") if i.isdigit()]
        semester_list = semester_filter.split(",") if semester_filter else []

        # Apply filters
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

        return filters

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_subject(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_subject(instance)
        return instance

    def _validate_subject(self, instance):
        """Đảm bảo mã môn học là duy nhất (code)."""
        if instance.code:
            qs = Subject.objects.filter(code=instance.code)
            if instance.pk:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise ValueError("Mã môn học phải là duy nhất.")