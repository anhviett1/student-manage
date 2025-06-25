from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["subject_id", "subject_name", "credits", "status", "is_active", "is_deleted"]
    list_filter = ["status", "is_active", "is_deleted"]
    search_fields = ["subject_id", "subject_name", "description"]
    list_per_page = 20
    ordering = ["subject_name"]
    actions = ["soft_delete"]

    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, "Đã xóa mềm các môn học được chọn.")

    soft_delete.short_description = "Xóa mềm các môn học được chọn"
