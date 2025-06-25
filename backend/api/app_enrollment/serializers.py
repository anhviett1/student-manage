from rest_framework import serializers
from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
           "enrollment_id",
            "course",
            "semester",
            "class_obj"
            "student",
            "status",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["enrollment_id", "created_at", "updated_at"]
