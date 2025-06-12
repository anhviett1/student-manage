from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

class IsAdmin(BasePermission):
    """Allow access only to admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'

class IsTeacher(BasePermission):
    """
    Custom permission to only allow teachers to access the view.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'teacher') 

class IsStudent(BasePermission):
    """
    Custom permission to only allow students to access the view.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'student')

class IsAdminOrReadOnly(BasePermission):
    """Allow read-only access for all, write access for admins."""
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'

class IsOwnerOrAdmin(BasePermission):
    """Allow access to owners or admins."""
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            (obj == request.user or getattr(request.user, 'role', None) == 'admin')
        )

class IsAdminOrTeacher(BasePermission):
    """
    Custom permission to only allow admin or teacher users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and (getattr(request.user, 'is_admin', False) or getattr(request.user, 'is_teacher', False))

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

class CanManageSubject(BasePermission):
    """
    Cho phép người dùng quản lý môn học.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        content_type = ContentType.objects.get_for_model(view.model)
        permission = Permission.objects.filter(
            codename='can_manage_subject',
            content_type=content_type
        ).first()
        return permission and request.user.has_perm(f'{content_type.app_label}.can_manage_subject')

class CanViewSubjectScores(BasePermission):
    """
    Cho phép người dùng xem điểm số của môn học.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        content_type = ContentType.objects.get_for_model(view.model)
        permission = Permission.objects.filter(
            codename='can_view_subject_scores',
            content_type=content_type
        ).first()
        return permission and request.user.has_perm(f'{content_type.app_label}.can_view_subject_scores')



