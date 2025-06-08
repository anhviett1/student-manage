from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Subject
from .serializers import SubjectSerializer
from datetime import datetime
import pandas as pd
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'is_active', 'department__name', 'semester__name']
    search_fields = ['subject_id', 'name']

    def get_queryset(self):
        """
        Lọc queryset dựa trên quyền của người dùng.
        Người không có quyền quản lý chỉ thấy các môn học đang hoạt động và chưa bị xóa.
        """
        queryset = super().get_queryset()
        if not self.request.user.has_perm('app_subject.can_manage_subject'):
            queryset = queryset.filter(is_active=True, is_deleted=False)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Tạo mới một môn học.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'data': serializer.data,
            'message': _('Tạo môn học thành công.')
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Lấy thông tin chi tiết của một môn học.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'message': _('Lấy thông tin môn học thành công.')
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Cập nhật thông tin môn học.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'data': serializer.data,
            'message': _('Cập nhật môn học thành công.')
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Xóa mềm một môn học.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': _('Xóa môn học thành công.')
        }, status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """
        Lưu thông tin người tạo và người cập nhật khi tạo mới môn học.
        """
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """
        Cập nhật thông tin người cập nhật khi chỉnh sửa môn học.
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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def restore(self, request, pk=None):
        """
        Khôi phục môn học đã bị xóa mềm.
        """
        try:
            instance = self.get_object()
            if not instance.is_deleted:
                return Response({'error': _('Môn học chưa bị xóa.')}, status=status.HTTP_400_BAD_REQUEST)
            instance.is_deleted = False
            instance.deleted_by = None
            instance.deleted_at = None
            instance.updated_by = request.user
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({
                'data': serializer.data,
                'message': _('Khôi phục môn học thành công.')
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_status(self, request, pk=None):
        """
        Thay đổi trạng thái của môn học.
        """
        try:
            instance = self.get_object()
            new_status = request.data.get('status')
            if new_status not in dict(Subject.STATUS_CHOICES):
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
        Xuất danh sách môn học ra file Excel.
        """
        if not request.user.has_perm('app_subject.can_manage_subject'):
            return Response({'error': _('Không có quyền xuất dữ liệu.')}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(self.get_queryset())
        data = []
        for subject in queryset:
            data.append({
                'Mã Môn Học': subject.subject_id,
                'Tên Môn Học': subject.name,
                'Số Tín Chỉ': subject.credits,
                'Học Kỳ': subject.semester.name if subject.semester else 'N/A',
                'Khoa': subject.department.name if subject.department else 'N/A',
                'Trạng Thái': dict(Subject.STATUS_CHOICES).get(subject.status, subject.status),
                'Hoạt Động': 'Có' if subject.is_active else 'Không',
                'Ngày Tạo': subject.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'Ngày Cập Nhật': subject.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=subjects_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        df.to_excel(response, index=False)
        return response