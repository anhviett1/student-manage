from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'phone', 'department', 'status', 'is_active')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    list_filter = ('department', 'status', 'is_active', 'is_deleted')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('student_id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Thông tin địa chỉ', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Thông tin học tập', {
            'fields': ('department', 'status', 'major', 'minor', 'gpa', 'enrollment_date', 'graduation_date')
        }),
        ('Thông tin liên hệ khẩn cấp', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Thông tin bổ sung', {
            'fields': ('profile_picture', 'blood_type', 'medical_conditions', 'allergies')
        }),
        ('Thông tin hệ thống', {
            'fields': ('is_active', 'created_at', 'updated_at', 'deleted_at', 'deleted_by', 'is_deleted')
        }),
    )
