from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Activity
from .serializers import ActivitySerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(tags=['Activities']),
    retrieve=extend_schema(tags=['Activities']),
)
class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing activity logs.
    This is a read-only viewset as activities should only be created by the system.
    """
    queryset = Activity.objects.all().order_by('-created_at')
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        This view returns activities for the current user unless the user is staff/admin.
        Staff/admin users can see all activities.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Activity.objects.all().order_by('-created_at')
        return Activity.objects.filter(user=user).order_by('-created_at')
