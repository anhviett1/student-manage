from rest_framework import serializers
from .models import User, Department

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [ 'username', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True}
        }

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'is_active']