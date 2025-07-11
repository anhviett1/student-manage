from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from functools import lru_cache
from django.utils.translation import gettext_lazy as _

# Định nghĩa các role
ADMIN_ROLES = ["admin"]
TEACHER_ROLES = ["teacher"]
STUDENT_ROLES = ["student"]


# ===== Role-based Permission =====
class RolePermission(BasePermission):
    roles = []

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, "role", None) in self.roles
        )


def make_role_permission_class(role_list, message):
    return type(
        f"Is{'Or'.join(r.capitalize() for r in role_list)}",
        (RolePermission,),
        {"roles": role_list, "message": _(message)},
    )


IsAdmin = make_role_permission_class(ADMIN_ROLES, "Chỉ admin được phép.")
IsTeacher = make_role_permission_class(TEACHER_ROLES, "Chỉ giáo viên được phép.")
IsStudent = make_role_permission_class(STUDENT_ROLES, "Chỉ học sinh được phép.")
IsAdminOrTeacher = make_role_permission_class(
    ADMIN_ROLES + TEACHER_ROLES, "Chỉ admin hoặc giáo viên."
)
IsAdminOrStudent = make_role_permission_class(
    ADMIN_ROLES + STUDENT_ROLES, "Chỉ admin hoặc học sinh."
)
IsTeacherOrStudent = make_role_permission_class(
    TEACHER_ROLES + STUDENT_ROLES, "Chỉ giáo viên hoặc học sinh."
)
IsAllRoles = make_role_permission_class(
    ADMIN_ROLES + TEACHER_ROLES + STUDENT_ROLES, "Chỉ admin, giáo viên hoặc học sinh."
)


# ===== Admin or ReadOnly =====
class IsAdminOrReadOnly(BasePermission):
    message = _("Chỉ admin được chỉnh sửa.")

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        )


# ===== Owner or Admin =====
class IsOwnerOrAdmin(BasePermission):
    message = _("Chỉ chủ sở hữu hoặc admin.")

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        return request.user.is_authenticated and (
            obj == request.user or getattr(obj, "user", None) == request.user or is_admin
        )


# ===== Teacher or Admin for Specific Objects =====
class IsTeacherOrAdminForAssigned(BasePermission):
    message = _("Chỉ admin hoặc giáo viên được phân công.")

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        is_assigned_teacher = (
            getattr(request.user, "role", "") in TEACHER_ROLES
            and hasattr(obj, "teacher")
            and obj.teacher == request.user
        )
        return request.user.is_authenticated and (is_admin or is_assigned_teacher)


# ===== Student or Admin for Specific Objects =====
class IsStudentOrAdminForAssigned(BasePermission):
    message = _("Chỉ admin hoặc học sinh được phân công.")

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        is_assigned_student = (
            getattr(request.user, "role", "") in STUDENT_ROLES
            and hasattr(obj, "student")
            and obj.student == request.user
        )
        return request.user.is_authenticated and (is_admin or is_assigned_student)


# ===== Django-style Model Permission =====
@lru_cache(maxsize=128)
def get_permission(codename, model_cls):
    content_type = ContentType.objects.get_for_model(model_cls)
    return Permission.objects.filter(codename=codename, content_type=content_type).first()


class HasModelPermission(BasePermission):
    message = _("Không có quyền.")

    def __init__(self, codename=None):
        self.codename = codename

    def has_permission(self, request, view):
        if not (request.user.is_authenticated and self.codename):
            return False

        model = getattr(getattr(view, "queryset", None), "model", None)
        if not model:
            return False

        perm = get_permission(self.codename, model)
        if not perm:
            return False

        return request.user.has_perm(f"{perm.content_type.app_label}.{self.codename}")


def make_model_permission_class(name, codename, message=None):
    return type(
        name,
        (HasModelPermission,),
        {
            "__init__": lambda self: super(type(self), self).__init__(codename=codename),
            "message": _(message or f"Cần quyền `{codename}`."),
        },
    )


# ===== Application-specific Permissions =====
# 1. app_home – Quản lý hồ sơ người dùng
class ProfilePermission(BasePermission):
    message = _("Chỉ admin hoặc chủ sở hữu hồ sơ được phép chỉnh sửa.")

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        is_owner = obj == request.user or getattr(obj, "user", None) == request.user
        return request.user.is_authenticated and (is_admin or is_owner)


# 2. app_student – Quản lý học sinh
StudentAddPermission = make_model_permission_class(
    "StudentAddPermission", "add_student", "Cần quyền thêm học sinh."
)
StudentChangePermission = make_model_permission_class(
    "StudentChangePermission", "change_student", "Cần quyền sửa học sinh."
)
StudentDeletePermission = make_model_permission_class(
    "StudentDeletePermission", "delete_student", "Cần quyền xóa học sinh."
)

