from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from ..app_semester.models import Semester
from ..app_subject.models import Subject
from ..app_teacher.models import Teacher
from django.utils.translation import gettext_lazy as _
from ..app_department.models import Department

User = get_user_model()


def get_default_semester():
    return Semester.objects.first().semester_id if Semester.objects.exists() else "HK001"


def get_default_subject():
    return Subject.objects.first().subject_id if Subject.objects.exists() else "MH001"


class Class(models.Model):
    STATUS_CHOICES = [
        ("active", "Đang hoạt động"),
        ("inactive", "Không hoạt động"),
        ("pending", "Đang chờ duyệt"),
    ]

    class_id = models.CharField(max_length=20, unique=True, verbose_name="Mã lớp", default="L001", null=False, blank=False)
    # Thông tin lớp học
    class_name = models.CharField(max_length=200, verbose_name="Tên lớp", default="Lớp mặc định", null=False, blank=False)
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="class_departments",verbose_name="Khoa",)
    credits = models.PositiveIntegerField(verbose_name="Số tín chỉ", default=3, null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", verbose_name="Trạng thái")
    
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    # Quan hệ
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="class_semesters", verbose_name="Học kỳ", default=get_default_semester, to_field="semester_id",)
    subject = models.ForeignKey( Subject, on_delete=models.CASCADE, related_name="class_subjects", verbose_name="Môn học", default=get_default_subject, to_field="subject_id",)
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,related_name="class_teachers",verbose_name="Giảng viên", to_field="teacher_id",)
    teachers = models.ManyToManyField(Teacher, related_name="class_teacher_sets")
    subjects = models.ManyToManyField(Subject, related_name="class_subject_sets")

    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo", null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật", null=False, blank=False)

    def __str__(self):
        return f"{self.class_name} ({self.class_id})"

    class Meta:
        app_label = "app_class"
        
