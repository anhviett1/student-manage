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

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError(_("Tên khoa không được để trống."))
        if User.department.model.objects.filter(name=name).exists():
            raise forms.ValidationError(_("Khoa này đã tồn tại. Vui lòng chọn tên khác."))
        return name
    def save(self, commit=True):
        department = super().save(commit=False)
        if commit:
            department.save()
        return department
    def __str__(self):
        return self.cleaned_data.get("name", _("Khoa mới"))
    
