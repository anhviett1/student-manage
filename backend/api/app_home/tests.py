from rest_framework.test import APITestCase, APIRequestFactory, APITestCase, APIClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .permissions import (
    IsAdmin, IsTeacher, IsStudent, IsAdminOrReadOnly, IsOwnerOrAdmin,
    IsAdminOrTeacher, CanManageScores, CanManageSubject, CanViewSubjectScores,
    CanViewOwnScores
)
from .views import UserPermissionAPIView, UserRoleAPIView
from .models import Score, Subject  # Giả định model Score và Subject
from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from io import BytesIO
from PIL import Image
from .models import User, Department, Score
from .serializers import UserSerializer, DepartmentSerializer
import csv
from io import StringIO
import os
User = get_user_model()

class ViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Tạo người dùng với các vai trò khác nhau
        self.admin_user = User.objects.create_user(
            username="admin", password="pass123", role="admin", email="admin@example.com",
            first_name="Admin", last_name="User"
        )
        self.student_user = User.objects.create_user(
            username="student", password="pass123", role="student", email="student@example.com",
            first_name="Student", last_name="User"
        )

        # File ảnh mẫu để test AvatarUploadView
        self.image_content = self.create_test_image()
        self.image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=self.image_content,
            content_type="image/jpeg"
        )

    def create_test_image(self):
        """Tạo file ảnh giả lập để test."""
        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return buffer.getvalue()

    def tearDown(self):
        """Xóa các file ảnh sau khi test."""
        media_root = settings.MEDIA_ROOT
        for user in User.objects.all():
            if user.profile_picture:
                file_path = os.path.join(media_root, user.profile_picture.name)
                if os.path.exists(file_path):
                    os.remove(file_path)

    def test_login_api_view_success(self):
        """Kiểm tra đăng nhập thành công."""
        url = reverse("login")
        data = {"username": "admin", "password": "pass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Login successful")
        self.assertEqual(response.data["user"]["username"], "admin")
        self.assertEqual(response.data["user"]["role"], "admin")
        # Kiểm tra last_login_ip được cập nhật
        self.admin_user.refresh_from_db()
        self.assertIsNotNone(self.admin_user.last_login_ip)

    def test_login_api_view_invalid_credentials(self):
        """Kiểm tra đăng nhập với thông tin sai."""
        url = reverse("login")
        data = {"username": "admin", "password": "wrongpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["error"], "Invalid credentials")

    def test_logout_api_view(self):
        """Kiểm tra đăng xuất."""
        url = reverse("logout")
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Logout successful")
        # Kiểm tra đã đăng xuất
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 401)  # Chưa đăng nhập

    def test_profile_api_view_get(self):
        """Kiểm tra lấy thông tin hồ sơ."""
        url = reverse("profile")
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        serializer = UserSerializer(self.student_user)
        self.assertEqual(response.data, serializer.data)

    def test_profile_api_view_put(self):
        """Kiểm tra cập nhật hồ sơ."""
        url = reverse("profile")
        self.client.force_authenticate(user=self.student_user)
        data = {"first_name": "New", "last_name": "Name", "email": "new@example.com"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Profile updated successfully")
        self.student_user.refresh_from_db()
        self.assertEqual(self.student_user.first_name, "New")
        self.assertEqual(self.student_user.last_name, "Name")
        self.assertEqual(self.student_user.email, "new@example.com")

    def test_profile_api_view_put_invalid_data(self):
        """Kiểm tra cập nhật hồ sơ với dữ liệu không hợp lệ."""
        url = reverse("profile")
        self.client.force_authenticate(user=self.student_user)
        data = {"email": "invalid_email"}  # Email không hợp lệ
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_profile_api_view_unauthenticated(self):
        """Kiểm tra truy cập hồ sơ khi chưa đăng nhập."""
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_change_password_api_view_success(self):
        """Kiểm tra đổi mật khẩu thành công."""
        url = reverse("change_password")
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "old_password": "pass123",
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Password changed successfully")
        self.admin_user.refresh_from_db()
        self.assertTrue(self.admin_user.check_password("newpass123"))

    def test_change_password_api_view_wrong_old_password(self):
        """Kiểm tra đổi mật khẩu với mật khẩu cũ sai."""
        url = reverse("change_password")
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "old_password": "wrongpass",
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Old password is incorrect")

    def test_change_password_api_view_mismatch_passwords(self):
        """Kiểm tra đổi mật khẩu khi new_password và confirm_password không khớp."""
        url = reverse("change_password")
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "old_password": "pass123",
            "new_password": "newpass123",
            "confirm_password": "differentpass123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "New password and confirm password do not match")

    def test_change_password_api_view_short_password(self):
        """Kiểm tra đổi mật khẩu với mật khẩu mới quá ngắn."""
        url = reverse("change_password")
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "old_password": "pass123",
            "new_password": "short",
            "confirm_password": "short"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "New password must be at least 8 characters long")

    def test_user_role_api_view_get(self):
        """Kiểm tra lấy vai trò người dùng."""
        url = reverse("user-role")
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["role"], "student")
        self.assertEqual(response.data["role_display"], "Sinh viên")

    def test_user_role_api_view_put_admin(self):
        """Kiểm tra admin thay đổi vai trò."""
        url = reverse("user-role")
        self.client.force_authenticate(user=self.admin_user)
        data = {"role": "teacher"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Role updated successfully")
        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.role, "teacher")

    def test_user_role_api_view_put_non_admin(self):
        """Kiểm tra non-admin thay đổi vai trò."""
        url = reverse("user-role")
        self.client.force_authenticate(user=self.student_user)
        data = {"role": "admin"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["error"], "Only admins can change roles")

    def test_user_role_api_view_put_invalid_role(self):
        """Kiểm tra thay đổi vai trò không hợp lệ."""
        url = reverse("user-role")
        self.client.force_authenticate(user=self.admin_user)
        data = {"role": "invalid_role"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Invalid role")

    def test_avatar_upload_api_view_success(self):
        """Kiểm tra tải lên ảnh đại diện thành công."""
        url = reverse("avatar-upload")
        self.client.force_authenticate(user=self.student_user)
        data = {"avatar": self.image_file}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Avatar uploaded successfully")
        self.student_user.refresh_from_db()
        self.assertTrue(self.student_user.profile_picture.name.startswith("profile_pictures/student_test_image"))
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, self.student_user.profile_picture.name)))

    def test_avatar_upload_api_view_invalid_format(self):
        """Kiểm tra tải lên file không phải ảnh."""
        url = reverse("avatar-upload")
        self.client.force_authenticate(user=self.student_user)
        invalid_file = SimpleUploadedFile("test.txt", b"not an image", content_type="text/plain")
        data = {"avatar": invalid_file}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Invalid file format. Only JPG, JPEG, PNG, GIF are allowed")

    def test_avatar_upload_api_view_no_file(self):
        """Kiểm tra tải lên mà không có file."""
        url = reverse("avatar-upload")
        self.client.force_authenticate(user=self.student_user)
        data = {}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No avatar file provided")

    def test_avatar_upload_api_view_replace_existing(self):
        """Kiểm tra thay thế ảnh đại diện hiện có."""
        url = reverse("avatar-upload")
        self.client.force_authenticate(user=self.student_user)
        # Tải lên ảnh đầu tiên
        data = {"avatar": self.image_file}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 200)
        old_path = self.student_user.profile_picture.path

        # Tải lên ảnh mới
        new_image = SimpleUploadedFile("new_image.jpg", self.image_content, content_type="image/jpeg")
        data = {"avatar": new_image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.student_user.refresh_from_db()
        self.assertTrue(self.student_user.profile_picture.name.startswith("profile_pictures/student_new_image"))
        # Kiểm tra ảnh cũ đã bị xóa
        self.assertFalse(os.path.exists(old_path))

    def test_avatar_upload_api_view_delete(self):
        """Kiểm tra xóa ảnh đại diện."""
        url = reverse("avatar-upload")
        self.client.force_authenticate(user=self.student_user)
        # Tải lên ảnh trước
        data = {"avatar": self.image_file}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 200)
        old_path = self.student_user.profile_picture.path

        # Xóa ảnh
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Avatar deleted successfully")
        self.student_user.refresh_from_db()
        self.assertIsNone(self.student_user.profile_picture)
        self.assertFalse(os.path.exists(old_path))

    def test_avatar_upload_api_view_delete_no_avatar(self):
        """Kiểm tra xóa khi không có ảnh đại diện."""
        url = reverse("avatar-upload")
        self.client.force_authenticate(user=self.student_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "No avatar to delete")
