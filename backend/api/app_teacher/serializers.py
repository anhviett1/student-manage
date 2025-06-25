from rest_framework import serializers
from .models import Teacher
from drf_spectacular.utils import extend_schema_field


class TeacherSerializer(serializers.ModelSerializer):
    name =serializers.SerializerMethodField()
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() if obj.first_name and obj.last_name else ""
    class Meta:
        model = Teacher
        fields = [
            "teacher_id",
            "first_name",
            "last_name",
            "name",
            "email",
            "phone",
            "department",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["teacher_id", "created_at", "updated_at"]

    @extend_schema_field(serializers.CharField())
    def get_teacher_id(self, obj):
        return str(obj.teacher_id)