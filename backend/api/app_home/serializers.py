from rest_framework import serializers
from .models import User, Department
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer cho thay đổi mật khẩu"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message=_('Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ cái và số.')
            )
        ]
    )

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_('Mật khẩu cũ không đúng.'))
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer cho cập nhật hồ sơ người dùng"""
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone_number', 'emergency_contact', 'emergency_phone',
            'address', 'role', 'profile_picture', 'department'
        ]
        read_only_fields = ['username', 'role']

class UserSerializer(serializers.ModelSerializer):
    """Serializer cho User"""
    password = serializers.CharField(write_only=True, required=False)
    department_name = serializers.CharField(source='department.name', read_only=True, default=None)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'role', 'phone_number', 'emergency_contact', 'emergency_phone',
            'address', 'profile_picture', 'department', 'department_name',
            'is_active', 'last_login_ip', 'password'
        ]
        read_only_fields = [
            'is_active', 'last_login_ip', 'department_name'
        ]

    def validate_role(self, value):
        if value not in dict(User.ROLE_CHOICES).keys():
            raise serializers.ValidationError(_('Vai trò không hợp lệ.'))
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(_('Email đã được sử dụng.'))
        return value

    def validate_phone_number(self, value):
        if value:
            if not value.isdigit():
                raise serializers.ValidationError(_('Số điện thoại chỉ được chứa số.'))
            if len(value) < 10 or len(value) > 15:
                raise serializers.ValidationError(_('Số điện thoại phải có từ 10 đến 15 số.'))
        return value

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer cho Department"""
    class Meta:
        model = Department
        fields = [
            'name', 'code', 'description', 'is_active'
        ]
        read_only_fields = ['is_active']

    def validate_name(self, value):
        if Department.objects.filter(name=value.lower()).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(_('Tên khoa đã tồn tại.'))
        return value

    def validate_code(self, value):
        if value and Department.objects.filter(code=value.lower()).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(_('Mã khoa đã tồn tại.'))
        return value