from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScoreViewSet,
    ScoreListView,
    ScoreCreateView,
    ScoreDetailView,
    ScoreUpdateView,
    ScoreDeleteView,
    

)

router = DefaultRouter()
router.register(r'scores', ScoreViewSet)

app_name = 'app_scores'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', ScoreListView.as_view(), name='score_list'),
    path('create/', ScoreCreateView.as_view(), name='score_create'),
    path('<int:pk>/', ScoreDetailView.as_view(), name='score_detail'),
    path('<int:pk>/edit/', ScoreUpdateView.as_view(), name='score_edit'),
    path('<int:pk>/delete/', ScoreDeleteView.as_view(), name='score_delete'),
] 