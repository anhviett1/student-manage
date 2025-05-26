from django import forms
from .models import Class
from app_teacher.models import Teacher
from app_semester.models import Semester
from app_subject.models import Subject
from django.core.exceptions import ValidationError
from datetime import date

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = [
            'class_id',
            'name',
            'description',
            'status',
            'is_active',
            'semester',
            'subject',
            'teacher'
        ]
        widgets = {
            'class_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mã lớp'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên lớp'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mô tả',
                'rows': 3
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-control'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control'
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_class_id(self):
        class_id = self.cleaned_data.get('class_id')
        if not class_id:
            raise forms.ValidationError('Mã lớp không được để trống')
        
        # Kiểm tra định dạng mã lớp (ví dụ: L001)
        if not class_id.startswith('L'):
            raise forms.ValidationError('Mã lớp phải bắt đầu bằng "L"')
            
        # Kiểm tra trùng lặp
        if Class.objects.filter(class_id=class_id).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Mã lớp đã tồn tại')
            
        return class_id

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Tên lớp không được để trống')
            
        if len(name) < 3:
            raise forms.ValidationError('Tên lớp phải có ít nhất 3 ký tự')
            
        return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm class form-control cho tất cả các trường
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

        # Giới hạn danh sách giáo viên (instructor)
        self.fields['teacher'].queryset = Teacher.objects.all()

        # Giới hạn danh sách học kỳ (semester)
        self.fields['semester'].queryset = Semester.objects.all()

        # Giới hạn danh sách môn học (subjects)
        if self.instance.teacher:
            # Nếu người dùng là giáo viên, chỉ hiển thị môn học mà họ phụ trách
            # Giả định Teacher có mối quan hệ với Subject
            self.fields['subject'].queryset = Subject.objects.filter(teacher=self.instance.teacher)
        else:
            # Nếu là admin, hiển thị tất cả môn học
            self.fields['subject'].queryset = Subject.objects.all()