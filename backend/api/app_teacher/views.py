from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Teacher
from .serializers import TeacherSerializer
import pandas as pd
from django.http import HttpResponse
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Teachers'])
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'is_active', 'department__name', 'specialization']
    search_fields = ['teacher_id', 'first_name', 'last_name', 'email']

    def get_queryset(self):
        """
        Lọc queryset dựa trên quyền của người dùng.
        Người không có quyền quản lý chỉ thấy thông tin của chính họ nếu là giảng viên.
        """
        queryset = super().get_queryset()
        if not self.request.user.has_perm('app_teacher.can_manage_teacher'):
            if hasattr(self.request.user, 'teacher'):
                queryset = queryset.filter(user=self.request.user)
            else:
                queryset = queryset.none()
        return queryset

    def perform_create(self, serializer):
        """
        Tạo mới giảng viên, gán thông tin người tạo/cập nhật.
        """
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        """
        Cập nhật giảng viên, gán thông tin người cập nhật.
        """
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """
        Thực hiện xóa mềm bằng cách đánh dấu is_deleted và lưu thông tin người xóa.
        """
        instance.is_deleted = True
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.now()
        instance.save()

    def create(self, request, *args, **kwargs):
        """
        API tạo mới giảng viên.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'data': serializer.data,
            'message': _('Tạo giảng viên thành công.')
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        API lấy thông tin chi tiết giảng viên.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'message': _('Lấy thông tin giảng viên thành công.')
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        API cập nhật thông tin giảng viên.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'data': serializer.data,
            'message': _('Cập nhật giảng viên thành công.')
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        API xóa mềm giảng viên.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': _('Xóa giảng viên thành công.')
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def restore(self, request, pk=None):
        """
        Khôi phục giảng viên đã bị xóa mềm.
        """
        try:
            instance = self.get_object()
            if not instance.is_deleted:
                return Response({'error': _('Giảng viên chưa bị xóa.')}, status=status.HTTP_400_BAD_REQUEST)
            instance.is_deleted = False
            instance.deleted_by = None
            instance.deleted_at = None
            instance.updated_by = request.user
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({
                'data': serializer.data,
                'message': _('Khôi phục giảng viên thành công.')
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_status(self, request, pk=None):
        """
        Thay đổi trạng thái của giảng viên.
        """
        try:
            instance = self.get_object()
            new_status = request.data.get('status')
            if new_status not in dict(Teacher.STATUS_CHOICES):
                return Response({'error': _('Trạng thái không hợp lệ.')}, status=status.HTTP_400_BAD_REQUEST)
            instance.status = new_status
            instance.updated_by = request.user
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({
                'data': serializer.data,
                'message': _('Cập nhật trạng thái thành công.')
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def export(self, request):
        """
        Xuất danh sách giảng viên ra file Excel.
        """
        if not request.user.has_perm('app_teacher.can_manage_teacher'):
            return Response({'error': _('Không có quyền xuất dữ liệu.')}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(self.get_queryset())
        data = []
        for teacher in queryset:
            data.append({
                'Mã Giảng Viên': teacher.teacher_id,
                'Họ và Tên': teacher.get_full_name(),
                'Email': teacher.email,
                'Số Điện Thoại': teacher.phone,
                'Ngày Sinh': teacher.date_of_birth,
                'Giới Tính': dict(Teacher.GENDER_CHOICES).get(teacher.gender, teacher.gender),
                'Trạng Thái': dict(Teacher.STATUS_CHOICES).get(teacher.status, teacher.status),
                'Học Vị': dict(Teacher.DEGREE_CHOICES).get(teacher.degree, teacher.degree),
                'Chuyên Ngành': teacher.specialization,
                'Khoa': teacher.department.name if teacher.department else 'N/A',
                'Ngày Tạo': teacher.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'Ngày Cập Nhật': teacher.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=teachers_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        df.to_excel(response, index=False)
        return response

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Lấy thông tin của giảng viên hiện tại.
        """
        try:
            teacher = Teacher.objects.get(user=request.user)
            serializer = self.get_serializer(teacher)
            return Response({
                'data': serializer.data,
                'message': _('Lấy thông tin giảng viên thành công.')
            }, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response({
                'error': _('Không tìm thấy thông tin giảng viên.')
            }, status=status.HTTP_404_NOT_FOUND)