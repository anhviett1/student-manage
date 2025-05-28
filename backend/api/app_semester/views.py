from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from ..student_be.views import BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Semester
from .forms import SemesterForm
from .serializers import SemesterSerializer

class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.filter(is_deleted=False)
    serializer_class = SemesterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Semester.objects.filter(is_deleted=False)
        status = self.request.query_params.get('status', None)
        is_active = self.request.query_params.get('is_active', None)
        search = self.request.query_params.get('search', None)

        if status:
            queryset = queryset.filter(status=status)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(semester_id__icontains=search) |
                Q(academic_year__icontains=search)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    @action(detail=False, methods=['get'])
    def active(self, request):
        semesters = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(semesters, many=True)
        return Response(serializer.data)

class SemesterListView(BaseListView):
    model = Semester
    template_name = 'app_semester_fe/semester_list.html'
    context_object_name = 'semesters'
    ordering = ['-start_date']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        is_active = self.request.GET.get('is_active')
        search = self.request.GET.get('search')

        if status:
            queryset = queryset.filter(status=status)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(semester_id__icontains=search) |
                Q(academic_year__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Semester.STATUS_CHOICES
        return context

class SemesterDetailView(BaseDetailView):
    model = Semester
    template_name = 'app_semester_fe/semester_detail.html'
    context_object_name = 'semester'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Semester.STATUS_CHOICES
        return context

class SemesterCreateView(BaseCreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'app_semester_fe/semester_form.html'
    success_url = reverse_lazy('semesters:semester_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = _('Thêm học kỳ mới')
        return context

class SemesterUpdateView(BaseUpdateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'app_semester_fe/semester_form.html'
    success_url = reverse_lazy('semesters:semester_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = _('Cập nhật học kỳ')
        return context

class SemesterDeleteView(BaseDeleteView):
    model = Semester
    template_name = 'app_semester_fe/semester_confirm_delete.html'
    success_url = reverse_lazy('semesters:semester_list')

    def delete(self, request, *args, **kwargs):
        semester = self.get_object()
        semester.is_deleted = True
        semester.save()
        messages.success(request, _('Học kỳ đã được xóa thành công.'))
        return redirect(self.success_url)
