from rest_framework import serializers
from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
        read_only_fields = ["student", "score", "grade", "created_at", "updated_at"]