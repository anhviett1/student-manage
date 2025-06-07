from django.shortcuts import redirect, render
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from rest_framework import status, serializers, viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from ..app_student.models import Student
from ..app_teacher.models import Teacher
from ..app_subject.models import Subject
from ..app_class.models import Class
from ..app_activity.models import Activity
from .forms import ChangePasswordForm, UserProfileForm
from .models import Department
from .serializers import UserSerializer, DepartmentSerializer, ChangePasswordSerializer,UserProfileSerializer
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly, 
    IsOwnerOrAdmin
)

User = get_user_model()

#Signal handler được vô hiệu hóa - Admin sẽ tạo Student/Teacher từ trang admin
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    # Bỏ qua tự động tạo profile nếu là superuser
    if instance.is_superuser:
        return

    if created:
        if hasattr(instance, 'role') and instance.role == 'student':
            Student.objects.create(
                user=instance,
                first_name=instance.first_name if hasattr(instance, 'first_name') else instance.username,
                last_name=instance.last_name if hasattr(instance, 'last_name') else '',
                email=instance.email,
                phone_number='',  # Default empty phone
                date_of_birth='2000-01-01',  # Default date
                address='',
                city='',
                state=''
            )
        elif hasattr(instance, 'role') and instance.role == 'teacher':
            Teacher.objects.create(
                user=instance,
                first_name=instance.first_name if hasattr(instance, 'first_name') else instance.username,
                last_name=instance.last_name if hasattr(instance, 'last_name') else '',
                email=instance.email,
                phone_number='',  # Default empty phone
                date_of_birth='2000-01-01',  # Default date
                address='',
                city='',
                state='',
                subject='',
                salary=0
            )
        elif hasattr(instance, 'role') and instance.role == 'admin':
            # Admin profile creation logic if needed
            pass
    else:
        if hasattr(instance, 'role') and instance.role == 'student':
            try:
                student_profile = Student.objects.get(user=instance)
                student_profile.save()
            except Student.DoesNotExist:
                pass
        elif hasattr(instance, 'role') and instance.role == 'teacher':
            try:
                teacher_profile = Teacher.objects.get(user=instance)
                teacher_profile.save()
            except Teacher.DoesNotExist:
                pass
        elif hasattr(instance, 'role') and instance.role == 'admin':
            # Admin profile update logic if needed
            pass

class HomeApiEndpointSerializer(serializers.Serializer):
    """Serializer cho API endpoints"""
    message = serializers.CharField()
    api_endpoints = serializers.DictField(child=serializers.CharField())

@extend_schema(tags=['app_home'])
class HomeAPIView(APIView):
    """API View cho trang chủ"""
    permission_classes = [AllowAny]
    serializer_class = HomeApiEndpointSerializer
    
    def get(self, request, format=None):
        """Lấy danh sách API endpoints"""
        api_endpoints = {
            'api_gateway': '/api-gateway/',
            'api_docs': '/api-gateway/docs/',
            'api_schema': '/api-gateway/schema/',
            'api_redoc': '/api-gateway/redoc/',
            'token_obtain': '/api/token/',
            'token_refresh': '/api/token/refresh/',
            'token_verify': '/api/token/verify/',
            'login': '/api/login/',
            'logout': '/api/logout/',
            'profile': '/api/profile/',
            'change_password': '/api/change-password/',
        }
        dashboard_data = get_dashboard_context()
        api_endpoints.update({
            'dashboard': '/api/dashboard/',
            'students': '/api/students/',
            'teachers': '/api/teachers/',
            'subjects': '/api/subjects/',
            'classes': '/api/classes/',
            'scores': '/api/scores/',
            'enrollments': '/api/enrollments/',
            'activities': '/api/activities/',
            'semesters': '/api/semesters/',
        })
        data = {
            'message': 'Welcome to Student Management API',
            'api_endpoints': api_endpoints
        }
        
        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

def get_dashboard_context():
    """Lấy context chung cho dashboard"""
    return {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_teachers': Teacher.objects.filter(is_active=True).count(),
        'total_subjects': Subject.objects.filter(is_active=True).count(),
        'total_classes': Class.objects.filter(is_active=True).count(),

        'subjects_by_semester': Subject.objects.filter(is_active=True).values('semester').annotate(
            count=Count('subject_id')
        ),
        'recent_activities': Activity.objects.select_related('user').order_by('-created_at')[:10],
    }

@extend_schema(tags=['Authentication'])
class LoginAPIView(APIView):
    """API View cho đăng nhập"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Đăng nhập thành công',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role if hasattr(user, 'role') else None
                }
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Thông tin đăng nhập không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Authentication'])
class LogoutAPIView(APIView):
    """API View cho đăng xuất"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({'message': 'Đăng xuất thành công'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Profile'])
class ProfileAPIView(APIView):
    """API View cho hồ sơ người dùng"""
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Cập nhật hồ sơ thành công', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Profile'])
class ChangePasswordAPIView(APIView):
    """API View cho đổi mật khẩu"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Đổi mật khẩu thành công'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    """API endpoint cho quản lý người dùng"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        elif self.action == 'me':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Lấy thông tin người dùng hiện tại"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Đổi mật khẩu người dùng"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Đổi mật khẩu thành công'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)