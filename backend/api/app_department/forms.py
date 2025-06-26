from django import forms
from ..app_department.models import Department
from django.utils.translation import gettext_lazy as _

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["department_name", "description", "is_active"]

        widgets = {
            "department_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Nhập tên khoa"),
                    "required": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

        labels = {
            "department_name": _("Tên khoa"),
            "description": _("Mô tả"),
            "is_active": _("Đang hoạt động"),
        }

        error_messages = {
            "department_name": {"required": _("Vui lòng nhập tên khoa.")},
        }

    def clean_department_name(self):
        name = self.cleaned_data.get("department_name")
        if not name:
            raise forms.ValidationError(_("Tên khoa không được để trống."))
        if Department.objects.filter(department_name=name).exists():
            raise forms.ValidationError(_("Khoa này đã tồn tại. Vui lòng chọn tên khác."))
        return name
