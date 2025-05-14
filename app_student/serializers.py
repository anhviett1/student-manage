from rest_framework import serializers
from .models import Student
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name='StudentSerializer')
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
@extend_schema_serializer(component_name='StudentCreateSerializer')
class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'faculty']
        
@extend_schema_serializer(component_name='StudentDetailSerializer')
class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 1