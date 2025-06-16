from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'full_name', 'email', 'phone', 'department', 'status', 'is_active', 'is_deleted', 'created_at', 'updated_at'
    )
    list_filter = ('status', 'is_active', 'is_deleted', 'department', 'gender')
    search_fields = ('student_id', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('student_id',)

    fieldsets = (
        (_('User Info'), {
            'fields': ('user', 'student_id', 'first_name', 'last_name', 'email', 'phone')
        }),
        (_('Personal Info'), {
            'fields': ('date_of_birth', 'gender', 'profile_picture', 'blood_type', 'medical_conditions', 'allergies')
        }),
        (_('Address'), {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        (_('Academic Info'), {
            'fields': ('department', 'major', 'minor', 'status', 'enrollment_date', 'graduation_date', 'gpa', 'credits_earned', 'credits_attempted')
        }),
        (_('Emergency Contact'), {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        (_('Metadata'), {
            'fields': ('is_active', 'is_deleted', 'created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_by')
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_by')

    def get_queryset(self, request):
        return self.model.objects.all()

    def soft_delete(self, request, queryset):
        for student in queryset:
            student.soft_delete(user=request.user)
            student.user.soft_delete()
        self.message_user(request, _("Selected students have been soft deleted."))
    soft_delete.short_description = _("Soft delete selected students")

    def restore(self, request, queryset):
        for student in queryset:
            student.restore(user=request.user)
            student.user.restore()
        self.message_user(request, _("Selected students have been restored."))
    restore.short_description = _("Restore selected students")

    actions = ['soft_delete', 'restore']

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.user.first_name = obj.first_name
        obj.user.last_name = obj.last_name
        obj.user.email = obj.email
        obj.user.phone_number = obj.phone
        obj.user.is_active = obj.is_active
        obj.user.save()
        super().save_model(request, obj, form, change)
