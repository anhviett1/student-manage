from rest_framework import serializers
from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source="student.name")
    subject_name = serializers.ReadOnlyField(source="subject.name")
    semester_name = serializers.ReadOnlyField(source="semester.name")

    class Meta:
        model = Score
        fields = [
            "student_name",
            "subject_name",
            "semester_name",
        ]
        read_only_fields = ["created_at", "updated_at", "total_score"]