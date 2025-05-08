from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'class_id', 'enrollment_date', 'status')
    search_fields = ('student__first_name', 'student__last_name', 'class_id__class_name')
    list_filter = ('status', 'enrollment_date')
    raw_id_fields = ('student', 'class_id')
