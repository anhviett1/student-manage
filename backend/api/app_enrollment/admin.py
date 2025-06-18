from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'semester', 'enrollment_date', 'status', 'is_active', 'is_deleted']
    list_filter = ['status', 'is_active', 'enrollment_date', 'is_deleted']
    search_fields = ['student__first_name', 'student__last_name', 'subject__name', 'notes']
    raw_id_fields = ['student', 'subject', 'semester']
    list_per_page = 20
    ordering = ['-created_at']
    actions = ['soft_delete']

    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, 'Đã xóa mềm các đăng ký được chọn.')
    soft_delete.short_description = 'Xóa mềm các đăng ký được chọn'
