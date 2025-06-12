from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Department


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for custom User model
    """
    list_display = ('username', 'email', 'role', 'is_active', 'is_deleted', 'created_at', 'updated_at')
    list_filter = ('role', 'is_active', 'is_deleted', 'department')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email', 'role', 'phone_number', 'address', 'profile_picture')}),
        (_('Department'), {'fields': ('department',)}),
        (_('Emergency Contact'), {'fields': ('emergency_contact', 'emergency_phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Metadata'), {'fields': ('last_login_ip', 'created_at', 'updated_at', 'is_deleted')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'first_name', 'last_name', 'phone_number', 'department'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login_ip')
    
    def get_queryset(self, request):
        # Show all users, including soft-deleted ones
        return self.model.objects.all()
    
    def soft_delete(self, request, queryset):
        """Soft delete selected users"""
        for user in queryset:
            user.soft_delete()
        self.message_user(request, _("Selected users have been soft deleted."))
    soft_delete.short_description = _("Soft delete selected users")
    
    def restore(self, request, queryset):
        """Restore soft-deleted users"""
        for user in queryset:
            user.restore()
        self.message_user(request, _("Selected users have been restored."))
    restore.short_description = _("Restore selected users")
    
    actions = ['soft_delete', 'restore']
    
    def has_delete_permission(self, request, obj=None):
        # Disable hard delete, encourage soft delete
        return False


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Department model
    """
    list_display = ('name', 'code', 'is_active', 'is_deleted', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('name', 'code')
    ordering = ('name',)
    
    fieldsets = (
        (None, {'fields': ('name', 'code', 'description')}),
        (_('Status'), {'fields': ('is_active', 'is_deleted')}),
        (_('Metadata'), {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        # Show all departments, including soft-deleted ones
        return self.model.objects.all()
    
    def soft_delete(self, request, queryset):
        """Soft delete selected departments"""
        for dept in queryset:
            dept.soft_delete()
        self.message_user(request, _("Selected departments have been soft deleted."))
    soft_delete.short_description = _("Soft delete selected departments")
    
    def restore(self, request, queryset):
        """Restore soft-deleted departments"""
        for dept in queryset:
            dept.restore()
        self.message_user(request, _("Selected departments have been restored."))
    restore.short_description = _("Restore selected departments")
    
    actions = ['soft_delete', 'restore']
    
    def has_delete_permission(self, request, obj=None):
        # Disable hard delete, encourage soft delete
        return False
