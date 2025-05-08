from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from .views import APIGatewayView

router = DefaultRouter()
app_name = 'api_gateway'

urlpatterns = [
    path('', APIGatewayView.as_view(), name='api-gateway-root'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api_gateway:schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api_gateway:schema'), name='redoc'),
    
    # Module app_academic
    path('app_academic/', include([
        path('api/students/', include('app_student.urls', namespace='app_students')),
        path('api/teachers/', include('app_teacher.urls', namespace='app_teachers')),
        path('api/subjects/', include('app_subject.urls', namespace='app_subjects')),
    ])),
    
    # Module app_education
    path('app_education/', include([
        path('api/classes/', include('app_class.urls', namespace='app_classes')),
        path('api/scores/', include('app_score.urls', namespace='app_scores')),
    ])),
    
    # Module app_business
    path('app_business/', include([
        path('api/enrollments/', include('app_enrollment.urls', namespace='app_enrollments')),
    ])),
    
    # Home module
    path('app_home/', include('app_home.urls', namespace='app_home')),
]
