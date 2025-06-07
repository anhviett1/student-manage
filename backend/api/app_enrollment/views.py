from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..student_be.views import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentCreateSerializer, EnrollmentDetailSerializer
from .forms import EnrollmentForm
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(tags=['Enrollments']),
    retrieve=extend_schema(tags=['Enrollments']),
    create=extend_schema(tags=['Enrollments']),
    update=extend_schema(tags=['Enrollments']),
    partial_update=extend_schema(tags=['Enrollments']),
    destroy=extend_schema(tags=['Enrollments']),
    active=extend_schema(tags=['Enrollments']),
)
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.filter(is_deleted=False)
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return EnrollmentDetailSerializer
        return EnrollmentSerializer
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_enrollments = Enrollment.objects.filter(is_deleted=False)
        serializer = self.get_serializer(active_enrollments, many=True)
        return Response(serializer.data)

class EnrollmentListView(BaseListView):
    model = Enrollment
    search_fields = ['student__student_id', 'student__first_name', 'student__last_name', 'class__name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        class_filter = self.request.GET.get('class', '')
        semester_filter = self.request.GET.get('semester', '')
        status_filter = self.request.GET.get('status', '')
        
        if class_filter:
            queryset = queryset.filter(class_obj=class_filter)
        if semester_filter:
            queryset = queryset.filter(semester=semester_filter)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.select_related(
            'student', 'class_obj', 'semester', 'created_by'
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'class_filter': self.request.GET.get('class', ''),
            'semester_filter': self.request.GET.get('semester', ''),
            'status_filter': self.request.GET.get('status', ''),
            'status_choices': Enrollment.STATUS_CHOICES,
        })
        return context

class EnrollmentDetailView(BaseDetailView):
    model = Enrollment
    
    def get_queryset(self):
        return Enrollment.objects.select_related(
            'student', 'class_obj', 'semester', 'created_by'
        )

class EnrollmentCreateView(BaseCreateView):
    model = Enrollment
    form_class = EnrollmentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Thêm đăng ký học'
        return context

class EnrollmentUpdateView(BaseUpdateView):
    model = Enrollment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Cập nhật đăng ký học'
        return context

class EnrollmentDeleteView(BaseDeleteView):
    model = Enrollment

    
    def delete(self, request, *args, **kwargs):
        enrollment = self.get_object()
        enrollment.is_deleted = True
        enrollment.save()
        messages.success(request, 'Đăng ký học đã được xóa thành công.')
        return redirect(self.success_url)
