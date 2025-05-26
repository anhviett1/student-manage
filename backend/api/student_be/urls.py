from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('allauth.urls')),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('api-gateway/', include('api_gateway.urls', namespace='api_gateway')),
    
    # Web URLs
    path('', include('app_home.urls', namespace='home')),
    
    path('students/', include('app_student.urls', namespace='students')),
    path('teachers/', include('app_teacher.urls', namespace='teachers')),
    path('subjects/', include('app_subject.urls', namespace='subjects')),
    path('classes/', include('app_class.urls', namespace='classes')),
    path('scores/', include('app_score.urls', namespace='scores')),
    path('enrollments/', include('app_enrollment.urls', namespace='enrollments')),
    path('semesters/', include('app_semester.urls', namespace='semesters')),
    path('activities/', include('app_activity.urls', namespace='activities')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


