from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeAPIView, LoginAPIView, LogoutAPIView, ProfileAPIView, ChangePasswordAPIView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', HomeAPIView.as_view(), name='home'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    #path('api/', include(router.urls)),
]

urlpatterns += router.urls