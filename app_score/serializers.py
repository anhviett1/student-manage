from rest_framework import serializers
from .models import Score
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name='ScoreSerializer')
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
        
@extend_schema_serializer(component_name='ScoreCreateSerializer')
class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['student', 'subject', 'semester', 'midterm_score', 'final_score', 'notes']
        
@extend_schema_serializer(component_name='ScoreDetailSerializer')
class ScoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
        depth = 1