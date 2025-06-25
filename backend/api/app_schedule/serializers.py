from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [         
            "schedule_id",  
            "day_of_week",
            "start_time",
            "end_time",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["schedule_id", "created_at", "updated_at"]