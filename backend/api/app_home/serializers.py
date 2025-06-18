from rest_framework import serializers
from .models import User, Department


class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source="department.name")
    full_name = serializers.ReadOnlyField(source="get_full_name")
    role_display = serializers.ReadOnlyField(source="get_role_display_name")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "created_at",
            "updated_at",
            "is_active",
            "is_deleted",
            "last_login_ip",
            "profile_picture",
            "phone_number",
            "emergency_contact",
            "emergency_phone",
            "address",
            "department",
            "department_name",
            "full_name",
            "role_display",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "last_login_ip"]


class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.ReadOnlyField(source="head.get_full_name")

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
