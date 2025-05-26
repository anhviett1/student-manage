from rest_framework import serializers
from .models import Subject
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name='SubjectSerializer')
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        
@extend_schema_serializer(component_name='SubjectCreateSerializer')
class SubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_id', 'name', 'description', 'credits']
        
@extend_schema_serializer(component_name='SubjectDetailSerializer')
class SubjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        depth = 1