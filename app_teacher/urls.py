from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet

router = DefaultRouter()
router.register(r'', TeacherViewSet)

app_name = 'teachers'

urlpatterns = [
    path('', include(router.urls)),
] 