from rest_framework import serializers
from .models import Class


class ClassSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source="department.name")
    semester_name = serializers.ReadOnlyField(source="semester.name")
    subject_name = serializers.ReadOnlyField(source="subject.name")
    teacher_name = serializers.ReadOnlyField(source="teacher.full_name")
    teacher_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="teachers")
    subject_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="subjects")

    class Meta:
        model = Class
        fields = [f.name for f in Class._meta.fields] + [
            "department_name",
            "semester_name",
            "subject_name",
            "teacher_name",
            "teacher_ids",
            "subject_ids",
        ]
        read_only_fields = ["class_id", "created_at", "updated_at"]
