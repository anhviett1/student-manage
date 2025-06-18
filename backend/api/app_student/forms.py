from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .models import Student
from ..app_home.models import Department
from datetime import date


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "gender",
            "is_active",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
            "enrollment_date",
            "graduation_date",
            "status",
            "major",
            "minor",
            "emergency_contact_name",
            "emergency_contact_phone",
            "emergency_contact_relationship",
            "profile_picture",
            "student_id_card",
            "blood_type",
            "medical_conditions",
            "allergies",
            "department",
        ]
        widgets = {
            "student_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập mã sinh viên (VD: SV001)",
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
                choices=Student.GENDER_CHOICES,
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
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập địa chỉ",
                    "rows": 3,
                    "required": True,
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập thành phố",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập tỉnh/thành",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập mã bưu điện",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập quốc gia",
                }
            ),
            "enrollment_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "required": True,
                }
            ),
            "graduation_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "status": forms.Select(
                choices=Student.STATUS_CHOICES,
                attrs={
                    "class": "form-control select2",
                    "required": True,
                },
            ),
            "major": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập chuyên ngành",
                    "required": True,
                }
            ),
            "minor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập chuyên ngành phụ (tùy chọn)",
                }
            ),
            "emergency_contact_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập tên người liên hệ khẩn cấp",
                }
            ),
            "emergency_contact_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "VD: +0901234567",
                }
            ),
            "emergency_contact_relationship": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập mối quan hệ",
                }
            ),
            "profile_picture": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/jpeg,image/png",
                }
            ),
            "student_id_card": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập mã thẻ sinh viên",
                    "required": True,
                }
            ),
            "blood_type": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập nhóm máu (tùy chọn)",
                }
            ),
            "medical_conditions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập tình trạng sức khỏe (tùy chọn)",
                    "rows": 3,
                }
            ),
            "allergies": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập dị ứng (tùy chọn)",
                    "rows": 3,
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
            "student_id": _("Mã sinh viên"),
            "first_name": _("Tên"),
            "last_name": _("Họ"),
            "email": _("Email"),
            "phone": _("Số điện thoại"),
            "date_of_birth": _("Ngày sinh"),
            "gender": _("Giới tính"),
            "is_active": _("Đang hoạt động"),
            "address": _("Địa chỉ"),
            "city": _("Thành phố"),
            "state": _("Tỉnh/Thành"),
            "postal_code": _("Mã bưu điện"),
            "country": _("Quốc gia"),
            "enrollment_date": _("Ngày nhập học"),
            "graduation_date": _("Ngày tốt nghiệp"),
            "status": _("Trạng thái"),
            "major": _("Chuyên ngành"),
            "minor": _("Chuyên ngành phụ"),
            "emergency_contact_name": _("Người liên hệ khẩn cấp"),
            "emergency_contact_phone": _("Số điện thoại khẩn cấp"),
            "emergency_contact_relationship": _("Mối quan hệ"),
            "profile_picture": _("Ảnh đại diện"),
            "student_id_card": _("Mã thẻ sinh viên"),
            "blood_type": _("Nhóm máu"),
            "medical_conditions": _("Tình trạng sức khỏe"),
            "allergies": _("Dị ứng"),
            "department": _("Khoa"),
        }
        error_messages = {
            "student_id": {"required": _("Vui lòng nhập mã sinh viên.")},
            "first_name": {"required": _("Vui lòng nhập tên.")},
            "last_name": {"required": _("Vui lòng nhập họ.")},
            "email": {"required": _("Vui lòng nhập email.")},
            "date_of_birth": {"required": _("Vui lòng chọn ngày sinh.")},
            "enrollment_date": {"required": _("Vui lòng chọn ngày nhập học.")},
            "status": {"required": _("Vui lòng chọn trạng thái.")},
            "major": {"required": _("Vui lòng nhập chuyên ngành.")},
            "student_id_card": {"required": _("Vui lòng nhập mã thẻ sinh viên.")},
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
            self.fields["enrollment_date"].initial = date.today()

        if self.user and not self.user.has_perm("app_student.can_manage_student"):
            for field in self.fields.values():
                field.widget.attrs["disabled"] = True

    def clean_student_id(self):
        student_id = self.cleaned_data.get("student_id")
        if not student_id.startswith("SV"):
            raise forms.ValidationError(_('Mã sinh viên phải bắt đầu bằng "SV".'))
        if (
            Student.objects.filter(student_id=student_id)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise forms.ValidationError(_("Mã sinh viên đã tồn tại."))
        return student_id

    def clean_student_id_card(self):
        student_id_card = self.cleaned_data.get("student_id_card")
        if (
            Student.objects.filter(student_id_card=student_id_card)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise forms.ValidationError(_("Mã thẻ sinh viên đã tồn tại."))
        return student_id_card

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            Student.objects.filter(email=email)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise forms.ValidationError(_("Email này đã được sử dụng."))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            phone_validator = RegexValidator(
                regex=r"^\+?[0-9]{10,15}$", message=_("Số điện thoại phải có từ 10-15 chữ số.")
            )
            phone_validator(phone)
        return phone

    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data.get("emergency_contact_phone")
        if phone:
            phone_validator = RegexValidator(
                regex=r"^\+?[0-9]{10,15}$",
                message=_("Số điện thoại khẩn cấp phải có từ 10-15 chữ số."),
            )
            phone_validator(phone)
        return phone

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        if dob > date.today():
            raise forms.ValidationError(_("Ngày sinh không được là ngày trong tương lai."))
        return dob

    def clean_enrollment_date(self):
        enrollment_date = self.cleaned_data.get("enrollment_date")
        if enrollment_date > date.today():
            raise forms.ValidationError(_("Ngày nhập học không được là ngày trong tương lai."))
        return enrollment_date

    def clean_graduation_date(self):
        graduation_date = self.cleaned_data.get("graduation_date")
        enrollment_date = self.cleaned_data.get("enrollment_date")
        if graduation_date and enrollment_date and graduation_date <= enrollment_date:
            raise forms.ValidationError(_("Ngày tốt nghiệp phải sau ngày nhập học."))
        return graduation_date

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        is_active = cleaned_data.get("is_active")
        if status in ["graduated", "withdrawn"] and is_active:
            raise forms.ValidationError(
                _("Sinh viên đã tốt nghiệp hoặc rút lui không thể ở trạng thái hoạt động.")
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
