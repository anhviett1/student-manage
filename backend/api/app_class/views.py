from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from .models import Class
from .serializers import ClassSerializer

class ClassPermission(permissions.BasePermission):
    """Custom permission cho Class"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('app_class.can_view_class_details')
        return request.user.has_perm('app_class.can_manage_class')

@extend_schema(tags=['Classes'])
class ClassViewSet(viewsets.ModelViewSet):
    """API ViewSet cho quản lý lớp học"""
    queryset = Class.objects.filter(is_deleted=False)
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated, ClassPermission]
    lookup_field = 'class_id'

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
                Q(class_id__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset

    def perform_create(self, serializer):
        """Lưu thông tin người tạo và người cập nhật khi tạo lớp"""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """Lưu thông tin người cập nhật khi cập nhật lớp"""
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """Thực hiện xóa mềm và lưu thông tin người cập nhật"""
        instance.is_deleted = True
        instance.updated_by = self.request.user
        instance.save()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def active(self, request):
        """Lấy danh sách lớp đang hoạt động"""
        classes = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[permissions.IsAuthenticated, ClassPermission],
        url_path='hard-delete'
    )
    def hard_delete(self, request, class_id=None):
        """Xóa cứng lớp học (xóa hoàn toàn khỏi database)"""
        class_obj = self.get_object()
        class_obj.delete()
        return Response({'message': _('Lớp học đã được xóa hoàn toàn.')}, status=status.HTTP_204_NO_CONTENT)