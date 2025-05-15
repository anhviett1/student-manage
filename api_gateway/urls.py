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
    
    # API endpoints grouped by app
    path('api/v1/students/', include('app_student.urls', namespace='app_students')),
    path('api/v1/teachers/', include('app_teacher.urls', namespace='app_teachers')),
    path('api/v1/subjects/', include('app_subject.urls', namespace='app_subjects')),
    path('api/v1/classes/', include('app_class.urls', namespace='app_classes')),
    path('api/v1/scores/', include('app_score.urls', namespace='app_scores')),
    path('api/v1/enrollments/', include('app_enrollment.urls', namespace='app_enrollments')),
    path('api/v1/home/', include('app_home.urls', namespace='app_home')),
    #path('api/v1/semesters/', include('app_semester.urls', namespace='app_semesters')),
    path('api/v1/semester/', include('app_semester.urls', namespace='app_semester')),
    path('api/v1/activities/', include('app_activity.urls', namespace='app_activities')),
]
