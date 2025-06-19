from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, DepartmentExportAPIView, DepartmentRestoreAPIView

router = DefaultRouter()
router.register(r"", DepartmentViewSet, basename="departments")

urlpatterns = [
    path("", include(router.urls)),
    path("departments/<int:pk>/restore/", DepartmentRestoreAPIView.as_view(), name="department-restore"),
    path("departments/export/", DepartmentExportAPIView.as_view(), name="department-export"),
]
