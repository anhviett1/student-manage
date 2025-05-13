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
from .models import Teacher
from .serializers import TeacherSerializer, TeacherCreateSerializer, TeacherDetailSerializer
from .forms import TeacherForm

# Create your views here.

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return TeacherDetailSerializer
        return TeacherSerializer
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        subject = request.query_params.get('subject', None)
        if subject:
            teachers = Teacher.objects.filter(subject=subject)
            serializer = self.get_serializer(teachers, many=True)
            return Response(serializer.data)
        return Response({"error": "Subject parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class TeacherSearchMixin(SearchTermMixin):
    search_fields = ['teacher_id', 'first_name', 'last_name', 'email', 'specialization']

@login_required
def teacher_list(request):
    search_mixin = TeacherSearchMixin()
    search_term = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    faculty_filter = request.GET.get('faculty', '')

    # Base queryset
    teachers = Teacher.objects.select_related('created_by').order_by('-created_at')

    # Apply search and filters
    teachers = search_mixin.get_filtered_queryset(
        teachers,
        search_term,
        search_mixin.search_fields,
        status=status_filter if status_filter else None,
        faculty=faculty_filter if faculty_filter else None
    )

    # Pagination
    paginator = Paginator(teachers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_term': search_term,
        'status_filter': status_filter,
        'faculty_filter': faculty_filter,
        'status_choices': Teacher.STATUS_CHOICES,
        'faculty_choices': Teacher.FACULTY_CHOICES,
    }
    return render(request, 'app_teacher_fe/teacher_list.html', context)

@login_required
@permission_required('app_teacher.can_manage_teacher')
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.created_by = request.user
            teacher.save()
            messages.success(request, 'Giảng viên đã được thêm thành công.')
            return redirect('teacher_detail', pk=teacher.pk)
    else:
        form = TeacherForm()

    context = {
        'form': form,
        'action': 'Thêm giảng viên',
    }
    return render(request, 'app_teacher_fe/teacher_form.html', context)

@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher.objects.select_related(
        'created_by'
    ).prefetch_related('subjects'), pk=pk)
    return render(request, 'app_teacher_fe/teacher_detail.html', {'teacher': teacher})

@login_required
@permission_required('app_teacher.can_manage_teacher')
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Giảng viên đã được cập nhật thành công.')
            return redirect('teacher_detail', pk=teacher.pk)
    else:
        form = TeacherForm(instance=teacher)

    context = {
        'form': form,
        'action': 'Cập nhật giảng viên',
    }
    return render(request, 'app_teacher_fe/teacher_form.html', context)

@login_required
@permission_required('app_teacher.can_manage_teacher')
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Giảng viên đã được xóa thành công.')
        return redirect('teacher_list')
    return render(request, 'app_teacher_fe/teacher_confirm_delete.html', {'teacher': teacher})
