from rest_framework import serializers
from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "subject_id",
            "name",
            "credits",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["subject_id","name", "created_at", "updated_at"]