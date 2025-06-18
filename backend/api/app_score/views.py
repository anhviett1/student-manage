from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiParameter
from ..app_score.models import Score
from ..app_student.models import Student
from ..app_subject.models import Subject
from ..app_semester.models import Semester
from ..app_score.serializers import ScoreSerializer
import pandas as pd
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser

class ScorePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('app_score.can_view_score_details')
        return request.user.has_perm('app_score.can_manage_scores')

@extend_schema(tags=['Scores'])
class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated, ScorePermission]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        student_id = self.request.query_params.get('student_id', None)

        if status:
            queryset = queryset.filter(status=status)
        if student_id:
            queryset = queryset.filter(student__student_id=student_id)
        elif self.request.user.is_authenticated and self.request.user.is_student:
            # Lọc điểm của sinh viên đang đăng nhập
            try:
                student = Student.objects.get(user=self.request.user)
                queryset = queryset.filter(student=student)
            except Student.DoesNotExist:
                queryset = queryset.none()
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete(user=self.request.user)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def active(self, request):
        scores = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['DELETE'], permission_classes=[permissions.IsAuthenticated, ScorePermission], url_path='hard-delete')
    def hard_delete(self, request, pk=None):
        score = self.get_object()
        score.delete()
        return Response({'message': _('Điểm số đã được xóa hoàn toàn.')}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, ScorePermission], url_path='restore')
    def restore(self, request, pk=None):
        try:
            score = Score.objects.get(id=pk)
            if not score.is_active:
                return Response({'error': _('Điểm số này chưa bị xóa mềm.')}, status=status.HTTP_400_BAD_REQUEST)
            score.restore(user=self.request.user)
            serializer = self.get_serializer(score)
            return Response({'message': _('Khôi phục điểm số thành công.'), 'data': serializer.data}, status=status.HTTP_200_OK)
        except Score.DoesNotExist:
            return Response({'error': _('Điểm số không tồn tại.')}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, ScorePermission], url_path='change-status')
    def change_status(self, request, pk=None):
        score = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Score.STATUS_CHOICES).keys():
            return Response({'error': _('Trạng thái không hợp lệ.')}, status=status.HTTP_400_BAD_REQUEST)
        score.status = new_status
        score.updated_by = self.request.user
        score.save()
        serializer = self.get_serializer(score)
        return Response({'message': _('Cập nhật trạng thái thành công.'), 'data': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated, ScorePermission], url_path='upload-student-list')
    def upload_student_list(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': _('Vui lòng chọn file Excel.')}, status=status.HTTP_400_BAD_REQUEST)
        try:
            df = pd.read_excel(file)
            required_columns = ['student_id', 'name']
            if not all(col in df.columns for col in required_columns):
                return Response({'error': _('File Excel thiếu cột: student_id, name.')}, status=status.HTTP_400_BAD_REQUEST)

            students = []
            for _, row in df.iterrows():
                student, created = Student.objects.get_or_create(
                    student_id=row['student_id'],
                    defaults={'name': row['name'], 'user': None}
                )
                students.append({'student_id': student.student_id, 'name': student.name})
            return Response({'message': _('Tải danh sách sinh viên thành công.'), 'students': students}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated, ScorePermission], url_path='upload-scores')
    def upload_scores(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': _('Vui lòng chọn file Excel.')}, status=status.HTTP_400_BAD_REQUEST)
        try:
            df = pd.read_excel(file)
            required_columns = ['student_id', 'subject_id', 'semester_id', 'midterm_score', 'final_score']
            if not all(col in df.columns for col in required_columns):
                return Response({'error': _('File cần các cột: student_id, subject_id, semester_id, midterm_score, final_score.')}, status=status.HTTP_400_BAD_REQUEST)

            errors = []
            for idx, row in df.iterrows():
                try:
                    student = Student.objects.get(student_id=row['student_id'])
                    subject = Subject.objects.get(subject_id=row['subject_id'])
                    semester = Semester.objects.get(semester_id=row['semester_id'])
                    score, created = Score.objects.update_or_create(
                        student=student,
                        subject=subject,
                        semester=semester,
                        defaults={
                            'midterm_score': row['midterm_score'],
                            'final_score': row['final_score'],
                            'status': 'active',
                        }
                    )
                except Exception as e:
                    errors.append(f"Dòng {idx+2}: {str(e)}")
            if errors:
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': _('Nhập điểm số thành công.')}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated, ScorePermission], url_path='export-scores')
    def export_scores(self, request):
        scores = self.get_queryset()
        data = []
        for score in scores:
            data.append({
                'student_id': score.student.student_id,
                'subject_id': score.subject.subject_id,
                'semester_id': score.semester.semester_id,
                'midterm_score': score.midterm_score,
                'final_score': score.final_score,
                'total_score': score.total_score,
                'status': score.status,
                'notes': score.notes
            })
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=scores.xlsx'
        df.to_excel(response, index=False)
        return response