from rest_framework import viewsets
from django.db.models import Q
from .models import Semester
from .serializers import SemesterSerializer
from ..app_home.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Semesters"])
class SemesterViewSet(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Semester.objects.none()

        if self.request.user.is_authenticated:
            filters = Q()

            search_term = self.request.query_params.get("searchTerm", "")
            status_filter = self.request.query_params.get("status", "")
            academic_year_filter = self.request.query_params.get("academic_year", "")
            start_date = self.request.query_params.get("startDate")
            end_date = self.request.query_params.get("endDate")

            status_list = status_filter.split(",") if status_filter else ["upcoming", "current"]
            academic_year_list = academic_year_filter.split(",") if academic_year_filter else []

            filters &= Q(status__in=status_list)

            if search_term:
                filters &= (
                    Q(name__icontains=search_term)
                    | Q(academic_year__icontains=search_term)
                    | Q(description__icontains=search_term)
                    | Q(notes__icontains=search_term)
                )

            if start_date and end_date:
                filters &= Q(start_date__gte=start_date) & Q(end_date__lte=end_date)

            if academic_year_list:
                filters &= Q(academic_year__in=academic_year_list)

            queryset = Semester.objects.filter(filters).distinct().order_by("-start_date")

        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])
