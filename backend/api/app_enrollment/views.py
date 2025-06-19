from rest_framework import viewsets
from django.db.models import Q
from .models import Enrollment
from .serializers import EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Enrollments"])
class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Enrollment.objects.none()  # Empty default queryset

        if self.request.user.is_authenticated:
            # Base filter without any condition
            filters = Q()

            # Get request parameters for filtering
            search_term = self.request.query_params.get("searchTerm", "")
            status_filter = self.request.query_params.get("status", "")
            student_filter = self.request.query_params.get("student", "")
            subject_filter = self.request.query_params.get("subject", "")
            semester_filter = self.request.query_params.get("semester", "")
            class_filter = self.request.query_params.get("class", "")
            start_date = self.request.query_params.get("startDate")
            end_date = self.request.query_params.get("endDate")

            # Split comma-separated values into lists (if applicable)
            status_list = status_filter.split(",") if status_filter else ["pending", "approved"]
            student_list = [int(id) for id in student_filter.split(",") if id.isdigit()]
            subject_list = subject_filter.split(",") if subject_filter else []
            semester_list = semester_filter.split(",") if semester_filter else []
            class_list = [int(id) for id in class_filter.split(",") if id.isdigit()]

            # Apply filters using Q objects
            filters &= Q(status__in=status_list)

            if search_term:
                filters &= (
                    Q(notes__icontains=search_term)
                    | Q(student__name__icontains=search_term)
                    | Q(subject__name__icontains=search_term)
                    | Q(semester__name__icontains=search_term)
                    | Q(class_obj__name__icontains=search_term)
                )

            if start_date and end_date:
                filters &= Q(enrollment_date__range=[start_date, end_date])

            if student_list:
                filters &= Q(student__id__in=student_list)

            if subject_list:
                filters &= Q(subject__subject_id__in=subject_list)

            if semester_list:
                filters &= Q(semester__semester_id__in=semester_list)

            if class_list:
                filters &= Q(class_obj__id__in=class_list)

            # Return the filtered queryset
            queryset = Enrollment.objects.filter(filters).distinct().order_by("-created_at")

        return queryset
