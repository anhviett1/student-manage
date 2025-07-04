from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Teacher
from .serializers import TeacherSerializer
from ..app_home.permissions import IsAdmin, IsAdminOrTeacher, IsOwnerOrAdmin,  HasModelPermission
from drf_spectacular.utils import extend_schema,  OpenApiParameter
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=["Teachers"])
class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'teacher_id'

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminOrTeacher()]
        if self.action == ["retrieve", "me"]:
            return [IsOwnerOrAdmin()]
        elif self.action in ["create", "update", "partial_update"]:
            return [IsAdmin() , HasModelPermission(codename="change_teacher")]
        elif self.action == "destroy":
            return [IsAdmin() , HasModelPermission(codename="delete_teacher")]
        elif self.action in ["restore", "change_status"]:
            return [IsAdmin() , HasModelPermission(codename="change_teacher")]
        elif self.action == "export":
            return [IsAdmin()]
        
        return super().get_permissions()

    def get_queryset(self):
        queryset = Teacher.objects.none()
        
        if self.request.user.is_authenticated:
            filters = Q()
            search_term = self.request.query_params.get("searchTerm", "")
            status_filter = self.request.query_params.get("status", "")
            department_filter = self.request.query_params.get("department", "")
            degree_filter = self.request.query_params.get("degree", "")
            gender_filter = self.request.query_params.get("gender", "")
            
            status_list = status_filter.split(",") if status_filter else ["active"]
            department_list = [int(id) for id in department_filter.split(",") if id.isdigit()]
            degree_list = degree_filter.split(",") if degree_filter else []
            gender_list = gender_filter.split(",") if gender_filter else []
            
            filters &= Q(status__in=status_list)

            if search_term:
                filters &= (
                    Q(teacher_id__icontains=search_term)  
                    | Q(first_name__icontains=search_term)                  
                    | Q(last_name__icontains=search_term)                  
                    | Q(email__icontains=search_term)
                    | Q(specialization__icontains=search_term)
                )

            if department_list:
                filters &= Q(department__id__in=department_list)
            if degree_list:
                filters &= Q(degree__in=degree_list)
            if gender_list:
                filters &= Q(gender__in=gender_list)
            queryset = (
                Teacher.objects.filter(filters).distinct().order_by("teacher_id")
            )
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"Created teacher: { instance.teacher_id}")
        
   
    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(f"Updated teacher: { instance.teacher_id}")
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=["is_deleted", "is_active"])
        logger.info(f"Soft delete teacher: { instance.teacher_id}")
    
    @action(detail=False, methods=["get"], url_path="me")
    @extend_schema(
        #summary="Lấy thông tin giảng viên hiện tại",
        #description="Trả về thông tin chi tiết của giảng viên hiện tại dựa trên user đang đăng nhập.",
        responses={200: TeacherSerializer},
    )
    def me(self, request):
        """Lấy thông tin giảng viên hiện tại."""
        try:
            teacher = Teacher.objects.get(user=request.user, is_deleted=False)
            serializer = TeacherSerializer(teacher)
            logger.info(f"Retrieved profile for teacher: {teacher.teacher_id}")
            return Response({"message": "Lấy thông tin giảng viên thành công", "data": serializer.data}, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            logger.error(f"No teacher profile found for user: {request.user.username}")
            return Response(
                {"detail": "Không tìm thấy thông tin giảng viên"},
                status=status.HTTP_404_NOT_FOUND,
            )
            
    @action(detail=True, methods=["post"], url_path="restore")
    @extend_schema(
        summary="Khôi phục giáo viên",
        description="Khôi phục giáo viên xóa mềm.",
        responses={200: TeacherSerializer},
    )
    def restore(self, request, pk=None):
        try:
            teacher= Teacher.objects.get(pk=pk, is_delete=True)
            teacher.is_deleted = False
            teacher.is_active = True
            teacher.deleted_at = None
            teacher.save(update_fields=["is_delete", "is_active", "deleted_at"])
            logger.info(f"Restored teacher: {teacher.teacher_id}")
            return Response(
                {"message": "Khôi phục giáo viên thành công", "data": TeacherSerializer(teacher).data},
                status=status.HTTP_200_OK,
            )
        except Teacher.DoesNotExist:
            logger.error(f"Teacher with id {pk} not found or not deleted")
            return Response(
                {"detail": "Giáo viên không tồn tại hoặc chưa bị xóa"},
                status=status.HTTP_404_NOT_FOUND,
            )
    
    @action(detail=True, methods=["post"], url_path="change-status")
    @extend_schema(
        summary="Thay đổi trạng thái giáo viên",
        description="Thay đổi trạng thái giáo viên (active, inactive, graduated, suspended, on_leave).",
        parameters=[
            OpenApiParameter(name="status", type=str, description="Trạng thái mới của giáo viên")         
        ],
        responses={200: TeacherSerializer},
    )
    
    def change_status(self, request, pk=None):
        status_value = request.data.get("status")
        if not status_value or status_value not in dict(Teacher.STATUS_CHOICES).key():
            logger.error(f"Invalid status: {status_value}")
            return Response(
                {"detail": "Trạng thái không hợp lệ"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            teacher = Teacher.objects.get(pk=pk)
            teacher.status = status_value
            teacher.save(update_fields=["status"])
            logger.info(f"Changed status of student {teacher.teacher_id} to {status_value}")
            return Response(
                {"message": "Cập nhật trang thái thành công", "data": TeacherSerializer(teacher).data},
                status=status.HTTP_200_OK,
            )  
        except Teacher.DoesNotExist:
            logger.error(f"Teacher with id {pk} not found")
            return Response(
                {"detail": "Giáo viên không tồn tại"},
                status=status.HTTP_404_NOT_FOUND,
            )  
        
    @action(detail=False, methods=["get"], url_path="export")
    @extend_schema(
        summary="Xuất danh sách giảng viên",
        description="Xuất danh sách giảng viên dưới dạng file Excel.",
    )
    def export(self, request):
        """Xuất danh sách giảng viên dưới dạng Excel."""
        queryset = self.get_queryset()
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Teachers"

        headers = [
            "Mã Giảng Viên", "Họ", "Tên", "Email", "Số Điện Thoại", "Ngày Sinh",
            "Giới Tính", "Địa Chỉ", "Học Vị", "Chuyên Ngành", "Số Năm Kinh Nghiệm",
            "Tiểu Sử", "Trạng Thái", "Khoa",
        ]
        worksheet.append(headers)

        for teacher in queryset:
            row = [
                teacher.teacher_id,
                teacher.last_name,
                teacher.first_name,
                teacher.email,
                teacher.phone,
                teacher.date_of_birth,
                dict(Teacher.GENDER_CHOICES).get(teacher.gender, teacher.gender),
                teacher.address,
                dict(Teacher.DEGREE_CHOICES).get(teacher.degree, teacher.degree),
                teacher.specialization,
                teacher.years_of_experience,
                teacher.bio or "",
                dict(Teacher.STATUS_CHOICES).get(teacher.status, teacher.status),
                teacher.department.name if teacher.department else "",
            ]
            worksheet.append(row)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f"attachment; filename=teachers_{timezone.now().strftime('%Y%m%d')}.xlsx"
        workbook.save(response)
        #logger.info("Exported teacher list to Excel")
        return response