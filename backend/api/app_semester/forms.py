from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Semester
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = [
            'name', 'academic_year', 'start_date', 'end_date',
            'registration_start', 'registration_end', 'add_drop_deadline',
            'status', 'total_credits', 'min_credits', 'max_credits',
            'tuition_deadline', 'late_fee_start', 'late_fee_amount',
            'description', 'notes', 'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'Nhập tên học kỳ (VD: HK1)',
                'required': True,
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'Nhập năm học (VD: 2023-2024)',
                'required': True,
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
                'required': True,
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
                'required': True,
            }),
            'registration_start': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
                'required': True,
            }),
            'registration_end': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
                'required': True,
            }),
            'add_drop_deadline': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
            }),
            'status': forms.Select(choices=Semester.STATUS_CHOICES, attrs={
                'class': 'form-control select2',
                'required': True,
            }),
            'total_credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1',
            }),
            'min_credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1',
            }),
            'max_credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1',
            }),
            'tuition_deadline': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
            }),
            'late_fee_start': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
            }),
            'late_fee_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1000',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'data-placeholder': 'Mô tả học kỳ (tùy chọn)',
                'rows': 4,
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'data-placeholder': 'Ghi chú (tùy chọn)',
                'rows': 4,
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'name': _('Tên học kỳ'),
            'academic_year': _('Năm học'),
            'start_date': _('Ngày bắt đầu'),
            'end_date': _('Ngày kết thúc'),
            'registration_start': _('Bắt đầu đăng ký'),
            'registration_end': _('Kết thúc đăng ký'),
            'add_drop_deadline': _('Hạn thêm/xóa môn'),
            'status': _('Trạng thái'),
            'total_credits': _('Tổng tín chỉ'),
            'min_credits': _('Tín chỉ tối thiểu'),
            'max_credits': _('Tín chỉ tối đa'),
            'tuition_deadline': _('Hạn nộp học phí'),
            'late_fee_start': _('Bắt đầu phí trễ'),
            'late_fee_amount': _('Số tiền phí trễ'),
            'description': _('Mô tả'),
            'notes': _('Ghi chú'),
            'is_active': _('Đang hoạt động'),
        }
        error_messages = {
            'name': {'required': _('Vui lòng nhập tên học kỳ.')},
            'academic_year': {'required': _('Vui lòng nhập năm học.')},
            'start_date': {'required': _('Vui lòng chọn ngày bắt đầu.')},
            'end_date': {'required': _('Vui lòng chọn ngày kết thúc.')},
            'registration_start': {'required': _('Vui lòng chọn ngày bắt đầu đăng ký.')},
            'registration_end': {'required': _('Vui lòng chọn ngày kết thúc đăng ký.')},
            'status': {'required': _('Vui lòng chọn trạng thái.')},
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Giá trị mặc định
        if not self.instance.pk:
            self.fields['status'].initial = 'upcoming'
            self.fields['is_active'].initial = True

        # Phân quyền
        if self.user and not self.user.has_perm('app_semester.can_manage_semester'):
            for field in self.fields.values():
                field.widget.attrs['disabled'] = True

        # Validator cho academic_year
        self.fields['academic_year'].validators.append(
            RegexValidator(
                regex=r'^\d{4}-\d{4}$',
                message=_('Năm học phải có định dạng YYYY-YYYY (VD: 2023-2024).'),
            )
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError(_('Tên học kỳ không được để trống.'))
        if len(name) < 3 or len(name) > 50:
            raise ValidationError(_('Tên học kỳ phải có từ 3 đến 50 ký tự.'))
        if Semester.objects.filter(name=name, academic_year=self.cleaned_data.get('academic_year')).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError(_('Học kỳ này đã tồn tại trong năm học.'))
        return name

    def clean_academic_year(self):
        academic_year = self.cleaned_data.get('academic_year')
        if not academic_year:
            raise ValidationError(_('Năm học không được để trống.'))
        try:
            start_year, end_year = map(int, academic_year.split('-'))
            if end_year != start_year + 1:
                raise ValidationError(_('Năm học phải có định dạng YYYY-(YYYY+1), VD: 2023-2024.'))
        except (ValueError, AttributeError):
            raise ValidationError(_('Năm học không hợp lệ.'))
        return academic_year

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
        total_credits = cleaned_data.get('total_credits')
        status = cleaned_data.get('status')
        is_active = cleaned_data.get('is_active')

        # Kiểm tra ngày
        if start_date and end_date and start_date >= end_date:
            raise ValidationError(_('Ngày kết thúc phải sau ngày bắt đầu.'))
        if registration_start and registration_end and registration_start >= registration_end:
            raise ValidationError(_('Ngày kết thúc đăng ký phải sau ngày bắt đầu đăng ký.'))
        if registration_end and start_date and registration_end >= start_date:
            raise ValidationError(_('Ngày kết thúc đăng ký phải trước ngày bắt đầu học kỳ.'))
        if add_drop_deadline and start_date and add_drop_deadline >= start_date:
            raise ValidationError(_('Hạn thêm/xóa môn phải trước ngày bắt đầu học kỳ.'))
        if tuition_deadline and start_date and tuition_deadline >= start_date:
            raise ValidationError(_('Hạn nộp học phí phải trước ngày bắt đầu học kỳ.'))
        if late_fee_start and tuition_deadline and late_fee_start <= tuition_deadline:
            raise ValidationError(_('Ngày bắt đầu tính phí trễ phải sau hạn nộp học phí.'))

        # Kiểm tra tín chỉ
        if min_credits and max_credits and min_credits > max_credits:
            raise ValidationError(_('Tín chỉ tối thiểu không được lớn hơn tín chỉ tối đa.'))
        if total_credits and max_credits and total_credits < max_credits:
            raise ValidationError(_('Tổng tín chỉ không được nhỏ hơn tín chỉ tối đa.'))

        # Kiểm tra trạng thái
        if status == 'closed' and is_active:
            raise ValidationError(_('Học kỳ đã đóng không thể ở trạng thái hoạt động.'))

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            if not instance.pk:
                instance.created_by = self.user
            instance.updated_by = self.user
        if commit:
            instance.save()
        return instance