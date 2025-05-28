from django import forms
from .models import Score
from ..app_student.models import Student
from ..app_subject.models import Subject
from ..app_semester.models import Semester
from django.core.exceptions import ValidationError

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = [
            'student',
            'subject',
            'semester',
            'midterm_score',
            'final_score',
            'notes',
            'status',
            'is_active'
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
            'midterm_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập điểm giữa kỳ',
                'min': '0',
                'max': '10',
                'step': '0.1'
            }),
            'final_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập điểm cuối kỳ',
                'min': '0',
                'max': '10',
                'step': '0.1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập ghi chú',
                'rows': 3
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_midterm_score(self):
        score = self.cleaned_data.get('midterm_score')
        if score is not None:
            if score < 0 or score > 10:
                raise ValidationError('Điểm giữa kỳ phải từ 0 đến 10')
        return score

    def clean_final_score(self):
        score = self.cleaned_data.get('final_score')
        if score is not None:
            if score < 0 or score > 10:
                raise ValidationError('Điểm cuối kỳ phải từ 0 đến 10')
        return score

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        subject = cleaned_data.get('subject')
        semester = cleaned_data.get('semester')

        if student and subject and semester:
            # Kiểm tra xem sinh viên đã có điểm cho môn học này trong học kỳ này chưa
            if Score.objects.filter(
                student=student,
                subject=subject,
                semester=semester
            ).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationError('Sinh viên đã có điểm cho môn học này trong học kỳ này')

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