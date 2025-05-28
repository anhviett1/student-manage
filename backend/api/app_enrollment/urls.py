from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EnrollmentViewSet,
    EnrollmentListView,
    EnrollmentDetailView,
    EnrollmentCreateView,
    EnrollmentUpdateView,
    EnrollmentDeleteView,
)

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet)

app_name = 'app_enrollments'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', EnrollmentListView.as_view(), name='enrollment_list'),
    path('create/', EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('<int:pk>/edit/', EnrollmentUpdateView.as_view(), name='enrollment_edit'),
    path('<int:pk>/delete/', EnrollmentDeleteView.as_view(), name='enrollment_delete'),
] 