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
from .models import Student
from .serializers import StudentSerializer, StudentCreateSerializer, StudentDetailSerializer
from .forms import StudentForm
from app_home.permissions import IsAdmin, IsTeacher
from drf_spectacular.utils import extend_schema, extend_schema_view
from app_home.models import Department

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
    permission_classes = [IsAuthenticated, IsAdmin]
    
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

class StudentListView(BaseListView):
    model = Student
    template_name = 'app_student_fe/student_list.html'
    context_object_name = 'students'
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    
    def get_queryset(self):
        queryset = Student.objects.all()
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        department_filter = self.request.GET.get('department', '')

        if search_query:
            queryset = queryset.filter(
                Q(student_id__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        if department_filter:
            queryset = queryset.filter(department_id=department_filter)
            
        return queryset.select_related('department')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('search', ''),
            'status_filter': self.request.GET.get('status', ''),
            'department_filter': self.request.GET.get('department', ''),
            'departments': Department.objects.all(),
            'status_choices': Student.STATUS_CHOICES,
        })
        return context

class StudentDetailView(BaseDetailView):
    model = Student
    template_name = 'app_student_fe/student_detail.html'
    context_object_name = 'student'
    
    def get_queryset(self):
        return Student.objects.select_related(
            'user', 'created_by', 'department'
        ).prefetch_related('enrollments', 'scores')

class StudentCreateView(BaseCreateView):
    model = Student
    form_class = StudentForm
    template_name = 'app_student_fe/student_form.html'
    success_url = 'students:student_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Thêm sinh viên'
        return context

class StudentUpdateView(BaseUpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'app_student_fe/student_form.html'
    success_url = 'students:student_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Cập nhật sinh viên'
        return context

class StudentDeleteView(BaseDeleteView):
    model = Student
    template_name = 'app_student_fe/student_confirm_delete.html'
    success_url = 'students:student_list'
    
    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        student.is_deleted = True
        student.save()
        messages.success(request, 'Sinh viên đã được xóa thành công.')
        return redirect(self.success_url)
