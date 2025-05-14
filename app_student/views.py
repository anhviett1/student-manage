from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from student_be.mixins import SearchTermMixin
from .models import Student
from .serializers import StudentSerializer, StudentCreateSerializer, StudentDetailSerializer
from .forms import StudentForm
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(tags=['Students']),
    retrieve=extend_schema(tags=['Students']),
    create=extend_schema(tags=['Students']),
    update=extend_schema(tags=['Students']),
    partial_update=extend_schema(tags=['Students']),
    destroy=extend_schema(tags=['Students']),
    active=extend_schema(tags=['Students']),
)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.filter(is_deleted=False)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return StudentDetailSerializer
        return StudentSerializer
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_students = Student.objects.filter(is_deleted=False)
        serializer = self.get_serializer(active_students, many=True)
        return Response(serializer.data)

class StudentSearchMixin(SearchTermMixin):
    search_fields = ['student_id', 'first_name', 'last_name', 'email']

@login_required
def student_list(request):
    search_mixin = StudentSearchMixin()
    search_term = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    faculty_filter = request.GET.get('faculty', '')

    # Base queryset
    students = Student.objects.select_related('created_by').order_by('-created_at')

    # Apply search and filters
    students = search_mixin.get_filtered_queryset(
        students,
        search_term,
        search_mixin.search_fields,
        status=status_filter if status_filter else None,
        faculty=faculty_filter if faculty_filter else None
    )

    # Pagination
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_term': search_term,
        'status_filter': status_filter,
        'faculty_filter': faculty_filter,
        'status_choices': Student.STATUS_CHOICES,
        'faculty_choices': Student.FACULTY_CHOICES,
    }
    return render(request, 'app_student_fe/student_list.html', context)

@login_required
@permission_required('app_student.can_manage_student')
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.created_by = request.user
            student.save()
            messages.success(request, 'Sinh viên đã được thêm thành công.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()

    context = {
        'form': form,
        'action': 'Thêm sinh viên',
    }
    return render(request, 'app_student_fe/student_form.html', context)

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related(
        'created_by'
    ).prefetch_related('enrollments', 'scores'), pk=pk)
    return render(request, 'app_student_fe/student_detail.html', {'student': student})

@login_required
@permission_required('app_student.can_manage_student')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sinh viên đã được cập nhật thành công.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'action': 'Cập nhật sinh viên',
    }
    return render(request, 'app_student_fe/student_form.html', context)

@login_required
@permission_required('app_student.can_manage_student')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Sinh viên đã được xóa thành công.')
        return redirect('student_list')
    return render(request, 'app_student_fe/student_confirm_delete.html', {'student': student})
