from rest_framework import viewsets
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from .models import Semester
from .serializers import SemesterSerializer
from ..app_home.permissions import IsAdminOrReadOnly


@extend_schema(tags=["Semesters"])
class SemesterViewSet(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "semester_id"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Semester.objects.none()

        filters = self._build_filters()
        return Semester.objects.filter(filters).distinct().order_by("-start_date")

    def _build_filters(self):
        """Tạo bộ lọc từ query parameters."""
        query = self.request.query_params
        filters = Q()

        # Lấy các filter
        search_term = query.get("searchTerm", "")
        status_filter = query.get("status", "")
        academic_year_filter = query.get("academic_year", "")
        start_date = query.get("startDate")
        end_date = query.get("endDate")

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

        return filters

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_semester(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_semester(instance)
        return instance

    def _validate_semester(self, instance):
        """Kiểm tra logic ngày tháng hợp lệ."""
        if instance.start_date > instance.end_date:
            raise ValueError("Ngày bắt đầu không thể lớn hơn ngày kết thúc.")
        if instance.registration_start > instance.registration_end:
            raise ValueError("Ngày bắt đầu đăng ký không thể lớn hơn ngày kết thúc đăng ký.")
        if instance.add_drop_deadline < instance.registration_start:
            raise ValueError("Hạn chót thêm/xóa môn không thể trước ngày bắt đầu đăng ký.")
