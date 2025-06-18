from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Activity
from .serializers import ActivitySerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(tags=["Activities"]),
    retrieve=extend_schema(tags=["Activities"]),
)
class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all().order_by("-created_at")
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Activity.objects.all().order_by("-created_at")
        return Activity.objects.filter(user=user).order_by("-created_at")
