from django.db import models
from django.utils.translation import gettext_lazy as _
from ..app_home.models import User
from ..app_department.models import Department
from ..app_class.models import Class
from ..app_semester.models import Semester

class Schedule(models.Model):
    DAY_CHOICES = [
        ('mon', _('Thứ Hai')), ('tue', _('Thứ Ba')), ('wed', _('Thứ Tư')),
        ('thu', _('Thứ Năm')), ('fri', _('Thứ Sáu')), ('sat', _('Thứ Bảy')), ('sun', _('Chủ Nhật')),
    ]
    STATUS_CHOICES = [('active', _('Đang hoạt động')), ('inactive', _('Không hoạt động')), ('pending', _('Đang chờ duyệt'))]
    schedule_id = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name=_('Mã lịch học'), default='LH001')
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules', verbose_name=_('Lớp học'))
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teaching_schedules', verbose_name=_('Giảng viên'))
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='schedules', verbose_name=_('Học kỳ'))
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='schedules', verbose_name=_('Khoa'))
    
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES, verbose_name=_('Ngày trong tuần'))
    start_time = models.TimeField(verbose_name=_('Giờ bắt đầu'))
    end_time = models.TimeField(verbose_name=_('Giờ kết thúc'))
    room = models.CharField(max_length=50, verbose_name=_('Phòng học'), default='P101')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name=_('Trạng thái')) 
    is_active = models.BooleanField(default=True, verbose_name=_('Đang hoạt động'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('Đã xóa'))
   
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Ngày tạo'), null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Ngày cập nhật'))
    def __str__(self): return f"{self.class_assigned} - {self.day_of_week} {self.start_time}-{self.end_time}"
    class Meta:
        verbose_name = _('schedule')
        verbose_name_plural = _('schedules')
        ordering = ['day_of_week', 'start_time']
        permissions = [
            ("can_view_schedule", _("Có thể xem lịch học")),
            ("can_manage_schedule", _("Có thể quản lý lịch học")),
        ]