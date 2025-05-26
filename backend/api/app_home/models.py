from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class BaseModel(models.Model):
    """
    Base model cho tất cả các model trong hệ thống
    Cung cấp các trường cơ bản và chức năng chung
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Ngày tạo'),
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Ngày cập nhật'),
        db_index=True
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_('Đã xóa'),
        db_index=True
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Ngày xóa')
    )
    created_by = models.ForeignKey(
        'app_home.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_created',
        verbose_name=_('Người tạo')
    )
    updated_by = models.ForeignKey(
        'app_home.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_updated',
        verbose_name=_('Người cập nhật')
    )
    deleted_by = models.ForeignKey(
        'app_home.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_deleted',
        verbose_name=_('Người xóa')
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self, user=None):
        """Soft delete object"""
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.deleted_by = user
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])

    def restore(self, user=None):
        """Restore soft deleted object"""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.updated_by = user
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by', 'updated_by'])

    def save(self, *args, **kwargs):
        """Override save method to handle created_by and updated_by"""
        if not self.pk:  # New object
            if not self.created_by and hasattr(self, 'request') and self.request.user.is_authenticated:
                self.created_by = self.request.user
        else:  # Existing object
            if hasattr(self, 'request') and self.request.user.is_authenticated:
                self.updated_by = self.request.user
        super().save(*args, **kwargs)

    @classmethod
    def get_active_objects(cls):
        """Get all active (non-deleted) objects"""
        return cls.objects.filter(is_deleted=False)

    @classmethod
    def get_deleted_objects(cls):
        """Get all deleted objects"""
        return cls.objects.filter(is_deleted=True)

class User(AbstractUser):
    """
    Custom User model cho hệ thống
    """
    ROLE_CHOICES = (
        ('student', _('Sinh viên')),
        ('teacher', _('Giảng viên')),
        ('admin', _('Quản trị viên')),
        ('staff', _('Nhân viên')),
        ('parent', _('Phụ huynh')),
        ('department_head', _('Trưởng khoa')),
    )
    
    # Thông tin cơ bản
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name=_('Vai trò'),
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Ngày tạo'),
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Ngày cập nhật'),
        db_index=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Đang hoạt động'),
        db_index=True
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_('Đã xóa'),
        db_index=True
    )
    
    # Thông tin liên hệ
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP đăng nhập cuối')
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name=_('Ảnh đại diện')
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('Số điện thoại')
    )
    emergency_contact = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Liên hệ khẩn cấp')
    )
    emergency_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('Số điện thoại khẩn cấp')
    )
    
    # Thông tin bổ sung
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('Số điện thoại')
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Địa chỉ')
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Khoa')
    )
    role = models.ForeignKey(
        'Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Vai trò')
    )
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
        permissions = [
            ("can_view_dashboard", _("Có thể xem bảng điều khiển")),
            ("can_manage_students", _("Có thể quản lý sinh viên")),
            ("can_manage_teachers", _("Có thể quản lý giảng viên")),
            ("can_manage_classes", _("Có thể quản lý lớp học")),
            ("can_manage_subjects", _("Có thể quản lý môn học")),
            ("can_manage_scores", _("Có thể quản lý điểm số")),
            ("can_view_reports", _("Có thể xem báo cáo")),
            ("can_manage_enrollments", _("Có thể quản lý đăng ký")),
        ]
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Lấy họ và tên đầy đủ của người dùng"""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def get_short_name(self):
        """Lấy tên ngắn gọn của người dùng"""
        return self.first_name or self.username

    @property
    def is_student(self):
        """Kiểm tra xem người dùng có phải là sinh viên không"""
        return self.role == 'student'

    @property
    def is_teacher(self):
        """Kiểm tra xem người dùng có phải là giảng viên không"""
        return self.role == 'teacher'

    @property
    def is_admin(self):
        """Kiểm tra xem người dùng có phải là admin không"""
        return self.role == 'admin'

    def get_role_display_name(self):
        """Lấy tên hiển thị của vai trò"""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    def update_last_login_ip(self, ip_address):
        """Cập nhật IP đăng nhập cuối cùng"""
        self.last_login_ip = ip_address
        self.save(update_fields=['last_login_ip'])

    def soft_delete(self):
        """Soft delete user"""
        self.is_active = False
        self.is_deleted = True
        self.save(update_fields=['is_active', 'is_deleted'])

    def restore(self):
        """Restore soft deleted user"""
        self.is_active = True
        self.is_deleted = False
        self.save(update_fields=['is_active', 'is_deleted'])

class Department(models.Model):
    """
    Model đại diện cho khoa trong hệ thống
    """
    name = models.CharField(
        max_length=200, 
        verbose_name='Tên khoa',
        null=False,
        blank=False
    )
    code = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name='Mã khoa',
        null=False,
        blank=False
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Mô tả'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Đang hoạt động'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Ngày tạo'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Ngày cập nhật'
    )
    is_deleted = models.BooleanField(
        default=False, 
        verbose_name='Đã xóa'
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = _('department')
        verbose_name_plural = _('departments')
        ordering = ['name']
        db_table = 'app_home_department'
        permissions = [
            ("can_view_department", "Có thể xem thông tin khoa"),
            ("can_manage_department", "Có thể quản lý khoa"),
        ]

    def save(self, *args, **kwargs):
        if not self.code:
            # Tự động tạo mã khoa nếu chưa có
            last_department = Department.objects.order_by('-id').first()
            if last_department:
                last_id = int(last_department.code[2:]) if last_department.code.startswith('KH') else 0
                self.code = f'KH{str(last_id + 1).zfill(3)}'
            else:
                self.code = 'KH001'
        super().save(*args, **kwargs)

    def soft_delete(self):
        """Soft delete object"""
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    def restore(self):
        """Restore soft deleted object"""
        self.is_deleted = False
        self.save(update_fields=['is_deleted'])

class Role(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return self.name