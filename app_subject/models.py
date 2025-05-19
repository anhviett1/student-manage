from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Subject(models.Model):
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
    
    subject_id = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name='Mã môn học', default='MH001')
    name = models.CharField(max_length=200, verbose_name='Tên môn học', default='Môn học mặc định', null=False, blank=False)
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    credits = models.PositiveIntegerField(verbose_name='Số tín chỉ', default=3)
    semester = models.ForeignKey('app_semester.Semester', on_delete=models.CASCADE, verbose_name='Học kỳ', null=True, blank=True)
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, verbose_name='Khoa', default='cntt')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo', null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_subjects')
    
    def __str__(self):
        return f"{self.name} ({self.subject_id})"
    
    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"
        ordering = ['name']
        permissions = [
            ("can_view_subject_details", "Có thể xem thông tin môn học"),
            ("can_manage_subject", "Có thể quản lý môn học"),
            ("can_view_subject_scores", "Có thể xem điểm môn học"),
            ("can_manage_subject_scores", "Có thể quản lý điểm môn học"),
        ]
