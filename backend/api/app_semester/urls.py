from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SemesterViewSet

router = DefaultRouter()
router.register(r"", SemesterViewSet, basename="semesters")

urlpatterns = [
    path("", include(router.urls)),
]
