from django.db import models
from django.utils.translation import gettext_lazy as _
from ..app_home.models import User

# Create your models here.
class Department(models.Model):
    department_id = models.AutoField(primary_key=True, verbose_name=_("ID khoa"))
    department_name= models.CharField(max_length=200, verbose_name=_("Tên khoa"), null=False, blank=False)
    description = models.TextField(blank=True, null=True, verbose_name=_("Mô tả"))
    is_active = models.BooleanField(default=True, verbose_name=_("Đang hoạt động"))
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Ngày tạo"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Ngày cập nhật"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Đã xóa"))
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, verbose_name=_("Trưởng khoa"), related_name="headed_departments",)

    def __str__(self):
        return self.department_name

    class Meta:
        app_label = "app_department"
