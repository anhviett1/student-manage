from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..student_be.mixins import SearchTermMixin
from ..student_be.views import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Subject
from .serializers import SubjectSerializer, SubjectCreateSerializer, SubjectDetailSerializer
from .forms import SubjectForm
from drf_spectacular.utils import extend_schema, extend_schema_view
from ..app_home.models import Department

# Create your views here.

@extend_schema_view(
    list=extend_schema(tags=['Subjects']),
    retrieve=extend_schema(tags=['Subjects']),
    create=extend_schema(tags=['Subjects']),
    update=extend_schema(tags=['Subjects']),
    partial_update=extend_schema(tags=['Subjects']),
    destroy=extend_schema(tags=['Subjects']),
    active=extend_schema(tags=['Subjects']),
)
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.filter(is_deleted=False)
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SubjectCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return SubjectDetailSerializer
        return SubjectSerializer
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_subjects = Subject.objects.filter(is_deleted=False)
        serializer = self.get_serializer(active_subjects, many=True)
        return Response(serializer.data)

class SubjectListView(BaseListView):
    model = Subject
    template_name = 'app_subject_fe/subject_list.html'
    context_object_name = 'subjects'
    search_fields = ['subject_id', 'name', 'description']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        department_filter = self.request.GET.get('department', '')
        status_filter = self.request.GET.get('status', '')
        
        if department_filter:
            queryset = queryset.filter(department=department_filter)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.select_related('created_by').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'department_filter': self.request.GET.get('department', ''),
            'status_filter': self.request.GET.get('status', ''),
            'departments': Department.objects.filter(is_active=True),
            'status_choices': Subject.STATUS_CHOICES,
        })
        return context

class SubjectDetailView(BaseDetailView):
    model = Subject
    template_name = 'app_subject_fe/subject_detail.html'
    context_object_name = 'subject'
    
    def get_queryset(self):
        return Subject.objects.select_related(
            'created_by'
        ).prefetch_related('classes', 'teachers')

class SubjectCreateView(BaseCreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'app_subject_fe/subject_form.html'
    success_url = 'subjects:subject_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Thêm môn học'
        return context

class SubjectUpdateView(BaseUpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'app_subject_fe/subject_form.html'
    success_url = 'subjects:subject_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Cập nhật môn học'
        return context

class SubjectDeleteView(BaseDeleteView):
    model = Subject
    template_name = 'app_subject_fe/subject_confirm_delete.html'
    success_url = 'subjects:subject_list'
    
    def delete(self, request, *args, **kwargs):
        subject = self.get_object()
        subject.is_deleted = True
        subject.save()
        messages.success(request, 'Môn học đã được xóa thành công.')
        return redirect(self.success_url)
