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
from student_be.views import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Teacher
from .serializers import TeacherSerializer, TeacherCreateSerializer, TeacherDetailSerializer
from .forms import TeacherForm
from app_home.permissions import IsAdmin
from drf_spectacular.utils import extend_schema, extend_schema_view
from app_home.models import Department

# Create your views here.

@extend_schema_view(
    list=extend_schema(tags=['Teachers']),
    retrieve=extend_schema(tags=['Teachers']),
    create=extend_schema(tags=['Teachers']),
    update=extend_schema(tags=['Teachers']),
    partial_update=extend_schema(tags=['Teachers']),
    destroy=extend_schema(tags=['Teachers']),
    active=extend_schema(tags=['Teachers']),
)
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.filter(is_deleted=False)
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return TeacherDetailSerializer
        return TeacherSerializer
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_teachers = Teacher.objects.filter(is_deleted=False)
        serializer = self.get_serializer(active_teachers, many=True)
        return Response(serializer.data)

class TeacherListView(BaseListView):
    model = Teacher
    template_name = 'app_teacher_fe/teacher_list.html'
    context_object_name = 'teachers'
    search_fields = ['teacher_id', 'first_name', 'last_name', 'email']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        department_filter = self.request.GET.get('department', '')
        status_filter = self.request.GET.get('status', '')
        
        if department_filter:
            queryset = queryset.filter(department=department_filter)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.select_related('user', 'created_by').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'department_filter': self.request.GET.get('department', ''),
            'status_filter': self.request.GET.get('status', ''),
            'departments': Department.objects.filter(is_active=True),
            'status_choices': Teacher.STATUS_CHOICES,
        })
        return context

class TeacherDetailView(BaseDetailView):
    model = Teacher
    template_name = 'app_teacher_fe/teacher_detail.html'
    context_object_name = 'teacher'
    
    def get_queryset(self):
        return Teacher.objects.select_related(
            'user', 'created_by'
        ).prefetch_related('classes', 'subjects')

class TeacherCreateView(BaseCreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'app_teacher_fe/teacher_form.html'
    success_url = 'teachers:teacher_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Thêm giáo viên'
        return context

class TeacherUpdateView(BaseUpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'app_teacher_fe/teacher_form.html'
    success_url = 'teachers:teacher_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Cập nhật giáo viên'
        return context

class TeacherDeleteView(BaseDeleteView):
    model = Teacher
    template_name = 'app_teacher_fe/teacher_confirm_delete.html'
    success_url = 'teachers:teacher_list'
    
    def delete(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.is_deleted = True
        teacher.save()
        messages.success(request, 'Giáo viên đã được xóa thành công.')
        return redirect(self.success_url)
