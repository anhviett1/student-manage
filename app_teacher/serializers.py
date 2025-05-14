from rest_framework import serializers
from .models import Teacher
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name='TeacherSerializer')
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        
@extend_schema_serializer(component_name='TeacherCreateSerializer')
class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'first_name', 'last_name', 'email', 'specialization', 'faculty']
        
@extend_schema_serializer(component_name='TeacherDetailSerializer')
class TeacherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        depth = 1