from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Sinh viên'),
        ('teacher', 'Giảng viên'),
        ('admin', 'Quản trị viên'),
        ('staff', 'Nhân viên'),
        ('parent', 'Phụ huynh'),
        ('department_head', 'Trưởng khoa'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name='Vai trò')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP đăng nhập cuối')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, verbose_name='Ảnh đại diện')
    
    # Thông tin liên hệ
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Số điện thoại')
    emergency_contact = models.CharField(max_length=100, blank=True, null=True, verbose_name='Liên hệ khẩn cấp')
    emergency_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Số điện thoại khẩn cấp')
    
    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"
        permissions = [
            ("can_view_dashboard", "Có thể xem bảng điều khiển"),
            ("can_manage_students", "Có thể quản lý sinh viên"),
            ("can_manage_teachers", "Có thể quản lý giảng viên"),
            ("can_manage_classes", "Có thể quản lý lớp học"),
            ("can_manage_subjects", "Có thể quản lý môn học"),
            ("can_manage_scores", "Có thể quản lý điểm số"),
            ("can_view_reports", "Có thể xem báo cáo"),
            ("can_manage_enrollments", "Có thể quản lý đăng ký"),
        ]
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username