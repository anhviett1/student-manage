from django.urls import path
from .views import HomeAPIView, home_view, dashboard_view

app_name = 'home'

urlpatterns = [
    path('', HomeAPIView.as_view(), name='home-api'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('main/', home_view, name='home'),
] 