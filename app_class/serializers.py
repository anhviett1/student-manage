from rest_framework import serializers
from .models import Class

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        
class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        
class ClassDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        depth = 1