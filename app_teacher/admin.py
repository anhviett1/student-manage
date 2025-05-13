from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'first_name', 'last_name', 'email', 'faculty', 'status', 'is_active']
    list_filter = ['faculty', 'status', 'is_active']
    search_fields = ['teacher_id', 'first_name', 'last_name', 'email']
    list_per_page = 20
    ordering = ['last_name', 'first_name']
    raw_id_fields = ['user']
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'profile_picture')
        }),
        ('Địa chỉ', {
            'fields': ('address', 'city', 'state')
        }),
        ('Thông tin công việc', {
            'fields': ('faculty', 'status', 'is_active')
        }),
    )
