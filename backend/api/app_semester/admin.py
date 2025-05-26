from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Semester

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    # List display configuration
    list_display = [
        'semester_id', 
        'name', 
        'academic_year',
        'start_date', 
        'end_date',
        'status',
        'total_credits',
        'is_active',
        'created_at',
        'created_by'
    ]
    
    # List filter configuration
    list_filter = [
        'status',
        'is_active',
        'academic_year',
        ('start_date', admin.DateFieldListFilter),
        ('end_date', admin.DateFieldListFilter),
    ]
    
    # Search fields configuration
    search_fields = [
        'semester_id',
        'name',
        'academic_year',
        'description',
        'notes'
    ]
    
    # Fieldsets for the edit form
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': (
                'semester_id',
                'name',
                'academic_year',
                'status',
                'is_active'
            )
        }),
        ('Thời gian', {
            'fields': (
                'start_date',
                'end_date',
                'registration_start',
                'registration_end',
                'add_drop_deadline'
            )
        }),
        ('Thông tin học tập', {
            'fields': (
                'total_credits',
                'min_credits',
                'max_credits'
            )
        }),
        ('Thông tin tài chính', {
            'fields': (
                'tuition_deadline',
                'late_fee_start',
                'late_fee_amount'
            )
        }),
        ('Thông tin bổ sung', {
            'fields': (
                'description',
                'notes'
            ),
            'classes': ('collapse',)
        }),
        ('Thông tin hệ thống', {
            'fields': (
                'created_at',
                'updated_at',
                'created_by',
                'updated_by'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    
    # List editable fields
    list_editable = [
        'is_active',
        'status'
    ]
    
    # List display links
    list_display_links = [
        'semester_id',
        'name'
    ]
    
    # Pagination
    list_per_page = 20
    
    # Ordering
    ordering = ['-start_date']
    
    # Date hierarchy
    date_hierarchy = 'start_date'
    
    # Actions
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} học kỳ đã được kích hoạt.')
    make_active.short_description = "Kích hoạt các học kỳ đã chọn"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} học kỳ đã được vô hiệu hóa.')
    make_inactive.short_description = "Vô hiệu hóa các học kỳ đã chọn"
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/semester_admin.css',)
        }
        js = ('admin/js/semester_admin.js',)

