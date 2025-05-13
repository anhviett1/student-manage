from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Teacher(models.Model):
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
    
    FACULTY_CHOICES = [
        ('cntt', 'Công nghệ thông tin'),
        ('kt', 'Kinh tế'),
        ('nn', 'Ngoại ngữ'),
        ('kh', 'Khoa học xã hội'),
        ('khac', 'Khác'),
    ]
    
    DEGREE_CHOICES = [
        ('bachelor', 'Cử nhân'),
        ('master', 'Thạc sĩ'),
        ('phd', 'Tiến sĩ'),
        ('professor', 'Giáo sư'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Tài khoản')
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name='Mã giảng viên')
    first_name = models.CharField(max_length=100, verbose_name='Tên')
    last_name = models.CharField(max_length=100, verbose_name='Họ')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Số điện thoại')
    date_of_birth = models.DateField(verbose_name='Ngày sinh')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Giới tính')
    address = models.TextField(verbose_name='Địa chỉ')
    
    # Thông tin chuyên môn
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, verbose_name='Khoa')
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, verbose_name='Học vị')
    specialization = models.CharField(max_length=200, verbose_name='Chuyên ngành')
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name='Số năm kinh nghiệm')
    
    # Thông tin bổ sung
    profile_picture = models.ImageField(upload_to='teacher_profiles/', null=True, blank=True, verbose_name='Ảnh đại diện')
    bio = models.TextField(blank=True, null=True, verbose_name='Tiểu sử')
    
    # Thông tin hệ thống
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_teachers')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Giảng viên"
        verbose_name_plural = "Giảng viên"
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
