from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TeacherViewSet,
    TeacherListView,
    TeacherDetailView,
    TeacherCreateView,
    TeacherUpdateView,
    TeacherDeleteView
)

router = DefaultRouter()
router.register(r'', TeacherViewSet)

app_name = 'teachers'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', TeacherListView.as_view(), name='teacher_list'),
    path('create/', TeacherCreateView.as_view(), name='teacher_create'),
    path('<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('<int:pk>/edit/', TeacherUpdateView.as_view(), name='teacher_edit'),
    path('<int:pk>/delete/', TeacherDeleteView.as_view(), name='teacher_delete'),
] 