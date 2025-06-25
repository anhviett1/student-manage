from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", _("Sinh viên")),
        ("teacher", _("Giảng viên")),
        ("admin", _("Quản trị viên")),
        ("department_head", _("Trưởng khoa")),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student",
        verbose_name=_("Vai trò"),
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Ngày tạo"), db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Ngày cập nhật"), db_index=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Đang hoạt động"), db_index=True)
    is_deleted = models.BooleanField(default=False, verbose_name=_("Đã xóa"), db_index=True)
   
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("IP đăng nhập cuối"))
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True, verbose_name=_("Ảnh đại diện"))
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Số điện thoại"))
    
    emergency_contact = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Liên hệ khẩn cấp"))
    emergency_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Số điện thoại khẩn cấp"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Địa chỉ"))
    department = models.ForeignKey("app_department.Department", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Khoa"), related_name="users")

    class Meta:
        app_label = "app_home"

    def __str__(self):
        return self.username
    
    def get_short_name(self):
        return self.first_name or self.username

    @property
    def is_student(self):
        return self.role == "student"

    @property
    def is_teacher(self):
        return self.role == "teacher"

    @property
    def is_admin(self):
        return self.role == "admin"


       

