"""
URL configuration for student_be project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin and Authentication
    path('admin/', admin.site.urls),
    path('auth/login/', include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),
    
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
 
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1 Endpoints
    path('api/v1/students/', include('api.app_student.urls')),
    path('api/v1/teachers/', include('api.app_teacher.urls')),
    path('api/v1/home/', include('api.app_home.urls')),
    path('api/v1/classes/', include('api.app_class.urls')),
    path('api/v1/scores/', include('api.app_score.urls')),
    path('api/v1/subjects/', include('api.app_subject.urls')),
    path('api/v1/enrollments/', include('api.app_enrollment.urls')),
    path('api/v1/activities/', include('api.app_activity.urls')),
    path('api/v1/semesters/', include('api.app_semester.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
