from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Student
from .serializers import StudentSerializer
from ..app_home.permissions import (
    IsAdmin,
    IsAdminOrTeacher,
    ProfilePermission,
    StudentAddPermission,
    StudentChangePermission,
    StudentDeletePermission,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
import logging
import re

logger = logging.getLogger(__name__)


@extend_schema(tags=["Students"])
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAdmin]
    lookup_field = "student_id"

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminOrTeacher()]
        if self.action == "retrieve":
            return [ProfilePermission()]
        elif self.action == "create":
            return [IsAdmin(), StudentAddPermission()]
        elif self.action in ["update", "partial_update", "restore", "change_status"]:
            return [IsAdmin(), StudentChangePermission()]
        elif self.action == "destroy":
            return [IsAdmin(), StudentDeletePermission()]
        elif self.action in ["export", "me"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Student.objects.none()

        filters = Q()
        query = self.request.query_params
        search_term = query.get("searchTerm", "")
        status_filter = query.get("status", "")
        department_filter = query.get("department", "")
        class_filter = query.get("class_assigned", "")
        gender_filter = query.get("gender", "")
        start_date = query.get("startDate")
        end_date = query.get("endDate")

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
            filters &= Q(department__department_id__in=department_list)
        if class_list:
            filters &= Q(class_assigned__id__in=class_list)
        if gender_list:
            filters &= Q(gender__in=gender_list)

        return Student.objects.filter(filters).distinct().order_by("student_id")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._validate_student(instance)
        instance.calculate_gpa()
        logger.info(f"Created student: {instance.student_id}")

    def perform_update(self, serializer):
        instance = serializer.save()
        self._validate_student(instance)
        instance.calculate_gpa()
        logger.info(f"Updated student: {instance.student_id}")

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["is_deleted", "is_active", "deleted_at"])
        logger.info(f"Soft delete student: {instance.student_id}")

    def _validate_student(self, instance):
        """Kiểm tra logic hợp lệ."""
        if not instance.first_name or not instance.last_name:
            raise ValueError("Họ và tên không được để trống.")
        if instance.gpa is not None and (instance.gpa < 0 or instance.gpa > 4.0):
            raise ValueError("GPA phải nằm trong khoảng từ 0 đến 4.0.")
        if instance.email and not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", instance.email
        ):
            raise ValueError("Email không hợp lệ.")
        if instance.phone and not re.match(r"^(0|\+84)\d{9}$", instance.phone):
            raise ValueError("Số điện thoại không hợp lệ.")

    @extend_schema(
        summary="Get current student's profile",
        responses={200: StudentSerializer},
    )
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            student = Student.objects.get(user=request.user, is_deleted=False)
            serializer = self.get_serializer(student)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            logger.error(f"Student profile not found for user {request.user.id}")
            return Response(
                {"detail": "Không tìm thấy thông tin sinh viên cho người dùng này."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Error fetching student profile: {str(e)}")
            return Response(
                {"detail": "Có lỗi xảy ra khi lấy thông tin sinh viên."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Khôi phục sinh viên",
        description="Khôi phục sinh viên xóa mềm.",
        responses={200: StudentSerializer},
    )
    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk, is_deleted=True)
            student.is_deleted = False
            student.is_active = True
            student.deleted_at = None
            student.save(update_fields=["is_deleted", "is_active", "deleted_at"])
            return Response(
                {
                    "message": "Khôi phục sinh viên thành công",
                    "data": StudentSerializer(student).data,
                },
                status=status.HTTP_200_OK,
            )
        except Student.DoesNotExist:
            logger.error(f"Student with id {pk} not found or not deleted")
            return Response(
                {"detail": "Sinh viên không tồn tại hoặc chưa bị xóa"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        summary="Thay đổi trạng thái sinh viên",
        description="Thay đổi trạng thái sinh viên (active, inactive, graduated, suspended, on_leave).",
        parameters=[
            OpenApiParameter(name="status", type=str, description="Trạng thái mới của sinh viên")
        ],
        responses={200: StudentSerializer},
    )
    @action(detail=True, methods=["post"], url_path="change-status")
    def change_status(self, request, pk=None):
        status_value = request.data.get("status")
        if not status_value or status_value not in dict(Student.STATUS_CHOICES).keys():
            logger.error(f"Invalid status: {status_value}")
            return Response(
                {"detail": "Trạng thái không hợp lệ"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            student = Student.objects.get(pk=pk)
            student.status = status_value
            student.save(update_fields=["status"])
            return Response(
                {
                    "message": "Cập nhật trạng thái thành công",
                    "data": StudentSerializer(student).data,
                },
                status=status.HTTP_200_OK,
            )
        except Student.DoesNotExist:
            logger.error(f"Student with id {pk} not found")
            return Response(
                {"detail": "Sinh viên không tồn tại"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        summary="Xuất danh sách sinh viên",
        description="Xuất danh sách sinh viên dưới dạng file Excel.",
        responses={200: None},
    )
    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        try:
            queryset = self.get_queryset()
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Students"

            headers = [
                "Mã Sinh Viên",
                "Họ",
                "Tên",
                "Email",
                "Số Điện Thoại",
                "Ngày Sinh",
                "Giới Tính",
                "Địa Chỉ",
                "Thành Phố",
                "Tỉnh/Thành",
                "Quốc Gia",
                "Chuyên Ngành",
                "GPA",
                "Trạng Thái",
                "Khoa",
                "Ngày Nhập Học",
                "Ngày Tốt Nghiệp",
                "Người Liên Hệ Khẩn Cấp",
                "SĐT Khẩn Cấp",
                "Mối Quan Hệ",
            ]
            worksheet.append(headers)

            for student in queryset:
                row = [
                    student.student_id,
                    student.last_name,
                    student.first_name,
                    student.email or "",
                    student.phone or "",
                    student.date_of_birth,
                    (
                        dict(Student.GENDER_CHOICES).get(student.gender, student.gender)
                        if student.gender
                        else ""
                    ),
                    student.address or "",
                    student.city or "",
                    student.state or "",
                    student.country or "",
                    student.major or "",
                    str(student.gpa) if student.gpa is not None else "",
                    dict(Student.STATUS_CHOICES).get(student.status, student.status),
                    student.department.department_name if student.department else "",
                    student.enrollment_date,
                    student.graduation_date or "",
                    student.emergency_contact_name or "",
                    student.emergency_contact_phone or "",
                    student.emergency_contact_relationship or "",
                ]
                worksheet.append(row)

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = (
                f"attachment; filename=students_{timezone.now().strftime('%Y%m%d')}.xlsx"
            )
            workbook.save(response)
            return response
        except Exception as e:
            logger.error(f"Error exporting students: {str(e)}")
            return Response(
                {"detail": "Không thể xuất danh sách sinh viên."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
