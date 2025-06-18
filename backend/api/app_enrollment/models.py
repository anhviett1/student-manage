from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ..app_student.models import Student
from ..app_subject.models import Subject
from ..app_semester.models import Semester
from datetime import date
from django.utils.translation import gettext_lazy as _
from ..app_home.models import User
from ..app_class.models import Class

User = get_user_model()


def get_default_student():
    student = Student.objects.first()
    return student.student_id if student else None


def get_default_subject():
    subject = Subject.objects.first()
    return subject.subject_id if subject else None


def get_default_semester():
    semester = Semester.objects.first()
    return semester.semester_id if semester else None


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("active", "Đang hoạt động"),
        ("inactive", "Không hoạt động"),
        ("pending", "Đang chờ duyệt"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="student_enrollments",
        verbose_name="Sinh viên",
        default=get_default_student,
        null=True,
        blank=True,
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="subject_enrollments",
        verbose_name="Môn học",
        default=get_default_subject,
        null=True,
        blank=True,
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="semester_enrollments",
        verbose_name="Học kỳ",
        default=get_default_semester,
        null=True,
        blank=True,
    )
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="class_enrollments")

    # Thông tin đăng ký
    enrollment_date = models.DateField(verbose_name="Ngày đăng ký", default=date.today)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Chờ xử lý"),
            ("approved", "Đã duyệt"),
            ("rejected", "Từ chối"),
        ],
        default="pending",
    )
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    # Thông tin hệ thống
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Ngày tạo", null=False, blank=False
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.semester})"

    class Meta:
        verbose_name = _("enrollment")
        verbose_name_plural = _("enrollments")
        ordering = ["-created_at"]
        unique_together = ["student", "subject", "semester"]
        permissions = [
            ("can_view_enrollment_details", "Có thể xem thông tin đăng ký"),
            ("can_manage_enrollment", "Có thể quản lý đăng ký"),
            ("can_view_enrollment_statistics", "Có thể xem thống kê đăng ký"),
            ("can_export_enrollment", "Có thể xuất đăng ký"),
        ]
