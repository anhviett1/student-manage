from django.contrib import admin
from .models import Department
from .forms import DepartmentForm  

from django.utils.translation import gettext_lazy as _

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    form = DepartmentForm  # ✅ thêm dòng này

    list_display = (
        "department_id", "department_name", "is_active", "is_deleted", "created_at", "updated_at"
    )
    list_filter = ("is_active", "is_deleted")
    search_fields = ("department_id", "department_name")
    ordering = ("department_name",)

    fieldsets = (
        (None, {"fields": ("department_name", "description")}),
        (_("Status"), {"fields": ("is_active", "is_deleted")}),
        (_("Metadata"), {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        return self.model.objects.all()

    def soft_delete(self, request, queryset):
        for dept in queryset:
            dept.is_deleted = True
            dept.is_active = False
            dept.save()
        self.message_user(request, _("Đã xóa mềm các khoa được chọn."))

    soft_delete.short_description = _("Xóa mềm các khoa được chọn")

    def restore(self, request, queryset):
        for dept in queryset:
            dept.is_deleted = False
            dept.is_active = True
            dept.save()
        self.message_user(request, _("Đã khôi phục các khoa được chọn."))

    restore.short_description = _("Khôi phục các khoa được chọn")

    actions = ["soft_delete", "restore"]

    def has_delete_permission(self, request, obj=None):
        return False
