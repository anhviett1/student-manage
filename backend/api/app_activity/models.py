from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ("login", "Đăng nhập"),
        ("logout", "Đăng xuất"),
        ("create", "Tạo mới"),
        ("update", "Cập nhật"),
        ("delete", "Xóa"),
        ("view", "Xem"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    content_type = models.CharField(max_length=100, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Ngày tạo", null=False, blank=False
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Ngày cập nhật", null=False, blank=False
    )

    class Meta:
        verbose_name = "Hoạt động"
        verbose_name_plural = "Hoạt động"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} - {self.created_at}"
