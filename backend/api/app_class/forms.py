from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Class
from ..app_teacher.models import Teacher
from ..app_semester.models import Semester
from ..app_subject.models import Subject
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
            'teacher',
        ]
        widgets = {
            'class_id': forms.TextInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'Nhập mã lớp (VD: L001)',
                'required': True,
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'Nhập tên lớp (VD: Lớp Toán Cao Cấp 1)',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'data-placeholder': 'Nhập mô tả lớp (tùy chọn)',
                'rows': 4,
            }),
            'status': forms.Select(choices=Class.STATUS_CHOICES, attrs={
                'class': 'form-control select2',
                'required': True,
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'semester': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Chọn học kỳ',
                'required': True,
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Chọn môn học',
                'required': True,
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Chọn giáo viên',
                'required': True,
            }),
        }
        labels = {
            'class_id': _('Mã lớp'),
            'name': _('Tên lớp'),
            'description': _('Mô tả'),
            'status': _('Trạng thái'),
            'is_active': _('Đang hoạt động'),
            'semester': _('Học kỳ'),
            'subject': _('Môn học'),
            'teacher': _('Giáo viên'),
        }
        error_messages = {
            'class_id': {
                'required': _('Vui lòng nhập mã lớp.'),
                'unique': _('Mã lớp đã tồn tại.'),
            },
            'name': {'required': _('Vui lòng nhập tên lớp.')},
            'semester': {'required': _('Vui lòng chọn học kỳ.')},
            'subject': {'required': _('Vui lòng chọn môn học.')},
            'teacher': {'required': _('Vui lòng chọn giáo viên.')},
            'status': {'required': _('Vui lòng chọn trạng thái.')},
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Lấy user từ kwargs để kiểm tra quyền
        super().__init__(*args, **kwargs)

        # Tối ưu hóa queryset cho các trường ForeignKey
        self.fields['semester'].queryset = Semester.objects.filter(is_active=True).order_by('-start_date')
        self.fields['subject'].queryset = Subject.objects.filter(is_active=True).order_by('name')
        self.fields['teacher'].queryset = Teacher.objects.filter(is_active=True).order_by('name')

        # Đặt giá trị mặc định nếu là form mới
        if not self.instance.pk:
            self.fields['status'].initial = 'active'
            self.fields['is_active'].initial = True

        # Tùy chỉnh quyền: Vô hiệu hóa form nếu không có quyền quản lý
        if self.user and not self.user.has_perm('app_class.can_manage_class'):
            for field in self.fields.values():
                field.widget.attrs['disabled'] = True

        # Tùy chỉnh subject dựa trên teacher nếu là giáo viên
        if self.user and self.user.has_perm('app_teacher.can_teach'):
            try:
                teacher = Teacher.objects.get(user=self.user)
                self.fields['subject'].queryset = Subject.objects.filter(teacher=teacher, is_active=True).order_by('name')
                if not self.instance.pk:
                    self.fields['teacher'].initial = teacher.teacher_id
                    self.fields['teacher'].widget.attrs['disabled'] = True
            except Teacher.DoesNotExist:
                pass

    def clean_class_id(self):
        class_id = self.cleaned_data.get('class_id')
        if not class_id:
            raise ValidationError(_('Mã lớp không được để trống.'))

        # Kiểm tra định dạng mã lớp: Bắt đầu bằng 'L', theo sau là số
        if not class_id.startswith('L') or not class_id[1:].isdigit():
            raise ValidationError(_('Mã lớp phải bắt đầu bằng "L" và theo sau là số (VD: L001).'))

        # Kiểm tra độ dài
        if len(class_id) < 4 or len(class_id) > 10:
            raise ValidationError(_('Mã lớp phải có độ dài từ 4 đến 10 ký tự.'))

        # Kiểm tra trùng lặp
        if Class.objects.filter(class_id=class_id).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError(_('Mã lớp đã tồn tại.'))

        return class_id

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError(_('Tên lớp không được để trống.'))

        # Kiểm tra độ dài
        if len(name) < 3 or len(name) > 100:
            raise ValidationError(_('Tên lớp phải có độ dài từ 3 đến 100 ký tự.'))

        return name

    def clean(self):
        cleaned_data = super().clean()
        semester = cleaned_data.get('semester')
        subject = cleaned_data.get('subject')
        teacher = cleaned_data.get('teacher')
        status = cleaned_data.get('status')
        is_active = cleaned_data.get('is_active')

        # Kiểm tra teacher có được gán dạy subject không
        if teacher and subject:
            if not Subject.objects.filter(teacher=teacher, subject_id=subject.subject_id).exists():
                raise ValidationError(_('Giáo viên này không được gán dạy môn học đã chọn.'))

        # Kiểm tra tính hợp lệ của semester
        if semester:
            today = date.today()
            if semester.end_date < today and status == 'active':
                raise ValidationError(_('Không thể đặt trạng thái "Đang hoạt động" cho lớp thuộc học kỳ đã kết thúc.'))

        # Kiểm tra status và is_active
        if status == 'inactive' and is_active:
            raise ValidationError(_('Lớp không hoạt động không thể ở trạng thái "Đang hoạt động".'))

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            if not instance.pk:  # Tạo mới
                instance.created_by = self.user
            instance.updated_by = self.user
        if commit:
            instance.save()
        return instance