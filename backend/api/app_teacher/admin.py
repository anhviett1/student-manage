from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'first_name', 'last_name', 'email', 'status', 'is_active']
    list_filter = [ 'status', 'is_active']
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
