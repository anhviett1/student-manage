from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from app_student.models import Student
from app_subject.models import Subject
from app_semester.models import Semester

User = get_user_model()

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Đang hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('pending', 'Đang chờ duyệt'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments', verbose_name='Sinh viên')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments', verbose_name='Môn học')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrollments', verbose_name='Học kỳ')
    
    # Thông tin đăng ký
    enrollment_date = models.DateField(verbose_name='Ngày đăng ký')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    notes = models.TextField(blank=True, null=True, verbose_name='Ghi chú')
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_enrollments')
    
    def __str__(self):
        return f"{self.student} - {self.subject} ({self.semester})"
    
    class Meta:
        verbose_name = "Đăng ký"
        verbose_name_plural = "Đăng ký"
        ordering = ['-created_at']
        unique_together = ['student', 'subject', 'semester']
        permissions = [
            ("can_view_enrollment_details", "Có thể xem thông tin đăng ký"),
            ("can_manage_enrollment", "Có thể quản lý đăng ký"),
            ("can_view_enrollment_statistics", "Có thể xem thống kê đăng ký"),
            ("can_export_enrollment", "Có thể xuất đăng ký"),
        ]