# 3. app_teacher – Quản lý giáo viên
TeacherAddPermission = make_model_permission_class(
    "TeacherAddPermission", "add_teacher", "Cần quyền thêm giáo viên."
)
TeacherChangePermission = make_model_permission_class(
    "TeacherChangePermission", "change_teacher", "Cần quyền sửa giáo viên."
)
TeacherDeletePermission = make_model_permission_class(
    "TeacherDeletePermission", "delete_teacher", "Cần quyền xóa giáo viên."
)


# 4. app_class – Quản lý lớp học
class ClassPermission(BasePermission):
    message = _("Chỉ admin, giáo viên hoặc học sinh được phân công.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or getattr(request.user, "role", "") in (ADMIN_ROLES + TEACHER_ROLES + STUDENT_ROLES)
        )

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        is_teacher = (
            getattr(request.user, "role", "") in TEACHER_ROLES and obj.teacher == request.user
        )
        is_student = (
            getattr(request.user, "role", "") in STUDENT_ROLES
            and request.user in obj.students.all()
        )
        return request.user.is_authenticated and (is_admin or is_teacher or is_student)


# 5. app_department – Quản lý khoa
class DepartmentPermission(IsAdminOrReadOnly):
    message = _("Chỉ admin được chỉnh sửa, các vai trò khác chỉ được xem.")


# 6. app_subject – Quản lý môn học
class SubjectPermission(BasePermission):
    message = _("Chỉ admin hoặc giáo viên được phân công.")

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        )

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        is_teacher = (
            getattr(request.user, "role", "") in TEACHER_ROLES and obj.teacher == request.user
        )
        return request.user.is_authenticated and (
            is_admin or is_teacher or request.method in SAFE_METHODS
        )


# 7. app_score – Quản lý điểm
class ScorePermission(BasePermission):
    message = _("Chỉ admin, giáo viên hoặc học sinh được phân công.")

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        is_teacher = (
            getattr(request.user, "role", "") in TEACHER_ROLES
            and obj.subject.teacher == request.user
        )
        is_student = (
            getattr(request.user, "role", "") in STUDENT_ROLES and obj.student == request.user
        )
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated and (is_admin or is_teacher or is_student)
        return request.user.is_authenticated and (is_admin or is_teacher)


# 8. app_schedule – Lịch học và lịch thi
class SchedulePermission(BasePermission):
    message = _("Chỉ admin, giáo viên hoặc học sinh được phân công.")

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        )

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        is_teacher = (
            getattr(request.user, "role", "") in TEACHER_ROLES
            and obj.subject.teacher == request.user
        )
        is_student = (
            getattr(request.user, "role", "") in STUDENT_ROLES
            and request.user in obj.class_room.students.all()
        )
        return request.user.is_authenticated and (is_admin or is_teacher or is_student)


# 9. app_enrollment – Đăng ký học
class EnrollmentPermission(BasePermission):
    message = _("Chỉ admin, giáo viên hoặc học sinh được phép.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or getattr(request.user, "role", "") in (ADMIN_ROLES + TEACHER_ROLES + STUDENT_ROLES)
        )

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        is_teacher = (
            getattr(request.user, "role", "") in TEACHER_ROLES
            and obj.subject.teacher == request.user
        )
        is_student = (
            getattr(request.user, "role", "") in STUDENT_ROLES and obj.student == request.user
        )
        return request.user.is_authenticated and (is_admin or is_teacher or is_student)


# 10. app_semester – Quản lý học kỳ
class SemesterPermission(IsAdminOrReadOnly):
    message = _("Chỉ admin được chỉnh sửa, các vai trò khác chỉ được xem.")


# 11. app_activity – Hoạt động ngoại khóa
class ActivityPermission(BasePermission):
    message = _("Chỉ admin, giáo viên hoặc học sinh được phân công.")

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or getattr(request.user, "role", "") in (ADMIN_ROLES + TEACHER_ROLES + STUDENT_ROLES)
        )

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_superuser or getattr(request.user, "role", "") in ADMIN_ROLES
        is_teacher = (
            getattr(request.user, "role", "") in TEACHER_ROLES and obj.created_by == request.user
        )
        is_student = (
            getattr(request.user, "role", "") in STUDENT_ROLES
            and request.user in obj.participants.all()
        )
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated and (is_admin or is_teacher or is_student)
        return request.user.is_authenticated and (is_admin or is_teacher)
