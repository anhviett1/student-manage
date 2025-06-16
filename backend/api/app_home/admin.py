from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from datetime import date
from .models import User, Department
from ..app_student.models import Student


class UserAdminForm(forms.ModelForm):
    student_id = forms.CharField(max_length=20, required=False, label=_('Mã sinh viên'))
    enrollment_date = forms.DateField(required=False, label=_('Ngày nhập học'), initial=date.today)
    department = forms.ModelChoiceField(queryset=Department.objects.filter(is_deleted=False), required=False, label=_('Khoa'))

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        student_id = cleaned_data.get('student_id')
        enrollment_date = cleaned_data.get('enrollment_date')
        department = cleaned_data.get('department')

        if role == 'student':
            if not student_id:
                self.add_error('student_id', _('Mã sinh viên là bắt buộc khi vai trò là sinh viên.'))
            if not enrollment_date:
                self.add_error('enrollment_date', _('Ngày nhập học là bắt buộc khi vai trò là sinh viên.'))
            if not department:
                self.add_error('department', _('Khoa là bắt buộc khi vai trò là sinh viên.'))
        return cleaned_data


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    list_display = ('username', 'email', 'role', 'is_active', 'is_deleted', 'created_at', 'updated_at')
    list_filter = ('role', 'is_active', 'is_deleted', 'department')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email', 'role', 'phone_number', 'address', 'profile_picture')}),
        (_('Emergency Contact'), {'fields': ('emergency_contact', 'emergency_phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Metadata'), {'fields': ('last_login_ip', 'created_at', 'updated_at', 'is_deleted')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'role',
                'first_name', 'last_name', 'phone_number', 'department'
            ),
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login_ip')

    def get_queryset(self, request):
        return self.model.objects.all()

    def soft_delete(self, request, queryset):
        for user in queryset:
            user.soft_delete()
            if hasattr(user, 'student'):
                user.student.soft_delete(user=request.user)
        self.message_user(request, _("Selected users have been soft deleted."))
    soft_delete.short_description = _("Soft delete selected users")

    def restore(self, request, queryset):
        for user in queryset:
            user.restore()
            if hasattr(user, 'student'):
                user.student.restore(user=request.user)
        self.message_user(request, _("Selected users have been restored."))
    restore.short_description = _("Restore selected users")

    actions = ['soft_delete', 'restore']

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change and obj.role == 'student':
            super().save_model(request, obj, form, change)
            try:
                Student.objects.create(
                    user=obj,
                    student_id=form.cleaned_data['student_id'],
                    first_name=obj.first_name,
                    last_name=obj.last_name,
                    email=obj.email,
                    phone=obj.phone_number,
                    date_of_birth=date.today(),
                    enrollment_date=form.cleaned_data['enrollment_date'],
                    department=form.cleaned_data['department'],
                    is_active=obj.is_active,
                    created_by=obj
                )
            except Exception as e:
                self.message_user(request, _(f"Lỗi khi tạo sinh viên: {str(e)}"), level='error')
        elif change and obj.role == 'student' and hasattr(obj, 'student'):
            student = obj.student
            student.first_name = obj.first_name
            student.last_name = obj.last_name
            student.email = obj.email
            student.phone = obj.phone_number
            student.is_active = obj.is_active
            student.save()
        super().save_model(request, obj, form, change)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
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
        return self.model.objects.all()

    def soft_delete(self, request, queryset):
        for dept in queryset:
            dept.soft_delete()
        self.message_user(request, _("Selected departments have been soft deleted."))
    soft_delete.short_description = _("Soft delete selected departments")

    def restore(self, request, queryset):
        for dept in queryset:
            dept.restore()
        self.message_user(request, _("Selected departments have been restored."))
    restore.short_description = _("Restore selected departments")

    actions = ['soft_delete', 'restore']

    def has_delete_permission(self, request, obj=None):
        return False
