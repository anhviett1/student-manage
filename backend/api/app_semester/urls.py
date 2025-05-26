from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SemesterViewSet,
    SemesterListView,
    SemesterDetailView,
    SemesterCreateView,
    SemesterUpdateView,
    SemesterDeleteView,
)

router = DefaultRouter()
router.register(r'semesters', SemesterViewSet)

app_name = 'semesters'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', SemesterListView.as_view(), name='semester_list'),
    path('create/', SemesterCreateView.as_view(), name='semester_create'),
    path('<int:pk>/', SemesterDetailView.as_view(), name='semester_detail'),
    path('<int:pk>/edit/', SemesterUpdateView.as_view(), name='semester_edit'),
    path('<int:pk>/delete/', SemesterDeleteView.as_view(), name='semester_delete'),
] 