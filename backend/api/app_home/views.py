from rest_framework import viewsets
from django.db.models import Q

from ..app_department.models import Department
from ..app_home.permissions import CanManageScores, CanViewOwnScores, IsAdmin
from ..app_score.models import Score
from ..app_score.serializers import ScoreSerializer
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.contrib.auth.models import Permission
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import csv, os
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout



@extend_schema(tags=["Users"])
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.none()

        if self.request.user.is_authenticated:
            filters = Q()

            search_term = self.request.query_params.get("searchTerm", "")
            role_filter = self.request.query_params.get("role", "")
            department_filter = self.request.query_params.get("department", "")
            status_filter = self.request.query_params.get("status", "")

            role_list = role_filter.split(",") if role_filter else []
            department_list = [int(id) for id in department_filter.split(",") if id.isdigit()]
            status_list = status_filter.split(",") if status_filter else ["active"]

            if status_list:
                filters &= Q(is_active__in=[s == "active" for s in status_list])

            if search_term:
                filters &= (
                    Q(username__icontains=search_term)
                    | Q(first_name__icontains=search_term)
                    | Q(last_name__icontains=search_term)
                    | Q(email__icontains=search_term)
                )

            if role_list:
                filters &= Q(role__in=role_list)

            if department_list:
                filters &= Q(department__id__in=department_list)

            queryset = User.objects.filter(filters).distinct().order_by("-created_at")

        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        if "last_login_ip" in self.request.data:
            instance.update_last_login_ip(self.request.data["last_login_ip"])

    def perform_destroy(self, instance):
        instance.soft_delete()

@extend_schema(tags=["Users"])
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            user.update_last_login_ip(request.META.get("REMOTE_ADDR"))
            serializer = UserSerializer(user)
            return Response(
                {"message": "Login successful", "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

@extend_schema(tags=["Users"])
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

@extend_schema(tags=["Users"])
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
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

@extend_schema(tags=["Users"])
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
        return Response(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )

@extend_schema(tags=["Users"])
class UserRoleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        new_role = request.data.get("role")
        if new_role not in dict(User.ROLE_CHOICES):
            return Response(
                {"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not user.is_admin and user.role != new_role:
            return Response(
                {"error": "Only admins can change roles"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user.role = new_role
        user.save(update_fields=["role"])
        return Response(
            {"message": "Role updated successfully"}, status=status.HTTP_200_OK
        )

@extend_schema(tags=["Users"])
class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        avatar_file = request.FILES.get("avatar")

        if not avatar_file:
            return Response({"error": "No avatar file provided"}, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({"message": "Avatar deleted successfully"}, status=status.HTTP_200_OK)
            except Exception:
                return Response({"error": "Failed to delete avatar"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No avatar to delete"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Users"])
class UserRestoreAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_deleted=True)
            user.restore()
            return Response({"message": "User restored successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found or not deleted"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(tags=["Users"])
class UserExportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Username", "Email", "Role", "Department", "Is Active"])

        users = User.objects.filter(is_deleted=False)
        for user in users:
            writer.writerow([
                user.id,
                user.username,
                user.email,
                user.department.name if user.department else "",
                user.is_active,
            ])

        return response

@extend_schema(tags=["Users"])
class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        avatar_file = request.FILES.get("avatar")

        if not avatar_file:
            return Response({"error": "No avatar file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra định dạng file (chỉ cho phép ảnh)
        allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
        file_ext = os.path.splitext(avatar_file.name)[1].lower()
        if file_ext not in allowed_extensions:
            return Response(
                {"error": "Invalid file format. Only JPG, JPEG, PNG, GIF are allowed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Xóa ảnh cũ nếu có
        if user.profile_picture:
            try:
                default_storage.delete(user.profile_picture.path)
            except Exception:
                pass  # Bỏ qua nếu file không tồn tại

        # Tạo tên file duy nhất dựa trên username và timestamp
        file_name = f"profile_pictures/{user.username}_{avatar_file.name}"
        file_path = default_storage.save(file_name, ContentFile(avatar_file.read()))

        # Cập nhật trường profile_picture của user
        user.profile_picture = file_path
        user.save(update_fields=["profile_picture"])

        # Trả về URL của ảnh
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
                return Response({"message": "Avatar deleted successfully"}, status=status.HTTP_200_OK)
            except Exception:
                return Response({"error": "Failed to delete avatar"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No avatar to delete"}, status=status.HTTP_400_BAD_REQUEST)    

@extend_schema(tags=["Scores"])
class ScoreManagementAPIView(APIView):
    permission_classes = [CanManageScores]
    queryset = Score.objects.all()  

    def post(self, request):
        # Logic quản lý điểm số
        return Response({"message": "Scores updated"}, status=status.HTTP_200_OK)
    
@extend_schema(tags=["Scores"])
class ViewOwnScoresAPIView(APIView):
    permission_classes = [CanViewOwnScores]
    queryset = Score.objects.all()

    def get(self, request):
        scores = Score.objects.filter(user=request.user)
        serializer = ScoreSerializer(scores, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Statistics"])
class StatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
    
@extend_schema(tags=["Permissions"])
class UserPermissionAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            permissions = user.user_permissions.all().values("codename", "name")
            return Response(list(permissions), status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            permission_codenames = request.data.get("permissions", [])
            permissions = Permission.objects.filter(codename__in=permission_codenames)
            user.user_permissions.add(*permissions)
            return Response({"message": "Permissions added successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            permission_codenames = request.data.get("permissions", [])
            permissions = Permission.objects.filter(codename__in=permission_codenames)
            user.user_permissions.remove(*permissions)
            return Response({"message": "Permissions removed successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)    
        