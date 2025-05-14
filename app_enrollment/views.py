from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentCreateSerializer, EnrollmentDetailSerializer
from .forms import EnrollmentForm
from app_subject.models import Subject
from app_semester.models import Semester
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(tags=['Enrollments']),
    retrieve=extend_schema(tags=['Enrollments']),
    create=extend_schema(tags=['Enrollments']),
    update=extend_schema(tags=['Enrollments']),
    partial_update=extend_schema(tags=['Enrollments']),
    destroy=extend_schema(tags=['Enrollments']),
    by_student=extend_schema(tags=['Enrollments']),
    by_class=extend_schema(tags=['Enrollments']),
    by_status=extend_schema(tags=['Enrollments']),
)
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return EnrollmentDetailSerializer
        return EnrollmentSerializer
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id', None)
        if student_id:
            enrollments = Enrollment.objects.filter(student_id=student_id)
            serializer = self.get_serializer(enrollments, many=True)
            return Response(serializer.data)
        return Response({"error": "Student ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def by_class(self, request):
        class_id = request.query_params.get('class_id', None)
        if class_id:
            enrollments = Enrollment.objects.filter(class_id=class_id)
            serializer = self.get_serializer(enrollments, many=True)
            return Response(serializer.data)
        return Response({"error": "Class ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status_val = request.query_params.get('status', None)
        if status_val:
            enrollments = Enrollment.objects.filter(status=status_val)
            serializer = self.get_serializer(enrollments, many=True)
            return Response(serializer.data)
        return Response({"error": "Status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

@login_required
def enrollment_list(request):
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    subject_filter = request.GET.get('subject', '')
    semester_filter = request.GET.get('semester', '')
    status_filter = request.GET.get('status', '')

    # Base queryset
    enrollments = Enrollment.objects.select_related(
        'student', 'subject', 'semester'
    ).order_by('-created_at')

    # Apply filters
    if search_query:
        enrollments = enrollments.filter(
            Q(student__student_id__icontains=search_query) |
            Q(student__full_name__icontains=search_query)
        )
    if subject_filter:
        enrollments = enrollments.filter(subject_id=subject_filter)
    if semester_filter:
        enrollments = enrollments.filter(semester_id=semester_filter)
    if status_filter:
        enrollments = enrollments.filter(status=status_filter)

    # Pagination
    paginator = Paginator(enrollments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options
    subjects = Subject.objects.filter(is_active=True)
    semesters = Semester.objects.filter(is_active=True)
    status_choices = Enrollment.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'subject_filter': subject_filter,
        'semester_filter': semester_filter,
        'status_filter': status_filter,
        'subjects': subjects,
        'semesters': semesters,
        'status_choices': status_choices,
    }
    return render(request, 'app_enrollment_fe/enrollment_list.html', context)

@login_required
@permission_required('app_enrollment.can_manage_enrollment')
def enrollment_create(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.created_by = request.user
            enrollment.save()
            messages.success(request, 'Đăng ký học đã được tạo thành công.')
            return redirect('enrollment_detail', pk=enrollment.pk)
    else:
        form = EnrollmentForm()

    context = {
        'form': form,
        'action': 'Thêm đăng ký học',
    }
    return render(request, 'app_enrollment_fe/enrollment_form.html', context)

@login_required
def enrollment_detail(request, pk):
    enrollment = get_object_or_404(Enrollment.objects.select_related(
        'student', 'subject', 'semester', 'created_by'
    ), pk=pk)
    return render(request, 'app_enrollment_fe/enrollment_detail.html', {'enrollment': enrollment})

@login_required
@permission_required('app_enrollment.can_manage_enrollment')
def enrollment_edit(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký học đã được cập nhật thành công.')
            return redirect('enrollment_detail', pk=enrollment.pk)
    else:
        form = EnrollmentForm(instance=enrollment)

    context = {
        'form': form,
        'action': 'Cập nhật đăng ký học',
    }
    return render(request, 'app_enrollment_fe/enrollment_form.html', context)

@login_required
@permission_required('app_enrollment.can_manage_enrollment')
def enrollment_delete(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Đăng ký học đã được xóa thành công.')
        return redirect('enrollment_list')
    return render(request, 'app_enrollment_fe/enrollment_confirm_delete.html', {'enrollment': enrollment})
