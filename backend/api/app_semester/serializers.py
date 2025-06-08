from rest_framework import serializers
from ..app_semester.models import Semester
from django.utils.translation import gettext_lazy as _

class SemesterSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    deleted_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Semester
        fields = [
            'semester_id', 'name',
            'academic_year', 'start_date',
            'end_date', 'registration_start',
            'registration_end', 'add_drop_deadline',
            'status', 'total_credits',
            'min_credits', 'max_credits',
            'tuition_deadline', 'late_fee_start',
            'late_fee_amount', 'description',
            'notes', 'is_active',
            'created_at', 'updated_at',
            'is_deleted', 'deleted_at',
            'created_by', 'updated_by',
            'deleted_by'
        ]
        read_only_fields = [
            'created_at', 'updated_at',
            'is_deleted', 'deleted_at',
            'created_by', 'updated_by',
            'deleted_by'
        ]

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        registration_start = data.get('registration_start')
        registration_end = data.get('registration_end')
        tuition_deadline = data.get('tuition_deadline')
        late_fee_start = data.get('late_fee_start')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(_('start_date must be before end_date'))
        if registration_start and registration_end and registration_start > registration_end:
            raise serializers.ValidationError(_('Ngày bắt đầu đăng ký phải trước ngày kết thúc đăng ký.'))
        if tuition_deadline and late_fee_start and tuition_deadline > late_fee_start:
            raise serializers.ValidationError(_('Hạn nộp học phí phải trước ngày bắt đầu tính phí trễ.'))
        if data.get('status') == 'current' and not data.get('is_active'):
            raise serializers.ValidationError(_('Học kỳ hiện tại phải có trạng thái is_active là True.'))
        if data.get('min_credits') > data.get('max_credits'):
            raise serializers.ValidationError(_('Số tín chỉ tối thiểu không được vượt quá số tín chỉ tối đa.'))
        return data