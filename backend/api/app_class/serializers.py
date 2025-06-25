from rest_framework import serializers
from .models import Class

class ClassSerializer(serializers.ModelSerializer):
    
    semester_name = serializers.CharField(source="semester.name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.name", read_only=True)

    class Meta:
        model = Class
        fields = [
            "class_id",
            "class_name",
            "description",
            "department",
            "credits",
            "status",
            "is_active",
            "is_deleted",
            "semester",
            "semester_name",
            "subject",
            "subject_name",
            "teacher",
            "teacher_name",
            "teachers",
            "subjects",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["class_id", "created_at", "updated_at"]