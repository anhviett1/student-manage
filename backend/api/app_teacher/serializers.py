from rest_framework import serializers
from .models import Teacher
from ..app_home.models import Department
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class TeacherSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        source='department', queryset=Department.objects.all(), write_only=True, required=True
    )
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    deleted_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    full_name = serializers.CharField(read_only=True, source='get_full_name')

    class Meta:
        model = Teacher
        fields = [
            'teacher_id', 'user', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'address', 'degree', 'specialization',
            'years_of_experience', 'profile_picture', 'bio', 'status', 'is_active',
            'created_at', 'updated_at', 'created_by', 'updated_by', 'is_deleted',
            'deleted_at', 'deleted_by', 'department', 'department_id', 'full_name',
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'created_by', 'updated_by', 'is_deleted',
            'deleted_at', 'deleted_by'
        ]

    def validate_teacher_id(self, value):
        if not value.startswith('GV'):
            raise serializers.ValidationError(_('Mã giảng viên phải bắt đầu bằng "GV".'))
        if Teacher.objects.filter(teacher_id=value).exclude(teacher_id=self.instance.teacher_id if self.instance else None).exists():
            raise serializers.ValidationError(_('Mã giảng viên đã tồn tại.'))
        return value

    def validate_email(self, value):
        if Teacher.objects.filter(email=value).exclude(teacher_id=self.instance.teacher_id if self.instance else None).exists():
            raise serializers.ValidationError(_('Email này đã được sử dụng.'))
        return value

    def validate_phone(self, value):
        if value:
            phone_validator = RegexValidator(
                regex=r'^\+?[0-9]{10,15}$',
                message=_('Số điện thoại phải có từ 10-15 chữ số.')
            )
            phone_validator(value)
        if Teacher.objects.filter(phone=value).exclude(teacher_id=self.instance.teacher_id if self.instance else None).exists():
            raise serializers.ValidationError(_('Số điện thoại này đã được sử dụng.'))
        return value

    def validate_date_of_birth(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(_('Ngày sinh không được là ngày trong tương lai.'))
        return value

    def validate_years_of_experience(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(_('Số năm kinh nghiệm phải từ 0 đến 100.'))
        return value

    def validate(self, data):
        if data.get('status') in ['retired', 'inactive'] and data.get('is_active', True):
            raise serializers.ValidationError(_('Giảng viên đã nghỉ hưu hoặc tạm nghỉ không thể ở trạng thái hoạt động.'))
        return data