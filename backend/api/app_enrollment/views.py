from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from ..app_enrollment.models import Enrollment
from ..app_enrollment.serializers import EnrollmentSerializer
from django.db.models import Q
import pandas as pd
from django.http import HttpResponse
from datetime import datetime

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'is_active', 'semester__semester_id', 'student__student_id', 'subject__subject_id']
    search_fields = ['student__name', 'subject__name', 'semester__name', 'notes']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('app_enrollment.can_manage_enrollment'):
            # Non-managers only see their own enrollments
            if hasattr(self.request.user, 'student'):
                queryset = queryset.filter(student=self.request.user.student)
            else:
                queryset = queryset.none()
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.updated_by = self.request.user
        instance.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def restore(self, request, pk=None):
        try:
            instance = self.get_object()
            if not instance.is_deleted:
                return Response({'error': 'Đăng ký chưa bị xóa.'}, status=status.HTTP_400_BAD_REQUEST)
            instance.is_deleted = False
            instance.updated_by = request.user
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({'data': serializer.data, 'message': 'Khôi phục đăng ký thành công.'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_status(self, request, pk=None):
        try:
            instance = self.get_object()
            new_status = request.data.get('status')
            if new_status not in dict(Enrollment.STATUS_CHOICES):
                return Response({'error': 'Trạng thái không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)
            instance.status = new_status
            instance.updated_by = request.user
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({'data': serializer.data, 'message': 'Cập nhật trạng thái thành công.'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def export(self, request):
        if not request.user.has_perm('app_enrollment.can_export_enrollment'):
            return Response({'error': 'Không có quyền xuất dữ liệu.'}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(self.get_queryset())
        data = []
        for enrollment in queryset:
            data.append({
                'Student ID': enrollment.student.student_id,
                'Student Name': enrollment.student.name,
                'Subject ID': enrollment.subject.subject_id,
                'Subject Name': enrollment.subject.name,
                'Semester ID': enrollment.semester.semester_id,
                'Semester Name': enrollment.semester.name,
                'Class ID': enrollment.class_obj.class_id,
                'Enrollment Date': enrollment.enrollment_date,
                'Status': enrollment.status,
                'Is Active': enrollment.is_active,
                'Notes': enrollment.notes,
                'Created At': enrollment.created_at,
                'Updated At': enrollment.updated_at
            })

        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=enrollments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        df.to_excel(response, index=False)
        return response