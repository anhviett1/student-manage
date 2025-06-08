from rest_framework import serializers
from .models import Student
from ..app_home.models import Department
from ..app_class.models import Class
from ..app_subject.models import Subject
from ..app_score.models import Score
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class StudentSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        source='department', queryset=Department.objects.all(), write_only=True, required=True
    )
    class_assigned = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    class_assigned_ids = serializers.PrimaryKeyRelatedField(
        source='class_assigned', queryset=Class.objects.all(), many=True, write_only=True, required=False
    )
    subjects = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    subject_ids = serializers.PrimaryKeyRelatedField(
        source='subjects', queryset=Subject.objects.all(), many=True, write_only=True, required=False
    )
    scores = serializers.SlugRelatedField(many=True, slug_field='id', read_only=True)
    score_ids = serializers.PrimaryKeyRelatedField(
        source='scores', queryset=Score.objects.all(), many=True, write_only=True, required=False
    )
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    deleted_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    full_name = serializers.CharField(read_only=True, source='get_full_name')

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_id', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'is_active', 'address', 'city', 'state',
            'postal_code', 'country', 'enrollment_date', 'graduation_date', 'status',
            'major', 'minor', 'gpa', 'credits_earned', 'credits_attempted',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'profile_picture', 'student_id_card', 'blood_type', 'medical_conditions',
            'allergies', 'created_at', 'updated_at', 'deleted_at', 'deleted_by',
            'is_deleted', 'department', 'department_id', 'class_assigned', 'class_assigned_ids',
            'subjects', 'subject_ids', 'scores', 'score_ids', 'full_name',
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'deleted_at', 'deleted_by', 'is_deleted',
            'created_by', 'updated_by', 'gpa', 'credits_earned', 'credits_attempted'
        ]

    def validate_student_id(self, value):
        if not value.startswith('SV'):
            raise serializers.ValidationError(_('Mã sinh viên phải bắt đầu bằng "SV".'))
        if Student.objects.filter(student_id=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(_('Mã sinh viên đã tồn tại.'))
        return value

    def validate_student_id_card(self, value):
        if Student.objects.filter(student_id_card=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(_('Mã thẻ sinh viên đã tồn tại.'))
        return value

    def validate_email(self, value):
        if Student.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(_('Email này đã được sử dụng.'))
        return value

    def validate_phone(self, value):
        if value:
            phone_validator = RegexValidator(
                regex=r'^\+?[0-9]{10,15}$',
                message=_('Số điện thoại phải có từ 10-15 chữ số.')
            )
            phone_validator(value)
        return value

    def validate_emergency_contact_phone(self, value):
        if value:
            phone_validator = RegexValidator(
                regex=r'^\+?[0-9]{10,15}$',
                message=_('Số điện thoại khẩn cấp phải có từ 10-15 chữ số.')
            )
            phone_validator(value)
        return value

    def validate_date_of_birth(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(_('Ngày sinh không được là ngày trong tương lai.'))
        return value

    def validate_enrollment_date(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError(_('Ngày nhập học không được là ngày trong tương lai.'))
        return value

    def validate_graduation_date(self, value):
        enrollment_date = self.initial_data.get('enrollment_date') or (self.instance.enrollment_date if self.instance else None)
        if value and enrollment_date and value <= enrollment_date:
            raise serializers.ValidationError(_('Ngày tốt nghiệp phải sau ngày nhập học.'))
        return value

    def validate(self, data):
        if data.get('status') in ['graduated', 'withdrawn'] and data.get('is_active', True):
            raise serializers.ValidationError(_('Sinh viên đã tốt nghiệp hoặc rút lui không thể ở trạng thái hoạt động.'))
        return data