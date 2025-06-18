from datetime import datetime
import os
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.apps import apps
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..app_student.models import Student
from ..app_teacher.models import Teacher
from ..app_subject.models import Subject
from ..app_class.models import Class
from ..app_activity.models import Activity
from .models import User, Department
from .serializers import UserSerializer, DepartmentSerializer, ChangePasswordSerializer, UserProfileSerializer
from .permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrAdmin

User = get_user_model()

class UserManager:
    @staticmethod
    def get_full_name(user):
        return f"{user.first_name} {user.last_name}".strip() or user.username

    @staticmethod
    def get_short_name(user):
        return user.first_name or user.username

    @staticmethod
    def is_student(user):
        return user.role == 'student'

    @staticmethod
    def is_teacher(user):
        return user.role == 'teacher'

    @staticmethod
    def is_admin(user):
        return user.role == 'admin'

    @staticmethod
    def get_role_display_name(user):
        return dict(user.ROLE_CHOICES).get(user.role, user.role)

    @staticmethod
    def update_last_login_ip(user, ip_address):
        user.last_login_ip = ip_address
        user.save(update_fields=['last_login_ip'])

class DepartmentManager:
    @staticmethod
    def get_department_string(department):
        return f"{department.code} - {department.name}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Tạo hoặc cập nhật hồ sơ người dùng dựa trên vai trò"""
    if instance.is_superuser or not hasattr(instance, 'role'):
        return

    profile_data = {
        'user': instance,
        'first_name': getattr(instance, 'first_name', instance.username),
        'last_name': getattr(instance, 'last_name', ''),
        'email': instance.email,
        'phone_number': '',
        'date_of_birth': '2000-01-01',
        'address': '',
        'city': '',
        'state': '',
    }

    if created:
        if instance.role == 'student':
            Student.objects.create(**profile_data)
        elif instance.role == 'teacher':
            profile_data['subject'] = ''
            profile_data['salary'] = 0
            Teacher.objects.create(**profile_data)
    else:
        if instance.role == 'student':
            Student.objects.filter(user=instance).update(**profile_data)
        elif instance.role == 'teacher':
            profile_data['subject'] = ''
            profile_data['salary'] = 0
            Teacher.objects.filter(user=instance).update(**profile_data)

def get_dashboard_context():
    """Lấy dữ liệu ngữ cảnh cho dashboard"""
    return {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_teachers': Teacher.objects.filter(is_active=True).count(),
        'total_subjects': Subject.objects.filter(is_active=True).count(),
        'total_classes': Class.objects.filter(is_active=True).count(),
        'subjects_by_semester': Subject.objects.filter(is_active=True)
            .values('semester')
            .annotate(count=Count('subject_id'))
            .order_by('semester'),
        'recent_activities': Activity.objects.select_related('user')
            .order_by('-created_at')[:10],
    }

@extend_schema(tags=['Users'])
class LoginAPIView(APIView):
    """API view cho đăng nhập người dùng"""
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            UserManager.update_last_login_ip(user, request.META.get('REMOTE_ADDR'))
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Đăng nhập thành công',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': getattr(user, 'role', None),
                }
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Thông tin đăng nhập không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Users'])
class LogoutAPIView(APIView):
    """API view cho đăng xuất người dùng"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            logout(request)
            return Response({'message': 'Đăng xuất thành công'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Users'])
class ProfileAPIView(APIView):
    """API view cho quản lý hồ sơ người dùng"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                'message': 'Cập nhật hồ sơ thành công',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Users'])
