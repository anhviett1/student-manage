from django import forms
from .models import Student
from app_home.models import Department

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'department',
            'major',
            'minor',
            'status',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relationship',
            'blood_type',
            'medical_conditions',
            'allergies',
            'profile_picture',
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
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'department': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Chọn khoa'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Chọn trạng thái'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Chọn giới tính'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm class form-control cho tất cả các trường
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
        
        # Cập nhật queryset cho department
        self.fields['department'].queryset = Department.objects.all()

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

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name and last_name:
            if len(first_name) < 2 or len(last_name) < 2:
                raise forms.ValidationError('Tên và họ phải có ít nhất 2 ký tự')

        return cleaned_data 