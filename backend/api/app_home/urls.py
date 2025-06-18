from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginAPIView, LogoutAPIView, ProfileAPIView, 
    ChangePasswordAPIView, UserViewSet, UserRoleAPIView,
    AvatarUploadView, DepartmentViewSet
)

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    #path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('role/', UserRoleAPIView.as_view(), name='user-role'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('avatar/', AvatarUploadView.as_view(), name='avatar-upload'),
    path('departments/', DepartmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='departments'),
]