class ChangePasswordAPIView(APIView):
    """API view cho thay đổi mật khẩu người dùng"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': 'Đổi mật khẩu thành công'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    """API endpoint cho quản lý người dùng"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        """Gán quyền động dựa trên hành động"""
        permission_classes = {
            'create': [IsAdmin],
            'update': [IsAdmin],
            'partial_update': [IsAdmin],
            'destroy': [IsAdmin],
            'me': [IsAuthenticated],
            'list': [IsAdmin],
            'retrieve': [IsAdmin],
            'deleted': [IsAdmin],
            'restore': [IsAdmin],
        }.get(self.action, [IsAdminOrReadOnly])
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Tạo người dùng mới với mật khẩu và vai trò"""
        user = serializer.save()
        user.set_password(serializer.validated_data.get('password', 'default_password123'))
        user.save()
        return user

    def perform_destroy(self, instance):
        """Xóa mềm người dùng thay vì xóa cứng"""
        instance.is_active = False
        instance.save(update_fields=['is_active'])

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Lấy hồ sơ của người dùng hiện tại"""
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Thay đổi mật khẩu qua hành động tùy chỉnh"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': 'Đổi mật khẩu thành công'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def deleted(self, request):
        """Lấy danh sách người dùng đã xóa mềm"""
        deleted_users = User.objects.filter(is_active=False)
        serializer = self.get_serializer(deleted_users, many=True)
        return Response({
            'message': 'Danh sách người dùng đã xóa mềm',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def restore(self, request, pk=None):
        """Khôi phục người dùng đã xóa mềm"""
        user = self.get_object()
        user.is_active = True
        user.save(update_fields=['is_active'])
        serializer = self.get_serializer(user)
        return Response({
            'message': 'Khôi phục người dùng thành công',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

@extend_schema(tags=['Users'])
class AvatarUploadView(APIView):
    """API view cho tải lên ảnh đại diện người dùng"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if 'avatar' not in request.FILES:
            return Response(
                {'error': 'Không có file ảnh đại diện được cung cấp'},
                status=status.HTTP_400_BAD_REQUEST
            )

        avatar_file = request.FILES['avatar']
        
        # Xác thực loại file
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if avatar_file.content_type not in allowed_types:
            return Response(
                {'error': 'Loại file không hợp lệ. Chỉ cho phép JPEG, PNG và GIF'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Xác thực kích thước file (tối đa 1MB)
        if avatar_file.size > 1024 * 1024:
            return Response(
                {'error': 'Kích thước file quá lớn. Kích thước tối đa là 1MB'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Tạo tên file duy nhất
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            ext = os.path.splitext(avatar_file.name)[1]
            filename = f'avatars/{request.user.id}_{timestamp}{ext}'

            # Xóa ảnh cũ nếu tồn tại
            if request.user.profile_picture:
                old_path = request.user.profile_picture.path
                if os.path.exists(old_path):
                    os.remove(old_path)

            # Lưu ảnh mới
            path = default_storage.save(filename, ContentFile(avatar_file.read()))
            request.user.profile_picture = path
            request.user.save()

            return Response({
                'avatar_url': request.user.profile_picture.url,
                'message': 'Tải ảnh đại diện thành công'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(tags=['Users'])
class UserRoleAPIView(APIView):
    """API view để lấy vai trò và quyền của người dùng"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        permissions = []
        
        # Thêm quyền dựa trên vai trò
        if user.is_superuser:
            permissions = ['*']  # Superuser có tất cả quyền
        elif user.role == 'admin':
            permissions = [
                'student:view', 'student:edit', 'student:delete',
                'teacher:view', 'teacher:edit', 'teacher:delete',
                'class:view', 'class:edit', 'class:delete',
                'subject:view', 'subject:edit', 'subject:delete',
                'enrollment:view', 'enrollment:edit', 'enrollment:delete',
                'score:view', 'score:edit', 'score:delete', 'score:upload',
                'semester:view', 'semester:edit', 'semester:delete',
                'department:view', 'department:edit', 'department:delete'
            ]
        elif user.role == 'teacher':
            permissions = [
                'student:view',
                'class:view',
                'subject:view',
                'enrollment:view',
                'score:view', 'score:edit', 'score:upload',
                'semester:view',
                'department:view'
            ]
        elif user.role == 'student':
            permissions = [
                'subject:view',
                'enrollment:view',
                'score:view',
                'department:view'
            ]

        return Response({
            'role': user.role,
            'is_superuser': user.is_superuser,
            'permissions': permissions
        }, status=status.HTTP_200_OK)

@extend_schema(tags=['Departments'])
class DepartmentViewSet(viewsets.ModelViewSet):
    """API endpoint cho quản lý khoa"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        """Gán quyền động dựa trên hành động"""
        permission_classes = {
            'create': [IsAdmin],
            'update': [IsAdmin],
            'partial_update': [IsAdmin],
            'destroy': [IsAdmin],
            'list': [IsAuthenticated],
            'retrieve': [IsAuthenticated],
            'deleted': [IsAdmin],
            'restore': [IsAdmin],
        }.get(self.action, [IsAdminOrReadOnly])
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Tạo khoa mới với mã tự động nếu cần"""
        department = serializer.save()
        if not department.code:
            department.code = department.name.upper().replace(' ', '_')
        department.save()
        return department

    def perform_destroy(self, instance):
        """Xóa mềm khoa thay vì xóa cứng"""
        instance.is_active = False
        instance.save(update_fields=['is_active'])

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def deleted(self, request):
        """Lấy danh sách các khoa đã xóa mềm"""
        deleted_departments = Department.objects.filter(is_active=False)
        serializer = self.get_serializer(deleted_departments, many=True)
        return Response({
            'message': 'Danh sách các khoa đã xóa mềm',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def restore(self, request, pk=None):
        """Khôi phục khoa đã xóa mềm"""
        department = self.get_object()
        department.is_active = True
        department.save(update_fields=['is_active'])
        serializer = self.get_serializer(department)
        return Response({
            'message': 'Khôi phục khoa thành công',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

@extend_schema(tags=['BaseModel'])
class SoftDeletedObjectsAPIView(APIView):
    """API view để liệt kê tất cả các đối tượng đã xóa mềm từ các model kế thừa BaseModel"""
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        deleted_objects = {}
        # Lấy tất cả các model kế thừa từ BaseModel
        for model in apps.get_models():
            if issubclass(model, User) and model != User:
                deleted_qs = model.objects.filter(is_active=False)
                serializer_class = UserSerializer if model == User else DepartmentSerializer
                deleted_objects[model.__name__] = serializer_class(deleted_qs, many=True).data

        return Response({
            'message': 'Danh sách các đối tượng đã xóa mềm',
            'data': deleted_objects
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def restore_all(self, request):
        """Khôi phục tất cả các đối tượng đã xóa mềm từ một model cụ thể"""
        model_name = request.data.get('model_name')
        if not model_name:
            return Response({'error': 'Yêu cầu cung cấp tên model'}, status=status.HTTP_400_BAD_REQUEST)

        model = None
        for m in apps.get_models():
            if m.__name__ == model_name and issubclass(m, User) and m != User:
                model = m
                break

        if not model:
            return Response({'error': 'Model không hợp lệ hoặc không kế thừa User'}, status=status.HTTP_400_BAD_REQUEST)

        deleted_objects = model.objects.filter(is_active=False)
        for obj in deleted_objects:
            obj.is_active = True
            obj.save(update_fields=['is_active'])

        serializer_class = UserSerializer if model == User else DepartmentSerializer
        restored_objects = model.objects.filter(is_active=True)
        serializer = serializer_class(restored_objects, many=True)
        return Response({
            'message': f'Khôi phục tất cả {model_name} thành công',
            'data': serializer.data
        }, status=status.HTTP_200_OK)