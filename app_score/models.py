from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from app_student.models import Student
from app_subject.models import Subject
from app_semester.models import Semester

User = get_user_model()

class Score(models.Model):
    STATUS_CHOICES = [
        ('active', 'Đang hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('pending', 'Đang chờ duyệt'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_scores', verbose_name='Sinh viên')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_scores', verbose_name='Môn học')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='semester_scores', verbose_name='Học kỳ')
    
    # Điểm số
    midterm_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='Điểm giữa kỳ')
    final_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='Điểm cuối kỳ')
    total_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='Tổng điểm')
    
    # Thông tin bổ sung
    notes = models.TextField(blank=True, null=True, verbose_name='Ghi chú')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_scores')
    
    def __str__(self):
        return f"{self.student} - {self.subject} ({self.semester})"
    
    def save(self, *args, **kwargs):
        # Tính tổng điểm nếu có điểm giữa kỳ và cuối kỳ
        if self.midterm_score is not None and self.final_score is not None:
            self.total_score = (self.midterm_score * 0.4) + (self.final_score * 0.6)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Điểm số"
        verbose_name_plural = "Điểm số"
        ordering = ['-created_at']
        unique_together = ['student', 'subject', 'semester']
        permissions = [
            ("can_view_score_details", "Có thể xem thông tin điểm số"),
            ("can_manage_score", "Có thể quản lý điểm số"),
            ("can_view_score_statistics", "Có thể xem thống kê điểm số"),
            ("can_export_score", "Có thể xuất điểm số"),
        ]