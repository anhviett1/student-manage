from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.db.models import Q, Count
from django.contrib.auth.models import Permission
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import csv, os
import logging
from drf_spectacular.utils import extend_schema
from ..app_department.models import Department
from ..app_score.models import Score
from ..app_score.serializers import ScoreSerializer
from .models import User
from .serializers import UserSerializer
from .permissions import (
    IsAdmin,
    IsAdminOrTeacher,
    ProfilePermission,
    ScorePermission,

)

logger = logging.getLogger(__name__)


@extend_schema(tags=["Users"])
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet quản lý người dùng."""

    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action == "register":
            return [AllowAny()]
        if self.action in ["retrieve", "update", "partial_update"]:
            return [ProfilePermission()]  # Sử dụng ProfilePermission cho hồ sơ người dùng
        if self.action == "change_role":
            return [IsAdmin()]  # Chỉ admin được thay đổi vai trò
        return super().get_permissions()

    def get_queryset(self):
        """Lọc người dùng dựa trên tham số truy vấn."""
        if not self.request.user.is_authenticated:
            return User.objects.none()

        # Admin có thể xem tất cả users
        if self.request.user.is_superuser or getattr(self.request.user, "role", "") in ["admin"]:
            queryset = User.objects.filter(is_deleted=False)
        else:
            # Non-admin chỉ có thể xem chính mình
            queryset = User.objects.filter(id=self.request.user.id, is_deleted=False)

        # Apply filters
        filters = Q()
        search_term = self.request.query_params.get("search", "")
        role_filter = self.request.query_params.get("role", "")
        department_filter = self.request.query_params.get("department", "")
        status_filter = self.request.query_params.get("status", "")

        if search_term:
            filters &= (
                Q(username__icontains=search_term)
                | Q(first_name__icontains=search_term)
                | Q(last_name__icontains=search_term)
                | Q(email__icontains=search_term)
            )

        if role_filter:
            role_list = role_filter.split(",") if role_filter else []
            if role_list:
                filters &= Q(role__in=role_list)

        if department_filter:
            department_list = [int(id) for id in department_filter.split(",") if id.isdigit()]
            if department_list:
                filters &= Q(department__id__in=department_list)

        if status_filter:
            status_list = status_filter.split(",") if status_filter else ["active"]
            if status_list:
                filters &= Q(is_active__in=[s == "active" for s in status_list])

        return queryset.filter(filters).distinct().order_by("-created_at")

    def perform_create(self, serializer):
        """Tạo người dùng mới và mã hóa mật khẩu nếu có."""
        user = serializer.save()
        password = self.request.data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return user

    def perform_update(self, serializer):
        """Cập nhật người dùng và lưu last_login_ip nếu có."""
        user = serializer.save()
        if "last_login_ip" in self.request.data:
            user.update_last_login_ip(self.request.data["last_login_ip"])
        return user

    def perform_destroy(self, instance):
        """Xóa mềm người dùng."""
        instance.soft_delete()

    @action(detail=True, methods=["put"], url_path="change-role")
    def change_role(self, request, pk=None):
        user = self.get_object()
        new_role = request.data.get("role")
        if new_role not in dict(User.ROLE_CHOICES):
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        user.role = new_role
        user.save(update_fields=["role"])
        return Response({"message": "Role updated successfully"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Users"])
class LogoutAPIView(APIView):
    """API để đăng xuất người dùng."""

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request):
        """Đăng xuất người dùng và thêm token vào danh sách đen nếu dùng JWT."""
        if hasattr(request.auth, "blacklist"):
            request.auth.blacklist()  # Vô hiệu hóa JWT token
        logout(request)  # Đăng xuất session
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Users"])
class ProfileAPIView(APIView):
    permission_classes = [ProfilePermission]  # Chỉ admin hoặc chủ sở hữu hồ sơ
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated successfully", "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        """Cập nhật người dùng và lưu last_login_ip nếu có."""
        user = serializer.save()
        if "last_login_ip" in self.request.data:
            user.update_last_login_ip(self.request.data["last_login_ip"])
        return user


@extend_schema(tags=["Users"])
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Chỉ người dùng đã đăng nhập
    serializer_class = UserSerializer

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not check_password(old_password, user.password):
            return Response(
                {"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"error": "New password and confirm password do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(new_password) < 8:
            return Response(
                {"error": "New password must be at least 8 characters long"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Users"])
class AvatarUploadView(APIView):
    permission_classes = [ProfilePermission]  # Chỉ admin hoặc chủ sở hữu hồ sơ
    serializer_class = UserSerializer

    def post(self, request):
        user = request.user
        avatar_file = request.FILES.get("avatar")

        if not avatar_file:
            return Response(
                {"error": "No avatar file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
        file_ext = os.path.splitext(avatar_file.name)[1].lower()
        if file_ext not in allowed_extensions:
            return Response(
                {"error": "Invalid file format. Only JPG, JPEG, PNG, GIF are allowed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.profile_picture:
            try:
                default_storage.delete(user.profile_picture.path)
            except Exception:
                pass

        file_name = f"profile_pictures/{user.username}_{avatar_file.name}"
        file_path = default_storage.save(file_name, ContentFile(avatar_file.read()))

        user.profile_picture = file_path
        user.save(update_fields=["profile_picture"])

        avatar_url = default_storage.url(file_path)
        return Response(
            {"message": "Avatar uploaded successfully", "avatar_url": avatar_url},
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        user = request.user
        if user.profile_picture:
            try:
                default_storage.delete(user.profile_picture.path)
                user.profile_picture = None
                user.save(update_fields=["profile_picture"])
                return Response(
                    {"message": "Avatar deleted successfully"}, status=status.HTTP_200_OK
                )
            except Exception:
                return Response(
                    {"error": "Failed to delete avatar"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response({"error": "No avatar to delete"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Users"])
class UserExportAPIView(APIView):
    permission_classes = [IsAdmin]  # Chỉ admin được export
    serializer_class = UserSerializer

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Username", "Email", "Role", "Department", "Is Active"])

        users = User.objects.filter(is_deleted=False)
        for user in users:
            writer.writerow(
                [
                    user.id,
                    user.username,
                    user.email,
                    user.role,
                    user.department.name if user.department else "",
                    user.is_active,
                ]
            )

        return response


@extend_schema(tags=["Scores"])
class ScoreManagementAPIView(APIView):
    permission_classes = [ScorePermission]  # Admin hoặc giáo viên được phân công
    serializer_class = ScoreSerializer
    queryset = Score.objects.all()

    def post(self, request):
        # Logic quản lý điểm số
        return Response({"message": "Scores updated"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Scores"])
class ViewOwnScoresAPIView(APIView):
    permission_classes = [ScorePermission]  # Admin, giáo viên hoặc học sinh được phân công
    queryset = Score.objects.all()

    def get(self, request):
        scores = Score.objects.filter(student=request.user)  # Chỉ lấy điểm của học sinh hiện tại
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Statistics"])
class StatisticsAPIView(APIView):
    permission_classes = [IsAdminOrTeacher]  # Admin hoặc giáo viên
    serializer_class = None

    def get(self, request):
        user_stats = User.objects.filter(is_deleted=False).aggregate(
            total_users=Count("id"),
            active_users=Count("id", filter=Q(is_active=True)),
            students=Count("id", filter=Q(role="student")),
            teachers=Count("id", filter=Q(role="teacher")),
            admins=Count("id", filter=Q(role="admin")),
        )

        department_stats = Department.objects.filter(is_deleted=False).aggregate(
            total_departments=Count("id"),
            active_departments=Count("id", filter=Q(is_active=True)),
        )

        data = {
            "users": user_stats,
            "departments": department_stats,
        }
        return Response(data, status=status.HTTP_200_OK)
