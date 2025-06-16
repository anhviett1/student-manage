from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .mixins import StaffRequiredMixin, SuperuserRequiredMixin, SearchTermMixin
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from ..app_student.models import Student

class BaseListView(LoginRequiredMixin, StaffRequiredMixin, ListView, SearchTermMixin):
    template_name = None
    context_object_name = 'object_list'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.get_search_query(self.request)
        if search_query:
            queryset = queryset.filter(search_query)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class BaseDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    template_name = None
    context_object_name = 'object'

class BaseCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    template_name = None
    success_url = None
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'{self.model.__name__} đã được tạo thành công.')
        return super().form_valid(form)

class BaseUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    template_name = None
    success_url = None
    
    def form_valid(self, form):
        messages.success(self.request, f'{self.model.__name__} đã được cập nhật thành công.')
        return super().form_valid(form)

class BaseDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    template_name = None
    success_url = None
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'{self.model.__name__} đã được xóa thành công.')
        return super().delete(request, *args, **kwargs)

class APIGatewayView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        description="API Gateway root endpoint",
        responses={200: dict}
    )
    def get(self, request, format=None):
        api_documentation = {
            'documentation': '/api/docs/',
            'schema': '/api/schema/',
            'redoc': '/api/redoc/',
        }
        
        api_modules = {
            'app_academic': {
                'api/students': '/api/v1/students/',
                'api/teachers': '/api/v1/teachers/',
                'api/subjects': '/api/v1/subjects/',
            },
            'app_education': {
                'api/classes': '/api/v1/classes/',
                'api/scores': '/api/v1/scores/',
            },
            'app_business': {
                'api/enrollments': '/api/v1/enrollments/',
            },
            'app_home': '/api/v1/users/',
        }
        
        return Response({
            'message': 'Welcome to the Student Management API Gateway',
            'api_documentation': api_documentation,
            'api_modules': api_modules,
            'authentication': {
                'token_obtain': '/api/token/',
                'token_refresh': '/api/token/refresh/',
                'token_verify': '/api/token/verify/',
            }
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint.
    """
    return Response({
        'status': 'ok',
        'message': 'Service is running'
    }, status=status.HTTP_200_OK)

def index(request):
    """
    Index page.
    """
    return HttpResponse("Welcome to Student Management System API")


