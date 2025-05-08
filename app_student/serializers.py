from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['created_at', 'updated_at', 'deleted_at', 'deleted_by', 'is_deleted']
        
class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 1