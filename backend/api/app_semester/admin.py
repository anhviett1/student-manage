from django.contrib import admin
from .models import Semester


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = [
        "semester_id",
        "semester_name",
        "academic_year",
        "start_date",
        "end_date",
        "status",
        "total_credits",
        "is_active",
        "is_deleted",
        "created_at",
    ]
    list_filter = [
        "status",
        "is_active",
        "is_deleted",
        "academic_year",
        ("start_date", admin.DateFieldListFilter),
        ("end_date", admin.DateFieldListFilter),
    ]
    search_fields = ["semester_id", "semester_name", "academic_year", "description", "notes"]
    ordering = ["-start_date"]
    list_per_page = 20
    actions = ["soft_delete"]

    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, "Đã xóa mềm các học kỳ được chọn.")

    soft_delete.short_description = "Xóa mềm các học kỳ được chọn"
