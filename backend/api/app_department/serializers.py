from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "department_id",
            "department_name",
            "description",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["department_id", "created_at", "updated_at"]

    