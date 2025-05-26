# app_home/forms.py
from django import forms
from django.contrib.auth import password_validation
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    """Form cho việc cập nhật thông tin người dùng"""
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'phone_number', 
                 'emergency_contact', 'emergency_phone', 'profile_picture']
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập họ của bạn'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên của bạn'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@domain.com'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0123456789'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên người liên hệ khẩn cấp'
            }),
            'emergency_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0123456789'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm validators cho số điện thoại
        phone_validator = RegexValidator(
            regex=r'^[0-9]{10,15}$',
            message='Số điện thoại phải có từ 10-15 chữ số'
        )
        self.fields['phone_number'].validators.append(phone_validator)
        self.fields['emergency_phone'].validators.append(phone_validator)

    def clean_profile_picture(self):
        """Validate profile picture"""
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError(_('Kích thước file không được vượt quá 5MB'))
            if not picture.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError(_('Chỉ chấp nhận file JPG hoặc PNG'))
        return picture

    def clean_phone_number(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.isdigit():
            raise forms.ValidationError(_('Số điện thoại chỉ được chứa chữ số'))
        return phone

    def clean_emergency_phone(self):
        """Validate emergency phone number"""
        phone = self.cleaned_data.get('emergency_phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError(_('Số điện thoại chỉ được chứa chữ số'))
        return phone

class ChangePasswordForm(PasswordChangeForm):
    """Form cho việc đổi mật khẩu"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm class Bootstrap cho các trường
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.help_text:
                field.widget.attrs['data-bs-toggle'] = 'tooltip'
                field.widget.attrs['title'] = field.help_text

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Mật khẩu cũ không đúng.')
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('Mật khẩu mới không khớp.')
        password_validation.validate_password(new_password2, self.user)
        return new_password2

    def save(self):
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        self.user.save()
        return self.user