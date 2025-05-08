from django.urls import path
from .views import HomeAPIView, home_view

app_name = 'home'

urlpatterns = [
    path('', HomeAPIView.as_view(), name='home-api'),
    path('dashboard/', home_view, name='dashboard'),
] 