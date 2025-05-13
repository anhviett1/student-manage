from django.db import models
from django.conf import settings


class Semester(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Sắp tới'),
        ('current', 'Đang diễn ra'),
        ('completed', 'Đã kết thúc'),
        ('cancelled', 'Đã hủy'),
    ]
    
    semester_id = models.AutoField(primary_key=True, verbose_name='Mã học kỳ')
    name = models.CharField(max_length=100, verbose_name='Tên học kỳ')
    code = models.CharField(max_length=20, unique=True, verbose_name='Mã học kỳ')
    academic_year = models.CharField(max_length=9, verbose_name='Năm học')  # Format: 2023-2024
    
    # Thời gian
    start_date = models.DateField(verbose_name='Ngày bắt đầu')
    end_date = models.DateField(verbose_name='Ngày kết thúc')
    registration_start = models.DateField(verbose_name='Ngày bắt đầu đăng ký')
    registration_end = models.DateField(verbose_name='Ngày kết thúc đăng ký')
    add_drop_deadline = models.DateField(verbose_name='Hạn chót thêm/xóa môn')
    
    # Thông tin học tập
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming', verbose_name='Trạng thái')
    total_credits = models.PositiveIntegerField(default=0, verbose_name='Tổng số tín chỉ')
    min_credits = models.PositiveIntegerField(default=12, verbose_name='Số tín chỉ tối thiểu')
    max_credits = models.PositiveIntegerField(default=24, verbose_name='Số tín chỉ tối đa')
    
    # Thông tin tài chính
    tuition_deadline = models.DateField(verbose_name='Hạn nộp học phí')
    late_fee_start = models.DateField(verbose_name='Ngày bắt đầu tính phí trễ')
    late_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Phí trễ hạn')
    
    # Thông tin bổ sung
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    notes = models.TextField(blank=True, null=True, verbose_name='Ghi chú')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_semesters', verbose_name='Người tạo')
    
    def __str__(self):
        return f"{self.name} - {self.academic_year}"
    
    class Meta:
        verbose_name = "Semesters"
        verbose_name_plural = "Semesters"
        ordering = ['-start_date']
        permissions = [
            ("can_view_semester", "Có thể xem học kỳ"),
            ("can_manage_semester", "Có thể quản lý học kỳ"),
            ("can_view_semester_schedule", "Có thể xem lịch học kỳ"),
            ("can_manage_semester_registration", "Có thể quản lý đăng ký học kỳ"),
        ]

