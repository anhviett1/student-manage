from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AvatarUploadView, LogoutAPIView, ProfileAPIView,
    ChangePasswordAPIView, UserViewSet,
    StatisticsAPIView, UserExportAPIView,
    ScoreManagementAPIView  
)


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),  
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
    path("avatar/", AvatarUploadView.as_view(), name="avatar-upload"),
    path("statistics/", StatisticsAPIView.as_view(), name="statistics"),
    path("export/", UserExportAPIView.as_view(), name="user-export"),
    path("score-management/", ScoreManagementAPIView.as_view(), name="score-management"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
