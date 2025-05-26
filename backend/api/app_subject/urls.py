from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubjectViewSet,
    SubjectListView,
    SubjectDetailView,
    SubjectCreateView,
    SubjectUpdateView,
    SubjectDeleteView
)

router = DefaultRouter()
router.register(r'', SubjectViewSet)

app_name = 'subjects'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', SubjectListView.as_view(), name='subject_list'),
    path('create/', SubjectCreateView.as_view(), name='subject_create'),
    path('<int:pk>/', SubjectDetailView.as_view(), name='subject_detail'),
    path('<int:pk>/edit/', SubjectUpdateView.as_view(), name='subject_edit'),
    path('<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),
] 