from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from functools import lru_cache
from django.utils.translation import gettext_lazy as _

ADMIN_ROLES = ['admin', 'superuser']

# ================================
# 1. Role-based permissions
# ================================

class RolePermission(BasePermission):
    """Permission kiểm tra vai trò (role)."""
    roles = []

    def has_permission(self, request, view):
        # Superuser của Django có mọi quyền, không cần kiểm tra vai trò
        if request.user.is_superuser:
            return True
        return (
            request.user.is_authenticated and
            getattr(request.user, 'role', None) in self.roles
        )

def make_role_permission_class(role_list, message):
    """Factory tạo permission theo role."""
    return type(
        f"Is{'Or'.join(r.capitalize() for r in role_list)}",
        (RolePermission,),
        {"roles": role_list, "message": _(message)}
    )

# Cụ thể hóa
IsAdmin = make_role_permission_class(ADMIN_ROLES, "Only admin users are allowed.")
IsTeacher = make_role_permission_class(['teacher'], "Only teacher users are allowed.")
IsStudent = make_role_permission_class(['student'], "Only student users are allowed.")
IsAdminOrTeacher = make_role_permission_class(ADMIN_ROLES + ['teacher'], "Only admin or teacher users are allowed.")

# ================================
# 2. Read-only for authenticated users, write for admin
# ================================

class IsAdminOrReadOnly(BasePermission):
    message = _("Only admin users can modify data.")

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_superuser or
            getattr(request.user, 'role', '') in ADMIN_ROLES
        )

# ================================
# 3. Object-level: is owner or admin
# ================================

class IsOwnerOrAdmin(BasePermission):
    message = _("Only the owner or admin can access this object.")

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, 'role', '') in ADMIN_ROLES
        return request.user.is_authenticated and (
            obj == request.user or
            getattr(obj, 'user', None) == request.user or
            is_admin
        )

# ================================
# 4. Model permission (dynamic by codename)
# ================================

@lru_cache(maxsize=128)
def get_permission(codename, model_cls):
    content_type = ContentType.objects.get_for_model(model_cls)
    return Permission.objects.filter(codename=codename, content_type=content_type).first()

class HasModelPermission(BasePermission):
    message = _("You do not have the required permission.")

    def __init__(self, codename=None):
        self.codename = codename

    def has_permission(self, request, view):
        if not (request.user.is_authenticated and self.codename):
            return False

        model = getattr(getattr(view, 'queryset', None), 'model', None)
        if not model:
            return False

        perm = get_permission(self.codename, model)
        if not perm:
            return False

        return request.user.has_perm(f"{perm.content_type.app_label}.{self.codename}")

# ================================
# 5. Factory tạo các quyền cụ thể theo codename
# ================================

def make_model_permission_class(name, codename, message=None):
    return type(
        name,
        (HasModelPermission,),
        {
            "__init__": lambda self: super(type(self), self).__init__(codename=codename),
            "message": _(message or f"You need `{codename}` permission.")
        }
    )

# Các quyền cụ thể
CanManageScores = make_model_permission_class("CanManageScores", "can_manage_scores")
CanManageSubjects = make_model_permission_class("CanManageSubjects", "can_manage_subjects")
CanViewSubjectScores = make_model_permission_class("CanViewSubjectScores", "can_view_subject_scores")

# ================================
# 6. Sinh viên xem điểm của chính mình
# ================================

class CanViewOwnScores(BasePermission):
    message = _("Only students can view their own scores.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', '') == 'student'

    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'user') and obj.user == request.user
