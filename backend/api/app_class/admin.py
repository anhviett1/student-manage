from django.contrib import admin
from .models import Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_id', 'name', 'status', 'is_active', 'created_at', 'is_deleted']
    list_filter = [ 'status', 'is_active', 'is_deleted']
    search_fields = ['class_id', 'name', 'description']
    raw_id_fields = ['semester', 'subject', 'teacher']
    list_per_page = 20
    ordering = ['-created_at']
    actions = ['soft_delete']

    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, 'Đã xóa mềm các lớp học được chọn.')
    soft_delete.short_description = 'Xóa mềm các lớp học được chọn'
