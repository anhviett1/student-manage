from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'phone', 'faculty', 'status', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('faculty', 'status', 'is_active', 'is_deleted')
    raw_id_fields = ('user',)
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Địa chỉ', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Thông tin học tập', {
            'fields': ('faculty', 'status', 'major', 'minor', 'gpa', 'enrollment_date', 'graduation_date')
        }),
        ('Thông tin hệ thống', {
            'fields': ('is_active', 'is_deleted')
        }),
    )
