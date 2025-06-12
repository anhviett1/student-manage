from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from ..app_student.models import Student
from ..app_teacher.models import Teacher
from ..app_subject.models import Subject
from ..app_class.models import Class
from ..app_activity.models import Activity
from .models import Department
from .serializers import UserSerializer, DepartmentSerializer, ChangePasswordSerializer, UserProfileSerializer
from .permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrAdmin

User = get_user_model()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile based on role."""
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
    """Retrieve dashboard context data."""
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
    """API view for user login."""
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
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
    """API view for user logout."""
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
    """API view for user profile management."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Cập nhật hồ sơ thành công',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Users'])
class ChangePasswordAPIView(APIView):
    """API view for changing user password."""
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
    """API endpoint for managing users."""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        """Dynamic permission assignment based on action."""
        permission_classes = {
            'create': [IsAdmin],  # Only admins can create users
            'update': [IsAdmin],
            'partial_update': [IsAdmin],
            'destroy': [IsAdmin],
            'me': [IsAuthenticated],
            'list': [IsAdmin],  # Restrict list to admins
            'retrieve': [IsAdmin],  # Restrict retrieve to admins
        }.get(self.action, [IsAdminOrReadOnly])
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Set password and role during user creation."""
        user = serializer.save()
        user.set_password(serializer.validated_data.get('password', 'default_password123'))  # Default password
        user.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Retrieve current user's profile."""
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password via custom action."""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': 'Đổi mật khẩu thành công'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)