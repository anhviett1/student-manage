from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ..app_home.models import User
from ..app_student.models import Student
from ..app_subject.models import Subject
from ..app_semester.models import Semester

User = get_user_model()

def get_default_student():
    return Student.objects.first().student_id if Student.objects.exists() else 1

def get_default_subject():
    return Subject.objects.first().subject_id if Subject.objects.exists() else 1

def get_default_semester():
    return Semester.objects.first().semester_id if Semester.objects.exists() else 1

class Score(models.Model):
    STATUS_CHOICES = [
        ("active", "Đang hoạt động"),
        ("inactive", "Không hoạt động"),
        ("pending", "Đang chờ duyệt"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_scores", verbose_name="Sinh viên", default=get_default_student)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject_scores", verbose_name="Môn học", default=get_default_subject)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="semester_scores", verbose_name="Học kỳ", default=get_default_semester)

    # Điểm số
    midterm_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Điểm giữa kỳ")
    final_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Điểm cuối kỳ")
    total_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Tổng điểm")

    # Thông tin bổ sung
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", verbose_name="Trạng thái")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo", null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.semester}"
    
    class Meta:
        app_label = "app_score"
        