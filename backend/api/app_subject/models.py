from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ..app_home.models import BaseModel, Department

User = get_user_model()

class Subject(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Đang hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('pending', 'Đang chờ duyệt'),
    ]
    
    subject_id = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name='Mã môn học', default='MH001')
    name = models.CharField(max_length=200, verbose_name='Tên môn học', default='Môn học mặc định', null=False, blank=False)
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    credits = models.PositiveIntegerField(verbose_name='Số tín chỉ', default=3)
    semester = models.ForeignKey('app_semester.Semester', on_delete=models.CASCADE, related_name='subject_semesters', verbose_name='Học kỳ', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='subject_departments', verbose_name='Khoa')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo', null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_subjects')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_subjects')
    
    def __str__(self):
        return f"{self.name} ({self.subject_id})"
    
    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')
        ordering = ['name']
        permissions = [
            ("can_view_subject_details", "Có thể xem thông tin môn học"),
            ("can_manage_subject", "Có thể quản lý môn học"),
            ("can_view_subject_scores", "Có thể xem điểm môn học"),
            ("can_manage_subject_scores", "Có thể quản lý điểm môn học"),
        ]
