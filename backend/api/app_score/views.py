from rest_framework import viewsets
from django.db.models import Q
from .models import Score
from .serializers import ScoreSerializer
from ..app_home.permissions import IsAdminOrTeacher, IsOwnerOrAdmin
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Scores"])
class ScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    permission_classes = [IsAdminOrTeacher]

    def get_permissions(self):
        if self.action in ["retrieve"]:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Score.objects.none()

        if self.request.user.is_authenticated:
            filters = Q()

            search_term = self.request.query_params.get("searchTerm", "")
            status_filter = self.request.query_params.get("status", "")
            student_filter = self.request.query_params.get("student", "")
            subject_filter = self.request.query_params.get("subject", "")
            semester_filter = self.request.query_params.get("semester", "")

            status_list = status_filter.split(",") if status_filter else ["active", "pending"]
            student_list = [int(id) for id in student_filter.split(",") if id.isdigit()]
            subject_list = subject_filter.split(",") if subject_filter else []
            semester_list = semester_filter.split(",") if semester_filter else []

            filters &= Q(status__in=status_list)

            if search_term:
                filters &= (
                    Q(notes__icontains=search_term)
                    | Q(student__name__icontains=search_term)
                    | Q(subject__name__icontains=search_term)
                    | Q(semester__name__icontains=search_term)
                )

            if student_list:
                filters &= Q(student__id__in=student_list)

            if subject_list:
                filters &= Q(subject__subject_id__in=subject_list)

            if semester_list:
                filters &= Q(semester__semester_id__in=semester_list)

            queryset = Score.objects.filter(filters).distinct().order_by("-created_at")

        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])
        return instance
    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.midterm_score is not None and instance.final_score is not None:
            instance.total_score = (instance.midterm_score * 0.4) + (instance.final_score * 0.6)
            instance.save(update_fields=["total_score"])
        return instance
    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.midterm_score is not None and instance.final_score is not None:
            instance.total_score = (instance.midterm_score * 0.4) + (instance.final_score * 0.6)
            instance.save(update_fields=["total_score"])
        return instance

