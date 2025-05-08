from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'subject_name', 'subject_code', 'teacher')
    search_fields = ('subject_name', 'subject_code')
    list_filter = ('teacher',)
    raw_id_fields = ('teacher',)
