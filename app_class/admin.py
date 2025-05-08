from django.contrib import admin
from .models import Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_code', 'instructor', 'start_date', 'end_date')
    search_fields = ('class_name', 'class_code', 'instructor')
    list_filter = ('start_date', 'end_date')
