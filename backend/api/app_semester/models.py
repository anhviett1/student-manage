from django.db import models
from django.conf import settings
from datetime import date
from django.utils.translation import gettext_lazy as _

class Semester(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Sắp tới'),
        ('current', 'Đang diễn ra'),
        ('completed', 'Đã kết thúc'),
        ('cancelled', 'Đã hủy'),
    ]

    semester_id = models.CharField(max_length=20, primary_key=True, verbose_name='Mã học kỳ', default='HK001')
    name = models.CharField(max_length=100, verbose_name='Tên học kỳ', default='Học kỳ 1')
    academic_year = models.CharField(max_length=9, verbose_name='Năm học', default='2023-2024')
    
    # Thời gian
    start_date = models.DateField(verbose_name='Ngày bắt đầu', default=date.today)
    end_date = models.DateField(verbose_name='Ngày kết thúc', default=date.today)
    registration_start = models.DateField(verbose_name='Ngày bắt đầu đăng ký', default=date.today)
    registration_end = models.DateField(verbose_name='Ngày kết thúc đăng ký', default=date.today)
    add_drop_deadline = models.DateField(verbose_name='Hạn chót thêm/xóa môn', default=date.today)

    # Thông tin học tập
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming', verbose_name='Trạng thái')
    total_credits = models.PositiveIntegerField(default=0, verbose_name='Tổng số tín chỉ')
    min_credits = models.PositiveIntegerField(default=12, verbose_name='Số tín chỉ tối thiểu')
    max_credits = models.PositiveIntegerField(default=24, verbose_name='Số tín chỉ tối đa')

    # Thông tin tài chính
    tuition_deadline = models.DateField(verbose_name='Hạn nộp học phí', default=date.today)
    late_fee_start = models.DateField(verbose_name='Ngày bắt đầu tính phí trễ', default=date.today)
    late_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Phí trễ hạn')

    # Thông tin bổ sung
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    notes = models.TextField(blank=True, null=True, verbose_name='Ghi chú')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    is_deleted = models.BooleanField(default=False, verbose_name='Đã xóa')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo', null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    

    def __str__(self):
        return f"{self.name} - {self.academic_year}"

    class Meta:
        verbose_name = _('semester')
        verbose_name_plural = _('semesters')
        ordering = ['-start_date']
        permissions = [
            ("can_view_semester", "Có thể xem học kỳ"),
            ("can_manage_semester", "Có thể quản lý học kỳ"),
            ("can_view_semester_schedule", "Có thể xem lịch học kỳ"),
            ("can_manage_semester_registration", "Có thể quản lý đăng ký học kỳ"),
        ]
    def save(self, *args, **kwargs):
        # Validate dates
        if self.start_date > self.end_date:
            raise ValueError(_('Ngày bắt đầu phải trước ngày kết thúc.'))
        if self.registration_start > self.registration_end:
            raise ValueError(_('Ngày bắt đầu đăng ký phải trước ngày kết thúc đăng ký.'))
        if self.tuition_deadline < self.late_fee_start:
            raise ValueError(_('Hạn nộp học phí phải trước ngày bắt đầu tính phí trễ.'))
        super().save(*args, **kwargs)
