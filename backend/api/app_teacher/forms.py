from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .models import Teacher
from ..app_home.models import Department
from datetime import date


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            "teacher_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập mã giảng viên (VD: GV001)",
                    "required": True,
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập tên",
                    "required": True,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập họ",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập email",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "VD: +0901234567",
                    "required": True,
                }
            ),
            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "required": True,
                }
            ),
            "gender": forms.Select(
                choices=Teacher.GENDER_CHOICES,
                attrs={
                    "class": "form-control select2",
                    "required": True,
                },
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập địa chỉ",
                    "rows": 3,
                    "required": True,
                }
            ),
            "degree": forms.Select(
                choices=Teacher.DEGREE_CHOICES,
                attrs={
                    "class": "form-control select2",
                    "required": True,
                },
            ),
            "specialization": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập chuyên ngành",
                    "required": True,
                }
            ),
            "years_of_experience": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "100",
                    "required": True,
                }
            ),
            "profile_picture": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/jpeg,image/png",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập tiểu sử (tùy chọn)",
                    "rows": 4,
                }
            ),
            "status": forms.Select(
                choices=Teacher.STATUS_CHOICES,
                attrs={
                    "class": "form-control select2",
                    "required": True,
                },
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "department": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "placeholder": "Chọn khoa",
                    "required": True,
                }
            ),
        }
        labels = {
            "teacher_id": _("Mã giảng viên"),
            "first_name": _("Tên"),
            "last_name": _("Họ"),
            "email": _("Email"),
            "phone": _("Số điện thoại"),
            "date_of_birth": _("Ngày sinh"),
            "gender": _("Giới tính"),
            "address": _("Địa chỉ"),
            "degree": _("Học vị"),
            "specialization": _("Chuyên ngành"),
            "years_of_experience": _("Số năm kinh nghiệm"),
            "profile_picture": _("Ảnh đại diện"),
            "bio": _("Tiểu sử"),
            "status": _("Trạng thái"),
            "is_active": _("Đang hoạt động"),
            "department": _("Khoa"),
        }
        error_messages = {
            "teacher_id": {"required": _("Vui lòng nhập mã giảng viên.")},
            "first_name": {"required": _("Vui lòng nhập tên.")},
            "last_name": {"required": _("Vui lòng nhập họ.")},
            "email": {"required": _("Vui lòng nhập email.")},
            "phone": {"required": _("Vui lòng nhập số điện thoại.")},
            "date_of_birth": {"required": _("Vui lòng chọn ngày sinh.")},
            "degree": {"required": _("Vui lòng chọn học vị.")},
            "specialization": {"required": _("Vui lòng nhập chuyên ngành.")},
            "years_of_experience": {"required": _("Vui lòng nhập số năm kinh nghiệm.")},
            "status": {"required": _("Vui lòng chọn trạng thái.")},
            "department": {"required": _("Vui lòng chọn khoa.")},
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["department"].queryset = Department.objects.filter(is_active=True).order_by(
            "name"
        )

        if not self.instance.pk:
            self.fields["status"].initial = "active"
            self.fields["is_active"].initial = True

        if self.user and not self.user.has_perm("app_teacher.can_manage_teacher"):
            for field in self.fields.values():
                field.widget.attrs["disabled"] = True

    def clean_teacher_id(self):
        teacher_id = self.cleaned_data.get("teacher_id")
        if not teacher_id.startswith("GV"):
            raise forms.ValidationError(_('Mã giảng viên phải bắt đầu bằng "GV".'))
        if (
            Teacher.objects.filter(teacher_id=teacher_id)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise forms.ValidationError(_("Mã giảng viên đã tồn tại."))
        return teacher_id

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            Teacher.objects.filter(email=email)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise forms.ValidationError(_("Email này đã được sử dụng."))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        phone_validator = RegexValidator(
            regex=r"^\+?[0-9]{10,15}$", message=_("Số điện thoại phải có từ 10-15 chữ số.")
        )
        phone_validator(phone)
        if (
            Teacher.objects.filter(phone=phone)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise forms.ValidationError(_("Số điện thoại này đã được sử dụng."))
        return phone

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        if dob > date.today():
            raise forms.ValidationError(_("Ngày sinh không được là ngày trong tương lai."))
        return dob

    def clean_years_of_experience(self):
        years = self.cleaned_data.get("years_of_experience")
        if years < 0 or years > 100:
            raise forms.ValidationError(_("Số năm kinh nghiệm phải từ 0 đến 100."))
        return years

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        is_active = cleaned_data.get("is_active")
        if status in ["retired", "inactive"] and is_active:
            raise forms.ValidationError(
                _("Giảng viên đã nghỉ hưu hoặc tạm nghỉ không thể ở trạng thái hoạt động.")
            )
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
