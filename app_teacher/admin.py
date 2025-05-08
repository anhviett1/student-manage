from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'first_name', 'last_name', 'email', 'phone_number', 'subject')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'subject')
    list_filter = ('subject',)
    raw_id_fields = ('user',)
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')
        }),
        ('Địa chỉ', {
            'fields': ('address', 'city', 'state')
        }),
        ('Thông tin công việc', {
            'fields': ('subject', 'salary')
        }),
    )
