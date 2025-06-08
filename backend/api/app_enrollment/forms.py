from django import forms
from .models import Enrollment
from ..app_student.models import Student
from ..app_subject.models import Subject
from ..app_semester.models import Semester
from ..app_class.models import Class
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'student',
            'subject',
            'semester',
            'class_obj',
            'enrollment_date',
            'status',
            'is_active',
            'notes',
        ]
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Chọn sinh viên',
                'required': True,
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Chọn môn học',
                'required': True,
            }),
            'semester': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Chọn học kỳ',
                'required': True,
            }),
            'class_obj': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Chọn lớp',
                'required': True,
            }),
            'enrollment_date': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
                'placeholder': 'YYYY-MM-DD',
                'required': True,
            }),
            'status': forms.Select(choices=Enrollment.STATUS_CHOICES, attrs={
                'class': 'form-control',
                'required': True,
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập ghi chú (tùy chọn)',
                'rows': 4,
            }),
        }
        labels = {
            'student': _('Sinh viên'),
            'subject': _('Môn học'),
            'semester': _('Học kỳ'),
            'class_obj': _('Lớp'),
            'enrollment_date': _('Ngày đăng ký'),
            'status': _('Trạng thái'),
            'is_active': _('Đang hoạt động'),
            'notes': _('Ghi chú'),
        }
        error_messages = {
            'student': {'required': _('Vui lòng chọn sinh viên.')},
            'subject': {'required': _('Vui lòng chọn môn học.')},
            'semester': {'required': _('Vui lòng chọn học kỳ.')},
            'class_obj': {'required': _('Vui lòng chọn lớp.')},
            'enrollment_date': {'required': _('Vui lòng chọn ngày đăng ký.')},
            'status': {'required': _('Vui lòng chọn trạng thái.')},
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Lấy user từ kwargs để kiểm tra quyền
        super().__init__(*args, **kwargs)

        # Tối ưu hóa queryset cho các trường ForeignKey
        self.fields['student'].queryset = Student.objects.filter(is_active=True).order_by('name')
        self.fields['subject'].queryset = Subject.objects.filter(is_active=True).order_by('name')
        self.fields['semester'].queryset = Semester.objects.filter(is_active=True).order_by('-start_date')
        self.fields['class_obj'].queryset = Class.objects.filter(is_active=True).order_by('class_id')

        # Đặt giá trị mặc định nếu là form mới
        if not self.instance.pk:
            self.fields['enrollment_date'].initial = date.today()
            self.fields['status'].initial = 'pending'
            self.fields['is_active'].initial = True

        # Tùy chỉnh readonly cho người dùng không có quyền quản lý
        if self.user and not self.user.has_perm('app_enrollment.can_manage_enrollment'):
            for field in self.fields.values():
                field.widget.attrs['disabled'] = True

    def clean_enrollment_date(self):
        enrollment_date = self.cleaned_data.get('enrollment_date')
        if enrollment_date:
            if enrollment_date > date.today():
                raise ValidationError(_('Ngày đăng ký không được lớn hơn ngày hiện tại.'))
            if self.cleaned_data.get('semester'):
                semester = self.cleaned_data['semester']
                if enrollment_date < semester.registration_start or enrollment_date > semester.registration_end:
                    raise ValidationError(_('Ngày đăng ký phải nằm trong khoảng thời gian đăng ký của học kỳ.'))
        return enrollment_date

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        subject = cleaned_data.get('subject')
        semester = cleaned_data.get('semester')
        class_obj = cleaned_data.get('class_obj')
        status = cleaned_data.get('status')
        is_active = cleaned_data.get('is_active')

        # Kiểm tra unique_together
        if student and subject and semester:
            existing_enrollment = Enrollment.objects.filter(
                student=student,
                subject=subject,
                semester=semester,
            ).exclude(pk=self.instance.pk if self.instance else None)
            if existing_enrollment.exists():
                raise ValidationError(_('Sinh viên đã đăng ký môn học này trong học kỳ này.'))

        # Kiểm tra class_obj có thuộc subject và semester không
        if class_obj and subject and semester:
            if not Class.objects.filter(
                subject=subject,
                semester=semester,
                class_id=class_obj.class_id
            ).exists():
                raise ValidationError(_('Lớp không thuộc môn học hoặc học kỳ đã chọn.'))

        # Kiểm tra trạng thái và is_active
        if status == 'rejected' and is_active:
            raise ValidationError(_('Đăng ký bị từ chối không thể ở trạng thái hoạt động.'))

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