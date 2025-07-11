from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Score
from .serializers import ScoreSerializer
from ..app_home.permissions import ScorePermission
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=["Scores"])
class ScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    permission_classes = [ScorePermission]
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Score.objects.none()

        query = self.request.query_params
        filters = Q()

        # Lọc theo quyền: admin thấy tất cả, giáo viên thấy điểm của môn họ dạy, học sinh thấy điểm của họ
        if not (user.is_superuser or getattr(user, "role", "") == "admin"):
            if getattr(user, "role", "") == "teacher":
                filters &= Q(subject__teacher=user)
            elif getattr(user, "role", "") == "student":
                filters &= Q(student=user)

        # Lấy các filter
        search_term = query.get("search", "")
        status_filter = query.get("status", "")
        semester_id = query.get("semester_id", "")
        student_id = query.get("student_id", "")
        subject_id = query.get("subject_id", "")

        if status_filter:
            status_list = status_filter.split(",")
            filters &= Q(status__in=status_list)
        else:
            filters &= Q(status__in=["active", "pending"])

        if search_term:
            filters &= (
                Q(student__full_name__icontains=search_term)
                | Q(subject__name__icontains=search_term)
                | Q(semester__semester_name__icontains=search_term)
                | Q(notes__icontains=search_term)
            )

        if semester_id:
            filters &= Q(semester__semester_id=semester_id)

        if student_id:
            filters &= Q(student__student_id=student_id)

        if subject_id:
            filters &= Q(subject__subject_id=subject_id)

        return Score.objects.filter(filters).distinct().order_by("-created_at")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_score(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_score(instance)
        return instance

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])

    def _validate_score(self, instance):
        """Kiểm tra logic hợp lệ."""
        if not instance.student or not instance.subject or not instance.semester:
            raise ValueError("Sinh viên, môn học và học kỳ phải được cung cấp.")
        if instance.midterm_score is not None and (
            instance.midterm_score < 0 or instance.midterm_score > 10
        ):
            raise ValueError("Điểm giữa kỳ phải nằm trong khoảng từ 0 đến 10.")
        if instance.final_score is not None and (
            instance.final_score < 0 or instance.final_score > 10
        ):
            raise ValueError("Điểm cuối kỳ phải nằm trong khoảng từ 0 đến 10.")
        if instance.total_score is not None and (
            instance.total_score < 0 or instance.total_score > 10
        ):
            raise ValueError("Tổng điểm phải nằm trong khoảng từ 0 đến 10.")

    @extend_schema(
        summary="Export scores to Excel",
        responses={200: None},
    )
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        try:
            queryset = self.get_queryset()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Scores"

            headers = [
                "ID",
                "Sinh viên",
                "Môn học",
                "Học kỳ",
                "Điểm giữa kỳ",
                "Điểm cuối kỳ",
                "Tổng điểm",
                "Ghi chú",
                "Trạng thái",
                "Hoạt động",
                "Ngày tạo",
                "Ngày cập nhật",
            ]
            sheet.append(headers)

            for score in queryset:
                sheet.append(
                    [
                        score.id,
                        str(score.student),
                        str(score.subject),
                        str(score.semester),
                        str(score.midterm_score) if score.midterm_score is not None else "",
                        str(score.final_score) if score.final_score is not None else "",
                        str(score.total_score) if score.total_score is not None else "",
                        score.notes or "",
                        score.get_status_display(),
                        "Có" if score.is_active else "Không",
                        score.created_at,
                        score.updated_at,
                    ]
                )

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="scores_{timezone.now().strftime("%Y%m%d")}.xlsx"'
            )
            workbook.save(response)
            return response
        except Exception as e:
            logger.error(f"Error exporting scores: {str(e)}")
            return Response(
                {"detail": "Không thể xuất danh sách điểm."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
