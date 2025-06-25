from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ..app_department.models import Department

User = get_user_model()

class Subject(models.Model):
    STATUS_CHOICES = [
        ("active", "Đang hoạt động"),
        ("inactive", "Không hoạt động"),
        ("pending", "Đang chờ duyệt"),
    ]

    subject_id = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name="Mã môn học", default="MH001")
    subject_name = models.CharField(max_length=200, verbose_name="Tên môn học", default="Môn học mặc định", null=False, blank=False,)
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    credits = models.PositiveIntegerField(verbose_name="Số tín chỉ", default=3)
    
    semester = models.ForeignKey("app_semester.Semester", on_delete=models.CASCADE, related_name="subject_semesters", verbose_name="Học kỳ", null=True, blank=True,)
    department = models.ForeignKey( Department, on_delete=models.SET_NULL, null=True, related_name="subject_departments", verbose_name="Khoa")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", verbose_name="Trạng thái")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo", null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return f"{self.name} ({self.subject_id})"

    class Meta:
        app_label = "app_subject"
        
