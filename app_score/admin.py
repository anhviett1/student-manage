from django.contrib import admin
from .models import Score

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'score', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'subject__subject_name')
    list_filter = ('subject', 'enrollment')
    raw_id_fields = ('student', 'subject', 'enrollment')
