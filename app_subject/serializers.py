from rest_framework import serializers
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        
class SubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ['created_at', 'updated_at']
        
class SubjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        depth = 1