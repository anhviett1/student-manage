from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'semester', 'enrollment_date', 'status', 'is_active']
    list_filter = ['status', 'is_active', 'enrollment_date']
    search_fields = ['student__first_name', 'student__last_name', 'subject__name', 'notes']
    raw_id_fields = ['student', 'subject', 'semester']
    list_per_page = 20
    ordering = ['-created_at']
