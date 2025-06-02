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

class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow students to access the view.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'student')

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner or admin
        return obj.user == request.user or request.user.is_staff

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



