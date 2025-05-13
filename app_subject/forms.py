from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = [
            'subject_id',
            'name',
            'description',
            'credits',
            'faculty',
            'status',
            'is_active'
        ]
        widgets = {
            'subject_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mã môn học'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên môn học'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mô tả',
                'rows': 3
            }),
            'credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
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

    def clean_subject_id(self):
        subject_id = self.cleaned_data.get('subject_id')
        if not subject_id:
            raise forms.ValidationError('Mã môn học không được để trống')
        
        # Kiểm tra định dạng mã môn học (ví dụ: MH001)
        if not subject_id.startswith('MH'):
            raise forms.ValidationError('Mã môn học phải bắt đầu bằng "MH"')
            
        # Kiểm tra trùng lặp
        if Subject.objects.filter(subject_id=subject_id).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Mã môn học đã tồn tại')
            
        return subject_id

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Tên môn học không được để trống')
            
        if len(name) < 3:
            raise forms.ValidationError('Tên môn học phải có ít nhất 3 ký tự')
            
        return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm class form-control cho tất cả các trường
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'