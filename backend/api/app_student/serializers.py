from rest_framework import serializers
from .models import Student
from drf_spectacular.utils import extend_schema_serializer
from app_home.serializers import DepartmentSerializer

@extend_schema_serializer(component_name='StudentSerializer')
class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'department']
        
@extend_schema_serializer(component_name='StudentCreateSerializer')
class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'department']
        
@extend_schema_serializer(component_name='StudentDetailSerializer')
class StudentDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'
        depth = 1