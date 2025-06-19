from rest_framework import serializers
from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source="student.name")
    subject_name = serializers.ReadOnlyField(source="subject.name")
    semester_name = serializers.ReadOnlyField(source="semester.name")
    class_name = serializers.ReadOnlyField(source="class_obj.name")

    class Meta:
        model = Enrollment
        fields = [
            "student_name",
            "subject_name",
            "semester_name",
            "class_name",
        ]
        read_only_fields = ["created_at", "updated_at"]