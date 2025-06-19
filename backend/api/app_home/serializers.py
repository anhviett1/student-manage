from rest_framework import serializers
from .models import User
from drf_spectacular.utils import extend_schema_field

class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source="department.name") 


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
        ]
        read_only_fields = ["id", "created_at", "updated_at", "last_login_ip"]
