from rest_framework import serializers
from .models import Student
from ..app_home.serializers import DepartmentSerializer
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name='StudentSerializer')
class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

@extend_schema_serializer(component_name='StudentCreateSerializer')
class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'phone', 'address', 'department', 'status']

@extend_schema_serializer(component_name='StudentDetailSerializer')
class StudentDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'first_name', 'last_name', 'email', 'phone', 'address', 'department', 'status', 'created_at', 'updated_at']