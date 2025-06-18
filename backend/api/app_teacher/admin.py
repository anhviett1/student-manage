from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'first_name', 'last_name', 'email', 'status', 'is_active', 'is_deleted']
    list_filter = [ 'status', 'is_active', 'is_deleted']
    search_fields = ['teacher_id', 'first_name', 'last_name', 'email']
    list_per_page = 20
    ordering = ['last_name', 'first_name']
    raw_id_fields = ['user']
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('user', 'teacher_id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Địa chỉ', {
            'fields': ('address',)
        }),
        ('Thông tin chuyên môn', {
            'fields': ( 'degree', 'specialization', 'years_of_experience')
        }),
        ('Thông tin hệ thống', {
            'fields': ('status', 'is_active')
        }),
    )
    actions = ['soft_delete']

    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, 'Đã xóa mềm các giảng viên được chọn.')
    soft_delete.short_description = 'Xóa mềm các giảng viên được chọn'
