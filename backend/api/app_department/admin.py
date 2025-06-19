from django.contrib import admin
from .models import Department
from django.utils.translation import gettext_lazy as _

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "is_deleted", "created_at", "updated_at")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("name", "code")
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "code", "description")}),
        (_("Status"), {"fields": ("is_active", "is_deleted")}),
        (_("Metadata"), {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        return self.model.objects.all()

    def soft_delete(self, request, queryset):
        for dept in queryset:
            dept.soft_delete()
        self.message_user(request, _("Selected departments have been soft deleted."))

    soft_delete.short_description = _("Soft delete selected departments")

    def restore(self, request, queryset):
        for dept in queryset:
            dept.restore()
        self.message_user(request, _("Selected departments have been restored."))

    restore.short_description = _("Restore selected departments")

    actions = ["soft_delete", "restore"]

    def has_delete_permission(self, request, obj=None):
        return False
