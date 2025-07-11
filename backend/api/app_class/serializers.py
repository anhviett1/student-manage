from rest_framework import serializers
from .models import Class


class ClassSerializer(serializers.ModelSerializer):

    semester_name = serializers.CharField(source="semester.name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.name", read_only=True)

    class Meta:
        model = Class
        fields = "__all__"
        read_only_fields = ["class_id", "created_at", "updated_at"]
