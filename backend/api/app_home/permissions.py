from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from functools import lru_cache

# Hàm hỗ trợ để cache ContentType và Permission
@lru_cache(maxsize=128)
def get_permission(codename, model):
    content_type = ContentType.objects.get_for_model(model)
    return Permission.objects.filter(codename=codename, content_type=content_type).first()

class IsAdmin(BasePermission):
    """Cho phép truy cập chỉ cho người dùng có vai trò admin."""
    message = _("Only admin users are allowed to perform this action.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsTeacher(BasePermission):
    """Cho phép truy cập chỉ cho người dùng có vai trò giảng viên."""
    message = _("Only teacher users are allowed to perform this action.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher

class IsStudent(BasePermission):
    """Cho phép truy cập chỉ cho người dùng có vai trò sinh viên."""
    message = _("Only student users are allowed to perform this action.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student

class IsAdminOrReadOnly(BasePermission):
    """Cho phép đọc cho tất cả người dùng đã xác thực, ghi chỉ cho admin."""
    message = _("Only admin users can modify data.")

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == "admin"

class IsOwnerOrAdmin(BasePermission):
    """Cho phép truy cập cho chủ sở hữu đối tượng hoặc admin."""
    message = _("Only the owner or admin can perform this action.")

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            obj == request.user or request.user.role == "admin"
        )

class IsAdminOrTeacher(BasePermission):
    """Cho phép truy cập cho admin hoặc giảng viên."""
    message = _("Only admin or teacher users can perform this action.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_teacher
        )

class HasModelPermission(BasePermission):
    """Kiểm tra quyền dựa trên codename và model của view."""
    message = _("You do not have the required permission.")

    def __init__(self, codename):
        self.codename = codename

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        model = view.queryset.model if hasattr(view, "queryset") else None
        if not model:
            return False
        permission = get_permission(self.codename, model)
        if not permission:
            return False
        return request.user.has_perm(f"{permission.content_type.app_label}.{self.codename}")

# Các lớp quyền cụ thể kế thừa từ HasModelPermission
class CanManageScores(HasModelPermission):
    """Cho phép quản lý điểm số."""
    def __init__(self):
        super().__init__(codename="can_manage_scores")

class CanManageSubject(HasModelPermission):
    """Cho phép quản lý môn học."""
    def __init__(self):
        super().__init__(codename="can_manage_subject")

class CanViewSubjectScores(HasModelPermission):
    """Cho phép xem điểm số môn học."""
    def __init__(self):
        super().__init__(codename="can_view_subject_scores")

class CanViewOwnScores(BasePermission):
    """Cho phép sinh viên xem điểm số của chính họ."""
    message = _("Only students can view their own scores.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student

    def has_object_permission(self, request, view, obj):
        # Giả sử obj là bản ghi điểm số có trường user
        return hasattr(obj, "user") and obj.user == request.user