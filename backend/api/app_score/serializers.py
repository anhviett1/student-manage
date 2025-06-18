from rest_framework import serializers
from ..app_score.models import Score
from ..app_student.models import Student
from ..app_subject.models import Subject
from ..app_semester.models import Semester
from django.utils.translation import gettext_lazy as _

class ScoreSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(
        slug_field='student_id',
        queryset=Student.objects.all(),
        required=True
    )
    subject = serializers.SlugRelatedField(
        slug_field='subject_id',
        queryset=Subject.objects.all(),
        required=True
    )
    semester = serializers.SlugRelatedField(
        slug_field='semester_id',
        queryset=Semester.objects.filter(is_active=True),
        required=True
    )
    created_by = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    updated_by = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Score
        fields = [
            'id', 'student', 'subject', 'semester', 'midterm_score', 'final_score', 'total_score',
            'notes', 'status', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_score', 'created_at', 'updated_at' ]

    def validate_midterm_score(self, value):
        if value is not None and (value < 0 or value > 10):
            raise serializers.ValidationError(_('Điểm giữa kỳ phải từ 0 đến 10.'))
        return value

    def validate_final_score(self, value):
        if value is not None and (value < 0 or value > 10):
            raise serializers.ValidationError(_('Điểm cuối kỳ phải từ 0 đến 10.'))
        return value

    def validate(self, data):
        if data.get('status') == 'active' and not data.get('is_active'):
            raise serializers.ValidationError(_('Điểm số đang hoạt động phải có trạng thái is_active là True.'))
        return data