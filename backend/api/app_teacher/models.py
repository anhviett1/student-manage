from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from app_home.models import BaseModel, Department

User = get_user_model()

class Teacher(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Đang giảng dạy'),
        ('inactive', 'Tạm nghỉ'),
        ('retired', 'Đã nghỉ hưu'),
        ('on_leave', 'Nghỉ phép'),
    ]
    
    
    
    DEGREE_CHOICES = [
        ('bachelor', 'Cử nhân'),
        ('master', 'Thạc sĩ'),
        ('phd', 'Tiến sĩ'),
        ('professor', 'Giáo sư'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Tài khoản')
    teacher_id = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name='Mã giảng viên', default='GV001')
    first_name = models.CharField(max_length=100, verbose_name='Tên', default='Tên')
    last_name = models.CharField(max_length=100, verbose_name='Họ', default='Họ')
    email = models.EmailField(unique=True, verbose_name='Email', default='teacher@example.com')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Số điện thoại', default='0123456789')
    date_of_birth = models.DateField(verbose_name='Ngày sinh', default=timezone.now)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Giới tính', default='M')
    address = models.TextField(verbose_name='Địa chỉ', default='Địa chỉ mặc định')
    
    # Thông tin chuyên môn
   
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, verbose_name='Học vị', default='master')
    specialization = models.CharField(max_length=200, verbose_name='Chuyên ngành', default='Chưa xác định')
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name='Số năm kinh nghiệm')
    
    # Thông tin bổ sung
    profile_picture = models.ImageField(upload_to='teacher_profiles/', null=True, blank=True, verbose_name='Ảnh đại diện')
    bio = models.TextField(blank=True, null=True, verbose_name='Tiểu sử')
    
    # Thông tin hệ thống
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo', null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_teachers')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_teachers')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='teacher_departments')
    
    def __str__(self):
        return f"{self.teacher_id} - {self.get_full_name()}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')
        ordering = ['last_name', 'first_name']
        permissions = [
            ("can_view_teacher_details", "Có thể xem thông tin giảng viên"),
            ("can_manage_teacher", "Có thể quản lý giảng viên"),
            ("can_view_teacher_schedule", "Có thể xem lịch giảng dạy"),
            ("can_manage_teacher_schedule", "Có thể quản lý lịch giảng dạy"),
        ]

    @property
    def full_name(self):
        return self.get_full_name()