from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow teachers to access the view.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'teacher') 

class CanManageScores(BasePermission):
    """
    Cho phép người dùng quản lý điểm số nếu họ có quyền 'can_manage_scores'.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        content_type = ContentType.objects.get_for_model(view.model)
        permission = Permission.objects.filter(
            codename='can_manage_scores',
            content_type=content_type
        ).first()
        return permission and request.user.has_perm(f'{content_type.app_label}.can_manage_scores')

class CanViewOwnScores(BasePermission):
    """
    Cho phép người dùng xem điểm số của chính họ.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student