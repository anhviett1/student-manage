from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from app_semester.models import Semester
from app_subject.models import Subject
from app_teacher.models import Teacher

User = get_user_model()

class Class(models.Model):
    STATUS_CHOICES = [
        ('active', 'Đang hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('pending', 'Đang chờ duyệt'),
    ]
    
    FACULTY_CHOICES = [
        ('cntt', 'Công nghệ thông tin'),
        ('kt', 'Kinh tế'),
        ('nn', 'Ngoại ngữ'),
        ('kh', 'Khoa học xã hội'),
        ('khac', 'Khác'),
    ]
    
    class_id = models.CharField(max_length=20, unique=True, verbose_name='Mã lớp')
    name = models.CharField(max_length=200, verbose_name='Tên lớp')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, verbose_name='Khoa')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    
    # Quan hệ
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='classes', verbose_name='Học kỳ')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classes', verbose_name='Môn học')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='classes', verbose_name='Giảng viên')
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_classes')
    
    def __str__(self):
        return f"{self.name} ({self.class_id})"
    
    class Meta:
        verbose_name = "Lớp học"
        verbose_name_plural = "Lớp học"
        ordering = ['name']
        permissions = [
            ("can_view_class_details", "Có thể xem thông tin lớp học"),
            ("can_manage_class", "Có thể quản lý lớp học"),
            ("can_view_class_scores", "Có thể xem điểm lớp học"),
            ("can_manage_class_scores", "Có thể quản lý điểm lớp học"),
        ]
