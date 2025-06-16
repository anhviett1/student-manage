from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Student
from .serializers import StudentSerializer
import pandas as pd
from django.http import HttpResponse
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Students'])
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'is_active', 'department__name', 'major']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']

    def get_queryset(self):
        """
        Lọc queryset dựa trên quyền của người dùng.
        Người không có quyền quản lý chỉ thấy thông tin của chính họ nếu là sinh viên.
        """
        queryset = super().get_queryset()
        if not self.request.user.has_perm('app_student.can_manage_student'):
            if hasattr(self.request.user, 'student'):
                queryset = queryset.filter(user=self.request.user)
            else:
                queryset = queryset.none()
        return queryset

    def perform_create(self, serializer):
        """
        Tạo mới sinh viên, xử lý quan hệ ManyToMany và gán thông tin người tạo/cập nhật.
        """
        class_assigned_ids = serializer.validated_data.pop('class_assigned', [])
        subject_ids = serializer.validated_data.pop('subjects', [])
        score_ids = serializer.validated_data.pop('scores', [])
        student = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )
        student.class_assigned.set(class_assigned_ids)
        student.subjects.set(subject_ids)
        student.scores.set(score_ids)

    def perform_update(self, serializer):
        """
        Cập nhật sinh viên, xử lý quan hệ ManyToMany và gán thông tin người cập nhật.
        """
        class_assigned_ids = serializer.validated_data.pop('class_assigned', None)
        subject_ids = serializer.validated_data.pop('subjects', None)
        score_ids = serializer.validated_data.pop('scores', None)
        student = serializer.save(updated_by=self.request.user)
        if class_assigned_ids is not None:
            student.class_assigned.set(class_assigned_ids)
        if subject_ids is not None:
            student.subjects.set(subject_ids)
        if score_ids is not None:
            student.scores.set(score_ids)

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
        API tạo mới sinh viên.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'data': serializer.data,
            'message': _('Tạo sinh viên thành công.')
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        API lấy thông tin chi tiết sinh viên.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'message': _('Lấy thông tin sinh viên thành công.')
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        API cập nhật thông tin sinh viên.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'data': serializer.data,
            'message': _('Cập nhật sinh viên thành công.')
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        API xóa mềm sinh viên.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': _('Xóa sinh viên thành công.')
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def restore(self, request, pk=None):
        """
        Khôi phục sinh viên đã bị xóa mềm.
        """
        try:
            instance = self.get_object()
            if not instance.is_deleted:
                return Response({'error': _('Sinh viên chưa bị xóa.')}, status=status.HTTP_400_BAD_REQUEST)
            instance.is_deleted = False
            instance.deleted_by = None
            instance.deleted_at = None
            instance.updated_by = request.user
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({
                'data': serializer.data,
                'message': _('Khôi phục sinh viên thành công.')
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_status(self, request, pk=None):
        """
        Thay đổi trạng thái của sinh viên.
        """
        try:
            instance = self.get_object()
            new_status = request.data.get('status')
            if new_status not in dict(Student.STATUS_CHOICES):
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
        Xuất danh sách sinh viên ra file Excel.
        """
        if not request.user.has_perm('app_student.can_manage_student'):
            return Response({'error': _('Không có quyền xuất dữ liệu.')}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(self.get_queryset())
        data = []
        for student in queryset:
            data.append({
                'Mã Sinh Viên': student.student_id,
                'Họ và Tên': student.get_full_name(),
                'Email': student.email,
                'Số Điện Thoại': student.phone,
                'Ngày Sinh': student.date_of_birth,
                'Giới Tính': dict(Student.GENDER_CHOICES).get(student.gender, student.gender),
                'Trạng Thái': dict(Student.STATUS_CHOICES).get(student.status, student.status),
                'Chuyên Ngành': student.major,
                'GPA': student.gpa,
                'Tín Chỉ Tích Lũy': student.credits_earned,
                'Khoa': student.department.name,
                'Ngày Tạo': student.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'Ngày Cập Nhật': student.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=students_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        df.to_excel(response, index=False)
        return response

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Lấy thông tin của sinh viên hiện tại.
        """
        try:
            student = Student.objects.get(user=request.user)
            serializer = self.get_serializer(student)
            return Response({
                'data': serializer.data,
                'message': _('Lấy thông tin sinh viên thành công.')
            }, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({
                'error': _('Không tìm thấy thông tin sinh viên.')
            }, status=status.HTTP_404_NOT_FOUND)