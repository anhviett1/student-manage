from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = ["department_id", "created_at", "updated_at"]
