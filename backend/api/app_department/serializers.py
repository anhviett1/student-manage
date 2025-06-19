from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.ReadOnlyField(source="head.name")
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "is_deleted",
            "head",
            "head_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


    