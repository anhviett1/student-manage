from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AvatarUploadView,
    LoginAPIView,
    LogoutAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
    UserViewSet,
    UserRoleAPIView,
    AvatarUploadView,
    DepartmentViewSet
)

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")
router.register(r"", DepartmentViewSet, basename="departments")
urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("role/", UserRoleAPIView.as_view(), name="user-role"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
    path("avatar/", AvatarUploadView.as_view(), name="avatar-upload"),
]
