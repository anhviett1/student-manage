from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_id', 'name', 'credits', 'status', 'is_active']
    list_filter = [ 'status', 'is_active']
    search_fields = ['subject_id', 'name', 'description']
    list_per_page = 20
    ordering = ['name']
