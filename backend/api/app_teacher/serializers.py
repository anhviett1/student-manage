from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    user_full_name = serializers.ReadOnlyField(source="user.get_full_name")
    department_name = serializers.ReadOnlyField(source="department.name")
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Teacher
        fields = [f.name for f in Teacher._meta.fields] + [
            "user_full_name",
            "department_name",
            "full_name",
        ]
        read_only_fields = ["teacher_id", "created_at", "updated_at"]
