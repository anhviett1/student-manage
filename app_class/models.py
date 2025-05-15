from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from app_semester.models import Semester
from app_subject.models import Subject
from app_teacher.models import Teacher

User = get_user_model()

def get_default_semester():
    return Semester.objects.first().id if Semester.objects.exists() else 'HK001'

def get_default_subject():
    return Subject.objects.first().id if Subject.objects.exists() else 'MH001'

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

    class_id = models.CharField(max_length=20, unique=True, verbose_name='Mã lớp', default='L001', null=False, blank=False)
    # Thông tin lớp học
    name = models.CharField(max_length=200, verbose_name='Tên lớp', default='Lớp mặc định', null=False, blank=False)
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, verbose_name='Khoa', default='cntt', null=False, blank=False)
    credits = models.PositiveIntegerField(verbose_name='Số tín chỉ', default=3, null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    
    # Quan hệ
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='classes', verbose_name='Học kỳ', default=get_default_semester, to_field='semester_id')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classes', verbose_name='Môn học', default=get_default_subject, to_field='subject_id')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='classes', verbose_name='Giảng viên', to_field='teacher_id')

    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo', null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật', null=False, blank=False)
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
            ("can_view_class_enrollments", "Có thể xem danh sách đăng ký lớp học"),
            ("can_manage_class_enrollments", "Có thể quản lý danh sách đăng ký lớp học")
        ]