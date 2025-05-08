from rest_framework import serializers
from .models import Score

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
        
class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        exclude = ['created_at', 'updated_at']
        
class ScoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
        depth = 1