from rest_framework import serializers

from ..app_class.models import Class
from ..app_semester.models import Semester
from ..app_student.models import Student
from ..app_subject.models import Subject
from ..app_enrollment.models import Enrollment
from ..app_student.serializers import StudentSerializer
from ..app_subject.serializers import SubjectSerializer
from ..app_semester.serializers import SemesterSerializer
from ..app_class.serializers import ClassSerializer
from django.utils import timezone
from rest_framework.exceptions import ValidationError

class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    semester = SemesterSerializer(read_only=True)
    class_obj = ClassSerializer(read_only=True)
    
    student_id = serializers.PrimaryKeyRelatedField(
        source='student', queryset=Student.objects.all(), write_only=True, required=True
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        source='subject', queryset=Subject.objects.all(), write_only=True, required=True
    )
    semester_id = serializers.PrimaryKeyRelatedField(
        source='semester', queryset=Semester.objects.all(), write_only=True, required=True
    )
    class_id = serializers.PrimaryKeyRelatedField(
        source='class_obj', queryset=Class.objects.all(), write_only=True, required=True
    )

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_id', 'subject', 'subject_id', 'semester', 'semester_id',
            'class_obj', 'class_id', 'enrollment_date', 'status', 'is_active', 'notes',
            'created_at', 'updated_at', 'created_by', 'updated_by', 'is_deleted'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by', 'is_deleted']

    def validate(self, data):
        # Ensure enrollment_date is not in the future
        if data.get('enrollment_date') and data['enrollment_date'] > timezone.now().date():
            raise ValidationError({'enrollment_date': 'Ngày đăng ký không được là ngày trong tương lai.'})

        # Check unique_together constraint
        student = data.get('student')
        subject = data.get('subject')
        semester = data.get('semester')
        instance = self.instance

        if Enrollment.objects.filter(
            student=student, subject=subject, semester=semester
        ).exclude(id=instance.id if instance else None).exists():
            raise ValidationError('Sinh viên đã đăng ký môn học này trong học kỳ này.')

        # Ensure status is valid for is_active
        if data.get('status') == 'rejected' and data.get('is_active', True):
            raise ValidationError({'is_active': 'Đăng ký bị từ chối không thể ở trạng thái hoạt động.'})

        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)