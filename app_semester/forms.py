from django import forms
from .models import Semester
from django.core.exceptions import ValidationError
from datetime import date

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = [
            'name', 'code', 'academic_year',
            'start_date', 'end_date',
            'registration_start', 'registration_end',
            'add_drop_deadline', 'status',
            'total_credits', 'min_credits', 'max_credits',
            'tuition_deadline', 'late_fee_start',
            'late_fee_amount', 'description', 'notes',
            'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên học kỳ'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mã học kỳ'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập năm học (ví dụ: 2023-2024)'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'registration_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'registration_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'add_drop_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tuition_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'late_fee_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'total_credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'late_fee_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Nhập mô tả học kỳ'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        registration_start = cleaned_data.get('registration_start')
        registration_end = cleaned_data.get('registration_end')
        add_drop_deadline = cleaned_data.get('add_drop_deadline')
        tuition_deadline = cleaned_data.get('tuition_deadline')
        late_fee_start = cleaned_data.get('late_fee_start')
        min_credits = cleaned_data.get('min_credits')
        max_credits = cleaned_data.get('max_credits')

        if start_date and end_date and start_date > end_date:
            raise ValidationError("Ngày kết thúc phải sau ngày bắt đầu")

        if registration_start and registration_end and registration_start >= registration_end:
            raise ValidationError("Ngày kết thúc đăng ký phải sau ngày bắt đầu đăng ký")

        if registration_end and start_date and registration_end >= start_date:
            raise ValidationError("Ngày kết thúc đăng ký phải trước ngày bắt đầu học kỳ")

        if add_drop_deadline and start_date and add_drop_deadline >= start_date:
            raise ValidationError("Hạn chót thêm/xóa môn phải trước ngày bắt đầu học kỳ")

        if tuition_deadline and start_date and tuition_deadline >= start_date:
            raise ValidationError("Hạn nộp học phí phải trước ngày bắt đầu học kỳ")

        if late_fee_start and tuition_deadline and late_fee_start <= tuition_deadline:
            raise ValidationError("Ngày bắt đầu tính phí trễ phải sau hạn nộp học phí")

        if min_credits and max_credits and min_credits > max_credits:
            raise ValidationError("Số tín chỉ tối thiểu không được lớn hơn số tín chỉ tối đa")

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError('Tên học kỳ phải có ít nhất 3 ký tự')
        return name

    def clean_academic_year(self):
        academic_year = self.cleaned_data.get('academic_year')
        try:
            start_year, end_year = map(int, academic_year.split('-'))
            if end_year != start_year + 1:
                raise ValidationError("Năm học phải có định dạng YYYY-YYYY (ví dụ: 2023-2024)")
        except (ValueError, AttributeError):
            raise ValidationError("Năm học không hợp lệ")
        return academic_year 