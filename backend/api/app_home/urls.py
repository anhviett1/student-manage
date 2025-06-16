from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginAPIView, LogoutAPIView, ProfileAPIView, 
    ChangePasswordAPIView, UserViewSet, UserRoleAPIView,
    AvatarUploadView
)

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('auth/role/', UserRoleAPIView.as_view(), name='user-role'),
    path('auth/profile/', ProfileAPIView.as_view(), name='profile'),
    path('auth/change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('auth/avatar/', AvatarUploadView.as_view(), name='avatar-upload'),
]