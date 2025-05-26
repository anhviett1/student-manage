from django.contrib import admin
from .models import Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_id', 'name', 'status', 'is_active', 'created_at']
    list_filter = [ 'status', 'is_active']
    search_fields = ['class_id', 'name', 'description']
    raw_id_fields = ['semester', 'subject', 'teacher']
    list_per_page = 20
    ordering = ['-created_at']
