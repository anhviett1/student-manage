from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    """Form cập nhật thông tin người dùng"""
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'phone_number', 'emergency_contact', 'emergency_phone', 'profile_picture']
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'Nhập họ',
                'required': True,
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'Nhập tên',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'example@domain.com',
                'required': True,
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'VD: 0123456789',
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'Tên người liên hệ khẩn cấp',
            }),
            'emergency_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'data-placeholder': 'VD: 0123456789',
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png',
            }),
        }
        labels = {
            'last_name': _('Họ'),
            'first_name': _('Tên'),
            'email': _('Email'),
            'phone_number': _('Số điện thoại'),
            'emergency_contact': _('Người liên hệ khẩn cấp'),
            'emergency_phone': _('Số điện thoại khẩn cấp'),
            'profile_picture': _('Ảnh đại diện'),
        }
        error_messages = {
            'last_name': {'required': _('Vui lòng nhập họ.')},
            'first_name': {'required': _('Vui lòng nhập tên.')},
            'email': {'required': _('Vui lòng nhập email.')},
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        phone_validator = RegexValidator(
            regex=r'^\+?[0-9]{10,15}$',
            message=_('Số điện thoại phải có từ 10-15 chữ số, có thể bắt đầu bằng "+".')
        )
        self.fields['phone_number'].validators.append(phone_validator)
        self.fields['emergency_phone'].validators.append(phone_validator)

        if self.user and not self.user.has_perm('app_home.can_manage_user'):
            for field in self.fields.values():
                field.widget.attrs['disabled'] = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError(_('Email này đã được sử dụng.'))
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.lstrip('+').isdigit():
            raise forms.ValidationError(_('Số điện thoại chỉ được chứa chữ số và dấu "+".'))
        return phone

    def clean_emergency_phone(self):
        phone = self.cleaned_data.get('emergency_phone')
        if phone and not phone.lstrip('+').isdigit():
            raise forms.ValidationError(_('Số điện thoại chỉ được chứa chữ số và dấu "+".'))
        return phone

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError(_('Kích thước file không được vượt quá 2MB.'))
            if not picture.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError(_('Chỉ chấp nhận file JPG hoặc PNG.'))
        return picture

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.updated_by = self.user
        if commit:
            instance.save()
        return instance

class ChangePasswordForm(PasswordChangeForm):
    """Form đổi mật khẩu"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'data-bs-toggle': 'tooltip',
                'title': field.help_text or '',
            })

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_('Mật khẩu cũ không đúng.'))
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(_('Mật khẩu mới không khớp.'))
        password_validation.validate_password(new_password2, self.user)
        return new_password2

    def save(self, commit=True):
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user