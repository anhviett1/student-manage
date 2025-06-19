from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class_name = serializers.ReadOnlyField(source='class_assigned.name')
    teacher_name = serializers.ReadOnlyField(source='teacher.name')
    semester_name = serializers.ReadOnlyField(source='semester.name')
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Schedule
        fields = ['class_name', 'teacher_name', 'semester_name', 'department_name']
        read_only_fields = ['schedule_id', 'created_at', 'updated_at']