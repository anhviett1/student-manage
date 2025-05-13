from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'date_of_birth',
            'gender',
            'faculty',
            'status',
            'is_active'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mã sinh viên'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập họ'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập số điện thoại'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập địa chỉ',
                'rows': 3
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if not student_id:
            raise forms.ValidationError('Mã sinh viên không được để trống')
        
        # Kiểm tra định dạng mã sinh viên (ví dụ: SV001)
        if not student_id.startswith('SV'):
            raise forms.ValidationError('Mã sinh viên phải bắt đầu bằng "SV"')
            
        # Kiểm tra trùng lặp
        if Student.objects.filter(student_id=student_id).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Mã sinh viên đã tồn tại')
            
        return student_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email không được để trống')
            
        # Kiểm tra trùng lặp
        if Student.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Email đã tồn tại')
            
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm class form-control cho tất cả các trường
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name and last_name:
            if len(first_name) < 2 or len(last_name) < 2:
                raise forms.ValidationError('Tên và họ phải có ít nhất 2 ký tự')

        return cleaned_data 