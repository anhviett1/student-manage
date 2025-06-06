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
    path('change-password/', change_password, name='change_password'), 
    path('profile/', profile_view, name='profile'),    
    path('', include(router.urls)),

]  