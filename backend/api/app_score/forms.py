from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Score
from ..app_student.models import Student
from ..app_enrollment.models import Enrollment
from ..app_subject.models import Subject
from ..app_semester.models import Semester
from django.core.exceptions import ValidationError


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = [
            "student",
            "subject",
            "semester",
            "midterm_score",
            "final_score",
            "notes",
            "status",
            "is_active",
        ]
        widgets = {
            "student": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "data-placeholder": "Chọn sinh viên",
                    "required": True,
                }
            ),
            "subject": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "data-placeholder": "Chọn môn học",
                    "required": True,
                }
            ),
            "semester": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "data-placeholder": "Chọn học kỳ",
                    "required": True,
                }
            ),
            "midterm_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Điểm giữa kỳ (0-10)",
                    "min": "0",
                    "max": "10",
                    "step": "0.1",
                }
            ),
            "final_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Điểm cuối kỳ (0-10)",
                    "min": "0",
                    "max": "10",
                    "step": "0.1",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Ghi chú (tùy chọn)",
                    "rows": 4,
                }
            ),
            "status": forms.Select(
                choices=Score.STATUS_CHOICES,
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
            "student": _("Sinh viên"),
            "subject": _("Môn học"),
            "semester": _("Học kỳ"),
            "midterm_score": _("Điểm giữa kỳ"),
            "final_score": _("Điểm cuối kỳ"),
            "notes": _("Ghi chú"),
            "status": _("Trạng thái"),
            "is_active": _("Đang hoạt động"),
        }
        error_messages = {
            "student": {"required": _("Vui lòng chọn sinh viên.")},
            "subject": {"required": _("Vui lòng chọn môn học.")},
            "semester": {"required": _("Vui lòng chọn học kỳ.")},
            "status": {"required": _("Vui lòng chọn trạng thái.")},
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Tối ưu hóa queryset
        self.fields["student"].queryset = Student.objects.filter(is_active=True).order_by("name")
        self.fields["subject"].queryset = Subject.objects.filter(is_active=True).order_by("name")
        self.fields["semester"].queryset = Semester.objects.filter(is_active=True).order_by(
            "-start_date"
        )

        # Giá trị mặc định
        if not self.instance.pk:
            self.fields["status"].initial = "pending"
            self.fields["is_active"].initial = True

        # Phân quyền
        if self.user and not self.user.has_perm("app_score.can_manage_score"):
            for field in self.fields.values():
                field.widget.attrs["disabled"] = True

    def clean_midterm_score(self):
        score = self.cleaned_data.get("midterm_score")
        if score is not None:
            if score < 0 or score > 10:
                raise ValidationError(_("Điểm giữa kỳ phải từ 0 đến 10."))
        return score

    def clean_final_score(self):
        score = self.cleaned_data.get("final_score")
        if score is not None:
            if score < 0 or score > 10:
                raise ValidationError(_("Điểm cuối kỳ phải từ 0 đến 10."))
        return score

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get("student")
        subject = cleaned_data.get("subject")
        semester = cleaned_data.get("semester")
        status = cleaned_data.get("status")
        is_active = cleaned_data.get("is_active")

        # Kiểm tra unique_together
        if student and subject and semester:
            if (
                Score.objects.filter(
                    student=student,
                    subject=subject,
                    semester=semester,
                )
                .exclude(pk=self.instance.pk if self.instance else None)
                .exists()
            ):
                raise ValidationError(_("Sinh viên đã có điểm cho môn học này trong học kỳ này."))

            # Kiểm tra enrollment
            if not Enrollment.objects.filter(
                student=student,
                subject=subject,
                semester=semester,
                status="approved",
            ).exists():
                raise ValidationError(
                    _(
                        "Sinh viên chưa đăng ký môn học này trong học kỳ này hoặc đăng ký chưa được duyệt."
                    )
                )

        # Kiểm tra status và is_active
        if status == "failed" and is_active:
            raise ValidationError(_('Điểm trạng thái "Thất bại" không thể ở trạng thái hoạt động.'))

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
