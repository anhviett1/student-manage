from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema

# Create your views here.

class APIGatewayView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        description="API Gateway root endpoint",
        responses={200: dict}
    )
    def get(self, request, format=None):
        api_documentation = {
            'documentation': '/api-gateway/docs/',
            'schema': '/api-gateway/schema/',
            'redoc': '/api-gateway/redoc/',
        }
        
        api_modules = {
            'app_academic': {
                'api/students': '/api-gateway/app_academic/api_students_v1/',
                'api/teachers': '/api-gateway/app_academic/api_teachers_v1/',
                'api/subjects': '/api-gateway/app_academic/api_subjects_v1/',
            },
            'app_education': {
                'api/classes': '/api-gateway/app_education/api_classes_v1/',
                'api/scores': '/api-gateway/app_education/api_scores_v1/',
            },
            'app_business': {
                'api/enrollments': '/api-gateway/app_business/api_enrollments_v1/',
            },
            'app_home': '/api-gateway/app_home/',
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
