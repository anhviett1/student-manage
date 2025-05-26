from rest_framework import serializers
from .models import Semester
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name='SemesterSerializer')
class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'semester_id', 'name', 'academic_year', 
            'start_date', 'end_date', 'status', 'is_active'
        ]

@extend_schema_serializer(component_name='SemesterDetailSerializer')
class SemesterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'
        depth = 1 