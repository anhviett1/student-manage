from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('is_deleted',)
    raw_id_fields = ('user',)
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')
        }),
        ('Địa chỉ', {
            'fields': ('address', 'city', 'state')
        }),
        ('Thông tin học tập', {
            'fields': ('class_assigned', 'subjects')
        }),
        ('Trạng thái', {
            'fields': ('is_deleted', 'deleted_at', 'deleted_by')
        }),
    )
