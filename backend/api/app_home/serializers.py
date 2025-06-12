from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Department

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    password = serializers.CharField(write_only=True, required=False)  # Optional for updates
    role = serializers.ChoiceField(choices=['student', 'teacher', 'admin'], required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def validate_role(self, value):
        """Restrict role changes to valid choices."""
        if self.context['request'].user.role != 'admin' and value != self.instance.role:
            raise serializers.ValidationError("Chỉ admin có thể thay đổi vai trò.")
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile updates."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id', 'username', 'role']

    def to_representation(self, instance):
        """Override to ensure superuser role is 'admin' for frontend."""
        ret = super().to_representation(instance)
        if instance.is_superuser:
            ret['role'] = 'admin'
        return ret

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password."""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({'old_password': 'Mật khẩu cũ không đúng'})
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({'new_password': 'Mật khẩu mới phải khác mật khẩu cũ'})
        return data

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']