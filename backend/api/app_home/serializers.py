from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(source='department', queryset=User._meta.get_field('department').related_model.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'is_active', 'is_deleted', 'is_superuser', 'is_staff',
            'created_at', 'updated_at', 'last_login', 'last_login_ip',
            'profile_picture', 'phone_number', 'emergency_contact',
            'emergency_phone', 'address', 'department', 'department_id',
        ]
        read_only_fields = ['id', 'is_superuser', 'is_staff', 'created_at', 'updated_at', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Ưu tiên quyền cao nhất
        if instance.is_superuser:
            data['role'] = 'admin'
        elif instance.is_staff:
            data['role'] = 'staff'
        # Nếu không thì giữ nguyên role gốc
        return data