from rest_framework import serializers
from .models import Teacher
from drf_spectacular.utils import extend_schema_field


class TeacherSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source="user.name")
    department_name = serializers.ReadOnlyField(source="department.name")




    class Meta:
        model = Teacher
        fields = [
            "user_name",
            "department_name",

        ]
        read_only_fields = ["teacher_id", "created_at", "updated_at"]