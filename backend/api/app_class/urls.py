from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClassViewSet,
    ClassListView,
    ClassDetailView,
    ClassCreateView,
    ClassUpdateView,
    ClassDeleteView
)

router = DefaultRouter()
router.register(r'', ClassViewSet)

app_name = 'classes'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', ClassListView.as_view(), name='class_list'),
    path('create/', ClassCreateView.as_view(), name='class_create'),
    path('<int:pk>/', ClassDetailView.as_view(), name='class_detail'),
    path('<int:pk>/edit/', ClassUpdateView.as_view(), name='class_edit'),
    path('<int:pk>/delete/', ClassDeleteView.as_view(), name='class_delete'),
] 