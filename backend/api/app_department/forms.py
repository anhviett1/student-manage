from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = User.department.model
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "data-placeholder": _("Nhập tên khoa"),
                    "required": True,
                }
            ),
        }
        labels = {
            "name": _("Tên khoa"),
        }
        error_messages = {
            "name": {"required": _("Vui lòng nhập tên khoa.")},
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
