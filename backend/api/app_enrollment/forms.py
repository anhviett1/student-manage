from django import forms
from .models import Enrollment
from ..app_student.models import Student
from ..app_subject.models import Subject
from ..app_semester.models import Semester
from django.core.exceptions import ValidationError
from datetime import date

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'student',
            'subject',
            'semester',
            'enrollment_date',
            'status',
            'is_active',
            'notes'
        ]
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Chọn sinh viên'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Chọn môn học'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Chọn học kỳ'
            }),
            'enrollment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Chọn ngày đăng ký'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập ghi chú',
                'rows': 3
            })
        }

    def clean_enrollment_date(self):
        enrollment_date = self.cleaned_data.get('enrollment_date')
        if enrollment_date:
            if enrollment_date > date.today():
                raise ValidationError('Ngày đăng ký không thể lớn hơn ngày hiện tại')
        return enrollment_date

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        subject = cleaned_data.get('subject')
        semester = cleaned_data.get('semester')

        if student and subject and semester:
            # Kiểm tra xem sinh viên đã đăng ký môn học này trong học kỳ này chưa
            if Enrollment.objects.filter(
                student=student,
                subject=subject,
                semester=semester
            ).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationError('Sinh viên đã đăng ký môn học này trong học kỳ này')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm class form-control cho tất cả các trường
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

        # Giới hạn danh sách sinh viên
        self.fields['student'].queryset = Student.objects.filter(is_active=True)

        # Giới hạn danh sách môn học
        self.fields['subject'].queryset = Subject.objects.filter(is_active=True)

        # Giới hạn danh sách học kỳ
        self.fields['semester'].queryset = Semester.objects.filter(is_active=True) 