from rest_framework import serializers
from .models import Class
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name='ClassSerializer')
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        
@extend_schema_serializer(component_name='ClassCreateSerializer')
class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['class_id', 'name', 'description', 'faculty', 'semester', 'subject', 'teacher']
        
@extend_schema_serializer(component_name='ClassDetailSerializer')
class ClassDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        depth = 1