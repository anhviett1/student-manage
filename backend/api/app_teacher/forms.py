from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'teacher_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'date_of_birth',
            'gender',
           
            'degree',
            'specialization',
            'years_of_experience',
            'status',
            'is_active'
        ]
        widgets = {
            'teacher_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mã giảng viên'
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
          
            'degree': forms.Select(attrs={
                'class': 'form-control'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập chuyên ngành'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_teacher_id(self):
        teacher_id = self.cleaned_data.get('teacher_id')
        if not teacher_id:
            raise forms.ValidationError('Mã giảng viên không được để trống')
        
        # Kiểm tra định dạng mã giảng viên (ví dụ: GV001)
        if not teacher_id.startswith('GV'):
            raise forms.ValidationError('Mã giảng viên phải bắt đầu bằng "GV"')
            
        # Kiểm tra trùng lặp
        if Teacher.objects.filter(teacher_id=teacher_id).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Mã giảng viên đã tồn tại')
            
        return teacher_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email không được để trống')
            
        # Kiểm tra trùng lặp
        if Teacher.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
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