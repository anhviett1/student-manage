from rest_framework import serializers
from .models import Semester


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            "semester_id",
            "name",
            "start_date",
            "end_date",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["semester_id", "created_at", "updated_at"]