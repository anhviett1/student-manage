from rest_framework import serializers
from .models import Semester


class SemesterSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    class Meta:
        model = Semester
        fields = [
            "semester_id",
            "name",
            "academic_year",
            "start_date",
            "end_date",
            "registration_start",
            "registration_end",
            "add_drop_deadline",
            "status",
            "status_display",
            "total_credits",
            "min_credits",
            "max_credits",
            "tuition_deadline",
            "late_fee_start",
            "late_fee_amount",
            "description",
            "notes",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "semester_id",
            "created_at",
            "updated_at",
            "status_display",
        ]