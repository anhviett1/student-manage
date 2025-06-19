from rest_framework import serializers
from .models import Student
from drf_spectacular.utils import extend_schema_field


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    department_name = serializers.ReadOnlyField(source="department.name")
    class_assigned_names = serializers.SerializerMethodField()
    subject_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="subjects")
    score_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="scores")


    class Meta:
        model = Student
        fields = [
            "username",
            "department_name",
            "class_assigned_names",
            "subject_ids",
            "score_ids",
        ]
        read_only_fields = ["student_id", "created_at", "updated_at", "deleted_at", "gpa"]