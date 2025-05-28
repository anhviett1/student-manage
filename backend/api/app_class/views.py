from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Class
from .serializers import ClassSerializer, ClassCreateSerializer, ClassDetailSerializer
from .forms import ClassForm
from drf_spectacular.utils import extend_schema, extend_schema_view
from ..student_be.mixins import SearchTermMixin
from ..student_be.views import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView
from ..app_home.models import Department


# Create your views here.

@extend_schema_view(
    list=extend_schema(tags=['Classes']),
    retrieve=extend_schema(tags=['Classes']),
    create=extend_schema(tags=['Classes']),
    update=extend_schema(tags=['Classes']),
    partial_update=extend_schema(tags=['Classes']),
    destroy=extend_schema(tags=['Classes']),
    active=extend_schema(tags=['Classes']),
)
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.filter(is_deleted=False)
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ClassCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return ClassDetailSerializer
        return ClassSerializer
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_classes = Class.objects.filter(is_deleted=False)
        serializer = self.get_serializer(active_classes, many=True)
        return Response(serializer.data)

class ClassListView(BaseListView):
    model = Class
    template_name = 'app_class_fe/class_list.html'
    context_object_name = 'classes'
    search_fields = ['class_id', 'name', 'description']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        department_filter = self.request.GET.get('department', '')
        status_filter = self.request.GET.get('status', '')
        semester_filter = self.request.GET.get('semester', '')
        
        if department_filter:
            queryset = queryset.filter(department=department_filter)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if semester_filter:
            queryset = queryset.filter(semester=semester_filter)
            
        return queryset.select_related('created_by', 'semester').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'department_filter': self.request.GET.get('department', ''),
            'status_filter': self.request.GET.get('status', ''),
            'semester_filter': self.request.GET.get('semester', ''),
            'departments': Department.objects.filter(is_active=True),
            'status_choices': Class.STATUS_CHOICES,
        })
        return context

class ClassDetailView(BaseDetailView):
    model = Class
    template_name = 'app_class_fe/class_detail.html'
    context_object_name = 'class'
    
    def get_queryset(self):
        return Class.objects.select_related(
            'created_by', 'semester'
        ).prefetch_related('students', 'teachers', 'subjects')

class ClassCreateView(BaseCreateView):
    model = Class
    form_class = ClassForm
    template_name = 'app_class_fe/class_form.html'
    success_url = 'classes:class_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Thêm lớp học'
        return context

class ClassUpdateView(BaseUpdateView):
    model = Class
    form_class = ClassForm
    template_name = 'app_class_fe/class_form.html'
    success_url = 'classes:class_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Cập nhật lớp học'
        return context

class ClassDeleteView(BaseDeleteView):
    model = Class
    template_name = 'app_class_fe/class_confirm_delete.html'
    success_url = 'classes:class_list'
    
    def delete(self, request, *args, **kwargs):
        class_obj = self.get_object()
        class_obj.is_deleted = True
        class_obj.save()
        messages.success(request, 'Lớp học đã được xóa thành công.')
        return redirect(self.success_url)