# View giả định để kiểm tra permissions
class TestView(APIView):
    queryset = Score.objects.all()  # Giả định model Score

    def get(self, request):
        return Response({"message": "Success"}, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({"message": "Success"}, status=status.HTTP_201_CREATED)

class TestObjectPermissionView(APIView):
    queryset = Score.objects.all()

    def get(self, request, pk):
        score = Score.objects.get(pk=pk)
        self.check_object_permissions(request, score)
        return Response({"message": "Success"}, status=status.HTTP_200_OK)

class PermissionTests(APITestCase):
    def setUp(self):
        # Tạo người dùng với các vai trò khác nhau
        self.admin_user = User.objects.create_user(
            username="admin", password="pass123", role="admin", email="admin@example.com"
        )
        self.teacher_user = User.objects.create_user(
            username="teacher", password="pass123", role="teacher", email="teacher@example.com"
        )
        self.student_user = User.objects.create_user(
            username="student", password="pass123", role="student", email="student@example.com"
        )
        self.unauthenticated_user = None  # Người dùng chưa đăng nhập

        # Tạo model Score và Subject
        self.score = Score.objects.create(user=self.student_user, value=85.5)
        self.subject = Subject.objects.create(name="Math")

        # Lấy ContentType và gán quyền
        self.score_content_type = ContentType.objects.get_for_model(Score)
        self.subject_content_type = ContentType.objects.get_for_model(Subject)

        # Gán quyền cho teacher_user
        manage_scores_perm = Permission.objects.get(
            codename="can_manage_scores", content_type=self.score_content_type
        )
        manage_subject_perm = Permission.objects.get(
            codename="can_manage_subject", content_type=self.subject_content_type
        )
        view_subject_scores_perm = Permission.objects.get(
            codename="can_view_subject_scores", content_type=self.subject_content_type
        )
        self.teacher_user.user_permissions.add(
            manage_scores_perm, manage_subject_perm, view_subject_scores_perm
        )

        # Factory để tạo request
        self.factory = APIRequestFactory()

    def test_is_admin_permission(self):
        """Kiểm tra IsAdmin chỉ cho phép admin."""
        view = TestView.as_view(permission_classes=[IsAdmin])

        # Admin user
        request = self.factory.get("/test/")
        request.user = self.admin_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Teacher user
        request.user = self.teacher_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Unauthenticated user
        request.user = None
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_teacher_permission(self):
        """Kiểm tra IsTeacher chỉ cho phép giảng viên."""
        view = TestView.as_view(permission_classes=[IsTeacher])

        # Teacher user
        request = self.factory.get("/test/")
        request.user = self.teacher_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Admin user
        request.user = self.admin_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Student user
        request.user = self.student_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_student_permission(self):
        """Kiểm tra IsStudent chỉ cho phép sinh viên."""
        view = TestView.as_view(permission_classes=[IsStudent])

        # Student user
        request = self.factory.get("/test/")
        request.user = self.student_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Teacher user
        request.user = self.teacher_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_admin_or_read_only_permission(self):
        """Kiểm tra IsAdminOrReadOnly cho phép đọc với xác thực, ghi chỉ với admin."""
        view = TestView.as_view(permission_classes=[IsAdminOrReadOnly])

        # GET request
        request = self.factory.get("/test/")
        request.user = self.student_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST request với admin
        request = self.factory.post("/test/")
        request.user = self.admin_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # POST request với student
        request.user = self.student_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # GET request chưa xác thực
        request.user = None
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_owner_or_admin_permission(self):
        """Kiểm tra IsOwnerOrAdmin cho phép chủ sở hữu hoặc admin."""
        view = TestObjectPermissionView.as_view(permission_classes=[IsOwnerOrAdmin])

        # Admin user
        request = self.factory.get(f"/test/{self.score.id}/")
        request.user = self.admin_user
        response = view(request, pk=self.score.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Owner (student)
        request.user = self.student_user
        response = view(request, pk=self.score.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Non-owner (teacher)
        request.user = self.teacher_user
        response = view(request, pk=self.score.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_admin_or_teacher_permission(self):
        """Kiểm tra IsAdminOrTeacher cho phép admin hoặc giảng viên."""
        view = TestView.as_view(permission_classes=[IsAdminOrTeacher])

        # Admin user
        request = self.factory.get("/test/")
        request.user = self.admin_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Teacher user
        request.user = self.teacher_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Student user
        request.user = self.student_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_manage_scores_permission(self):
        """Kiểm tra CanManageScores cho phép người có quyền can_manage_scores."""
        view = TestView.as_view(permission_classes=[CanManageScores])

        # Teacher user với quyền
        request = self.factory.post("/test/")
        request.user = self.teacher_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Student user không có quyền
        request.user = self.student_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_manage_subject_permission(self):
        """Kiểm tra CanManageSubject cho phép người có quyền can_manage_subject."""
        view = TestView.as_view(permission_classes=[CanManageSubject], queryset=Subject.objects.all())

        # Teacher user với quyền
        request = self.factory.post("/test/")
        request.user = self.teacher_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Student user không có quyền
        request.user = self.student_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_view_subject_scores_permission(self):
        """Kiểm tra CanViewSubjectScores cho phép người có quyền can_view_subject_scores."""
        view = TestView.as_view(permission_classes=[CanViewSubjectScores], queryset=Subject.objects.all())

        # Teacher user với quyền
        request = self.factory.get("/test/")
        request.user = self.teacher_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Student user không có quyền
        request.user = self.student_user
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_view_own_scores_permission(self):
        """Kiểm tra CanViewOwnScores cho phép sinh viên xem điểm của chính họ."""
        view = TestObjectPermissionView.as_view(permission_classes=[CanViewOwnScores])

        # Student user (owner)
        request = self.factory.get(f"/test/{self.score.id}/")
        request.user = self.student_user
        response = view(request, pk=self.score.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Teacher user (non-owner)
        request.user = self.teacher_user
        response = view(request, pk=self.score.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Non-student user
        request.user = self.admin_user
        response = view(request, pk=self.score.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_permission_api_view(self):
        """Kiểm tra UserPermissionAPIView với quyền IsAdmin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("user-permissions", kwargs={"pk": self.teacher_user.id})

        # GET: Lấy danh sách quyền
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("can_manage_scores", [p["codename"] for p in response.data])

        # POST: Thêm quyền
        response = self.client.post(url, {"permissions": ["can_view_dashboard"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.teacher_user.has_perm("app_home.can_view_dashboard"))

        # DELETE: Xóa quyền
        response = self.client.delete(url, {"permissions": ["can_manage_scores"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.teacher_user.has_perm("app_home.can_manage_scores"))

        # Non-admin user
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post(url, {"permissions": ["can_view_dashboard"]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_role_api_view(self):
        """Kiểm tra UserRoleAPIView với quyền IsAuthenticated."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("user-role")

        # GET: Lấy vai trò
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], "admin")

        # PUT: Thay đổi vai trò (chỉ admin)
        response = self.client.put(url, {"role": "teacher"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.admin_user.role, "teacher")

        # Non-admin user
        self.client.force_authenticate(user=self.student_user)
        response = self.client.put(url, {"role": "admin"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class AdditionalViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Tạo người dùng
        self.admin_user = User.objects.create_user(
            username="admin", password="pass123", role="admin", email="admin@example.com",
            is_active=True, is_deleted=False
        )
        self.student_user = User.objects.create_user(
            username="student", password="pass123", role="student", email="student@example.com",
            is_active=True, is_deleted=False
        )
        self.deleted_user = User.objects.create_user(
            username="deleted", password="pass123", role="student", email="deleted@example.com",
            is_active=False, is_deleted=True
        )

        # Tạo khoa
        self.department = Department.objects.create(
            name="Computer Science", code="CS", is_active=True, is_deleted=False, head=self.admin_user
        )
        self.deleted_department = Department.objects.create(
            name="Math", code="MATH", is_active=False, is_deleted=True
        )

        # Tạo điểm số
        self.score = Score.objects.create(user=self.student_user, value=85.5)

        # Gán quyền can_manage_scores cho admin
        score_content_type = ContentType.objects.get_for_model(Score)
        manage_scores_perm = Permission.objects.get(
            codename="can_manage_scores", content_type=score_content_type
        )
        self.admin_user.user_permissions.add(manage_scores_perm)

    def test_statistics_api_view(self):
        """Kiểm tra API thống kê."""
        url = reverse("statistics")
        self.client.force_authenticate(user=self.admin_user)
        
        # Tạo thêm dữ liệu để kiểm tra thống kê
        User.objects.create_user(username="teacher", password="pass123", role="teacher")
        Department.objects.create(name="Physics", code="PHY", is_active=True)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["users"]["total_users"], 3)  # admin, student, teacher
        self.assertEqual(response.data["users"]["active_users"], 2)  # admin, teacher
        self.assertEqual(response.data["users"]["students"], 1)
        self.assertEqual(response.data["users"]["teachers"], 1)
        self.assertEqual(response.data["users"]["admins"], 1)
        self.assertEqual(response.data["departments"]["total_departments"], 2)  # CS, PHY
        self.assertEqual(response.data["departments"]["active_departments"], 1)

    def test_statistics_api_view_unauthenticated(self):
        """Kiểm tra API thống kê khi chưa đăng nhập."""
        url = reverse("statistics")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_user_restore_api_view_success(self):
        """Kiểm tra khôi phục người dùng đã xóa."""
        url = reverse("user-restore", kwargs={"pk": self.deleted_user.id})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "User restored successfully")
        self.deleted_user.refresh_from_db()
        self.assertFalse(self.deleted_user.is_deleted)
        self.assertTrue(self.deleted_user.is_active)

    def test_user_restore_api_view_not_found(self):
        """Kiểm tra khôi phục người dùng không tồn tại hoặc không bị xóa."""
        url = reverse("user-restore", kwargs={"pk": 999})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "User not found or not deleted")

        # Người dùng không bị xóa
        url = reverse("user-restore", kwargs={"pk": self.admin_user.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "User not found or not deleted")

    def test_user_restore_api_view_unauthenticated(self):
        """Kiểm tra khôi phục người dùng khi chưa đăng nhập."""
        url = reverse("user-restore", kwargs={"pk": self.deleted_user.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_user_permission_api_view_get(self):
        """Kiểm tra lấy danh sách quyền của người dùng."""
        url = reverse("user-permissions", kwargs={"pk": self.admin_user.id})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("can_manage_scores", [p["codename"] for p in response.data])

    def test_user_permission_api_view_post(self):
        """Kiểm tra thêm quyền cho người dùng."""
        url = reverse("user-permissions", kwargs={"pk": self.student_user.id})
        self.client.force_authenticate(user=self.admin_user)
        data = {"permissions": ["can_view_dashboard"]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Permissions added successfully")
        self.assertTrue(self.student_user.has_perm("app_home.can_view_dashboard"))

    def test_user_permission_api_view_delete(self):
        """Kiểm tra xóa quyền của người dùng."""
        url = reverse("user-permissions", kwargs={"pk": self.admin_user.id})
        self.client.force_authenticate(user=self.admin_user)
        data = {"permissions": ["can_manage_scores"]}
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Permissions removed successfully")
        self.assertFalse(self.admin_user.has_perm("app_home.can_manage_scores"))

    def test_user_permission_api_view_not_found(self):
        """Kiểm tra thêm/xóa quyền cho người dùng không tồn tại."""
        url = reverse("user-permissions", kwargs={"pk": 999})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, {"permissions": ["can_view_dashboard"]}, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "User not found")

    def test_user_permission_api_view_unauthenticated(self):
        """Kiểm tra truy cập API quyền khi chưa đăng nhập."""
        url = reverse("user-permissions", kwargs={"pk": self.student_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_user_export_api_view(self):
        """Kiểm tra xuất danh sách người dùng ra CSV."""
        url = reverse("user-export")
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="users.csv"')

        # Kiểm tra nội dung CSV
        content = response.content.decode("utf-8")
        csv_reader = csv.reader(StringIO(content))
        header = next(csv_reader)
        self.assertEqual(header, ["ID", "Username", "Full Name", "Email", "Role", "Department", "Is Active"])
        rows = list(csv_reader)
        self.assertEqual(len(rows), 2)  # admin, student (deleted_user bị lọc bởi is_deleted=False)
        self.assertIn([str(self.admin_user.id), "admin", "Admin User", "admin@example.com", "Quản trị viên", "Computer Science", "True"], rows)

    def test_user_export_api_view_unauthenticated(self):
        """Kiểm tra xuất người dùng khi chưa đăng nhập."""
        url = reverse("user-export")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_department_restore_api_view_success(self):
        """Kiểm tra khôi phục khoa đã xóa."""
        url = reverse("department-restore", kwargs={"pk": self.deleted_department.id})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Department restored successfully")
        self.deleted_department.refresh_from_db()
        self.assertFalse(self.deleted_department.is_deleted)
        self.assertTrue(self.deleted_department.is_active)

    def test_department_restore_api_view_not_found(self):
        """Kiểm tra khôi phục khoa không tồn tại hoặc không bị xóa."""
        url = reverse("department-restore", kwargs={"pk": 999})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Department not found or not deleted")

        # Khoa không bị xóa
        url = reverse("department-restore", kwargs={"pk": self.department.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Department not found or not deleted")

    def test_department_restore_api_view_unauthenticated(self):
        """Kiểm tra khôi phục khoa khi chưa đăng nhập."""
        url = reverse("department-restore", kwargs={"pk": self.deleted_department.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_department_export_api_view(self):
        """Kiểm tra xuất danh sách khoa ra CSV."""
        url = reverse("department-export")
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="departments.csv"')

        # Kiểm tra nội dung CSV
        content = response.content.decode("utf-8")
        csv_reader = csv.reader(StringIO(content))
        header = next(csv_reader)
        self.assertEqual(header, ["ID", "Code", "Name", "Head", "Is Active"])
        rows = list(csv_reader)
        self.assertEqual(len(rows), 1)  # Chỉ có CS (MATH bị lọc bởi is_deleted=False)
        self.assertIn([str(self.department.id), "CS", "Computer Science", "Admin User", "True"], rows)

    def test_department_export_api_view_unauthenticated(self):
        """Kiểm tra xuất khoa khi chưa đăng nhập."""
        url = reverse("department-export")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_score_management_api_view_success(self):
        """Kiểm tra tạo điểm số thành công."""
        url = reverse("score-management")
        self.client.force_authenticate(user=self.admin_user)
        data = {"user_id": self.student_user.id, "value": 90.0}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Score created successfully")
        self.assertTrue(Score.objects.filter(user=self.student_user, value=90.0).exists())

    def test_score_management_api_view_invalid_user(self):
        """Kiểm tra tạo điểm số với user_id không tồn tại."""
        url = reverse("score-management")
        self.client.force_authenticate(user=self.admin_user)
        data = {"user_id": 999, "value": 90.0}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "User not found")

    def test_score_management_api_view_unauthenticated(self):
        """Kiểm tra tạo điểm số khi chưa đăng nhập."""
        url = reverse("score-management")
        response = self.client.post(url, {"user_id": self.student_user.id, "value": 90.0}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_score_management_api_view_no_permission(self):
        """Kiểm tra tạo điểm số khi không có quyền can_manage_scores."""
        url = reverse("score-management")
        self.client.force_authenticate(user=self.student_user)
        data = {"user_id": self.student_user.id, "value": 90.0}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403)
