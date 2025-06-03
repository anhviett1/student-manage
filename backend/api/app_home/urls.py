from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeAPIView,
    home_view,
    dashboard_view,
    login_view,
    logout_view,
    profile_view,
    change_password,
    home,
    home_be_view,
    UserViewSet
)

app_name = 'app_home'

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # API endpoints
    path('api/', HomeAPIView.as_view(), name='home-api'),
    
    # Authentication
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password, name='change_password'),
    
    # Main views
    path('', home_view, name='home'),
    path('home_be', home_be_view, name='home_be'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('main/', home, name='main'),
    path('profile/', profile_view, name='profile'),
    
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
] 