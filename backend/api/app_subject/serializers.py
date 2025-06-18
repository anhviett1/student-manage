from rest_framework import serializers
from .models import Subject
from ..app_semester.models import Semester
from ..app_home.models import Department
from django.utils.translation import gettext_lazy as _

class SubjectSerializer(serializers.ModelSerializer):
    semester = serializers.SlugRelatedField(slug_field='name', read_only=True)
    semester_id = serializers.PrimaryKeyRelatedField(
        source='semester', queryset=Semester.objects.all(), write_only=True, required=False, allow_null=True
    )
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        source='department', queryset=Department.objects.all(), write_only=True, required=True
    )
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    deleted_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Subject
        fields = [
            'subject_id', 'name', 'description', 'credits', 'semester', 'semester_id',
            'department', 'department_id', 'status', 'is_active', 'created_at',
            'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'is_deleted', 'deleted_at'
        ]

    def validate_subject_id(self, value):
        if not value.startswith('MH'):
            raise serializers.ValidationError(_('Mã môn học phải bắt đầu bằng "MH".'))
        if Subject.objects.filter(subject_id=value).exclude(subject_id=self.instance.subject_id if self.instance else None).exists():
            raise serializers.ValidationError(_('Mã môn học đã tồn tại.'))
        return value

    def validate_name(self, value):
        if len(value) < 3 or len(value) > 200:
            raise serializers.ValidationError(_('Tên môn học phải từ 3 đến 200 ký tự.'))
        return value

    def validate_credits(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(_('Số tín chỉ phải từ 1 đến 10.'))
        return value

    def validate(self, data):
        if data.get('status') == 'inactive' and data.get('is_active', True):
            raise serializers.ValidationError(_('Môn học không hoạt động không thể ở trạng thái đang hoạt động.'))
        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)