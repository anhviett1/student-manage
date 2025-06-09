from django.db import models
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from ..app_semester.models import Semester
from ..app_semester.serializers import SemesterSerializer

class SemesterPermission(permissions.BasePermission):
    """Custom permission cho Semester"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('app_semester.can_view_semester_details')
        return request.user.has_perm('app_semester.can_manage_semester')

@extend_schema(tags=['Semesters'])
class SemesterViewSet(viewsets.ModelViewSet):
    """API ViewSet cho quản lý học kỳ"""
    queryset = Semester.objects.filter(is_deleted=False)
    serializer_class = SemesterSerializer
    permission_classes = [permissions.IsAuthenticated, SemesterPermission]
    lookup_field = 'semester_id'

    def get_queryset(self):
        """Lọc queryset dựa trên query params"""
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        is_active = self.request.query_params.get('is_active', None)
        search = self.request.query_params.get('search', None)

        if status:
            queryset = queryset.filter(status=status)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(semester_id__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset

    def perform_create(self, serializer):
        """Lưu thông tin người tạo và người cập nhật khi tạo học kỳ"""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """Lưu thông tin người cập nhật khi cập nhật học kỳ"""
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """Thực hiện xóa mềm và lưu thông tin người cập nhật"""
        instance.is_deleted = True
        instance.updated_by = self.request.user
        instance.save()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def active(self, request):
        """Lấy danh sách học kỳ đang hoạt động"""
        semesters = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(semesters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[permissions.IsAuthenticated, SemesterPermission],
        url_path='hard-delete'
    )
    def hard_delete(self, request, semester_id=None):
        """Xóa cứng học kỳ (xóa hoàn toàn khỏi database)"""
        semester_obj = self.get_object()
        semester_obj.delete()
        return Response({'message': _('Học kỳ đã được xóa hoàn toàn.')}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, SemesterPermission], url_path='restore')
    def restore(self, request, semester_id=None):
        try:
            semester = Semester.objects.get(semester_id=semester_id)
            if not semester.is_deleted:
                return Response({'error': _('Học kỳ này chưa bị xóa mềm.')}, status=status.HTTP_400_BAD_REQUEST)
            semester.restore(user=self.request.user)
            serializer = self.get_serializer(semester)
            return Response({'message': _('Khôi phục học kỳ thành công.'), 'data': serializer.data}, status=status.HTTP_200_OK)
        except Semester.DoesNotExist:
            return Response({'error': _('Học kỳ không tồn tại.')}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, SemesterPermission], url_path='change-status')
    def change_status(self, request, semester_id=None):
        semester = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Semester.STATUS_CHOICES).keys():
            return Response({'error': _('Trạng thái không hợp lệ.')}, status=status.HTTP_400_BAD_REQUEST)
        semester.status = new_status
        semester.updated_by = self.request.user
        semester.save()
        serializer = self.get_serializer(semester)
        return Response({'message': _('Cập nhật trạng thái thành công.'), 'data': serializer.data}, status=status.HTTP_200_OK)