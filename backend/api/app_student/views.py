from rest_framework import viewsets
from django.db.models import Q
from django.utils import timezone
from .models import Student
from .serializers import StudentSerializer
from ..app_home.permissions import IsAdmin, IsAdminOrTeacher, IsOwnerOrAdmin
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Students"])
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminOrTeacher()]
        if self.action == "retrieve":
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Student.objects.none()

        if self.request.user.is_authenticated:
            filters = Q()

            search_term = self.request.query_params.get("searchTerm", "")
            status_filter = self.request.query_params.get("status", "")
            department_filter = self.request.query_params.get("department", "")
            class_filter = self.request.query_params.get("class_assigned", "")
            gender_filter = self.request.query_params.get("gender", "")
            start_date = self.request.query_params.get("startDate")
            end_date = self.request.query_params.get("endDate")

            status_list = status_filter.split(",") if status_filter else ["active"]
            department_list = [int(id) for id in department_filter.split(",") if id.isdigit()]
            class_list = [int(id) for id in class_filter.split(",") if id.isdigit()]
            gender_list = gender_filter.split(",") if gender_filter else []

            filters &= Q(status__in=status_list)

            if search_term:
                filters &= (
                    Q(student_id__icontains=search_term)
                    | Q(first_name__icontains=search_term)
                    | Q(last_name__icontains=search_term)
                    | Q(email__icontains=search_term)
                    | Q(major__icontains=search_term)
                )

            if start_date and end_date:
                filters &= Q(enrollment_date__range=[start_date, end_date])

            if department_list:
                filters &= Q(department__id__in=department_list)

            if class_list:
                filters &= Q(class_assigned__id__in=class_list)

            if gender_list:
                filters &= Q(gender__in=gender_list)

            queryset = Student.objects.filter(filters).distinct().order_by("student_id")

        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.calculate_gpa()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.calculate_gpa()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["is_deleted", "is_active", "deleted_at"])
    def calculate_gpa(self):
        if not self.scores.exists():
            return 0.00
        total_points = 0
        total_credits = 0
        for score in self.scores.all():
            if score.grade_point and score.subject.credits:
                total_points += score.grade_point * score.subject.credits
                total_credits += score.subject.credits
        if total_credits > 0:
            self.gpa = round(total_points / total_credits, 2)
            self.save(update_fields=["gpa"])
        return self.gpa
