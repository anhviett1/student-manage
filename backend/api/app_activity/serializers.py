from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    activity_type_display = serializers.CharField(
        source="get_activity_type_display", read_only=True
    )

    class Meta:
        model = Activity
        fields = [
            "id",
            "user",
            "user_username",
            "activity_type",
            "activity_type_display",
            "content_type",
            "object_id",
            "description",
            "ip_address",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]
