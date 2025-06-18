from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Subject
from ..app_semester.models import Semester
from ..app_home.models import Department


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = [
            "subject_id",
            "name",
            "description",
            "credits",
            "semester",
            "department",
            "status",
            "is_active",
        ]
        widgets = {
            "subject_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập mã môn học (VD: MH001)",
                    "required": True,
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập tên môn học",
                    "required": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nhập mô tả (tùy chọn)",
                    "rows": 4,
                }
            ),
            "credits": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "max": "10",
                    "step": "1",
                    "required": True,
                }
            ),
            "semester": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "placeholder": "Chọn học kỳ (tùy chọn)",
                }
            ),
            "department": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "placeholder": "Chọn khoa",
                    "required": True,
                }
            ),
            "status": forms.Select(
                choices=Subject.STATUS_CHOICES,
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
        }
        labels = {
            "subject_id": _("Mã môn học"),
            "name": _("Tên môn học"),
            "description": _("Mô tả"),
            "credits": _("Số tín chỉ"),
            "semester": _("Học kỳ"),
            "department": _("Khoa"),
            "status": _("Trạng thái"),
            "is_active": _("Đang hoạt động"),
        }
        error_messages = {
            "subject_id": {"required": _("Vui lòng nhập mã môn học.")},
            "name": {"required": _("Vui lòng nhập tên môn học.")},
            "credits": {"required": _("Vui lòng nhập số tín chỉ.")},
            "department": {"required": _("Vui lòng chọn khoa.")},
            "status": {"required": _("Vui lòng chọn trạng thái.")},
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["semester"].queryset = Semester.objects.filter(is_active=True).order_by(
            "-start_date"
        )
        self.fields["department"].queryset = Department.objects.filter(is_active=True).order_by(
            "name"
        )

        if not self.instance.pk:
            self.fields["status"].initial = "pending"
            self.fields["is_active"].initial = True

        if self.user and not self.user.has_perm("app_subject.can_manage_subject"):
            for field in self.fields.values():
                field.widget.attrs["disabled"] = True

    def clean_subject_id(self):
        subject_id = self.cleaned_data.get("subject_id")
        if not subject_id.startswith("MH"):
            raise forms.ValidationError(_('Mã môn học phải bắt đầu bằng "MH".'))
        if (
            Subject.objects.filter(subject_id=subject_id)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise forms.ValidationError(_("Mã môn học đã tồn tại."))
        return subject_id

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3 or len(name) > 200:
            raise forms.ValidationError(_("Tên môn học phải từ 3 đến 200 ký tự."))
        return name

    def clean_credits(self):
        credits = self.cleaned_data.get("credits")
        if credits < 1 or credits > 10:
            raise forms.ValidationError(_("Số tín chỉ phải từ 1 đến 10."))
        return credits

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        is_active = cleaned_data.get("is_active")
        if status == "inactive" and is_active:
            raise forms.ValidationError(
                _("Môn học không hoạt động không thể ở trạng thái đang hoạt động.")
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
