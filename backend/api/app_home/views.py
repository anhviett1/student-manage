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
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from app_student.models import Student
from app_teacher.models import Teacher
from app_subject.models import Subject
from app_class.models import Class
from app_activity.models import Activity
from .forms import ChangePasswordForm, UserProfileForm
from .models import Department, Role
from .serializers import UserSerializer, DepartmentSerializer, RoleSerializer

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

@extend_schema(tags=['Home'])
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
        }
        
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
        # 'student_by_faculty': Student.objects.filter(is_active=True).values('faculty').annotate(
        #     count=Count('student_id')
        # ),
        'subjects_by_semester': Subject.objects.filter(is_active=True).values('semester').annotate(
            count=Count('subject_id')
        ),
        'recent_activities': Activity.objects.select_related('user').order_by('-created_at')[:10],
    }

def home_view(request):
    """View cho trang chủ"""
    return render(request, 'index.html', get_dashboard_context())

def dashboard_view(request):
    """View cho dashboard"""
    return home_view(request)

@login_required
def home(request):
    """View cho trang chủ đã đăng nhập"""
    return render(request, 'index.html', get_dashboard_context())

@login_required
def change_password(request):
    """View cho trang đổi mật khẩu"""
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_change_done')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'app_home_fe/change_password.html', {'form': form})

def login_view(request):
    """View cho trang đăng nhập"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app_home_fe/login.html', {'form': form})

@login_required
def logout_view(request):
    """View cho đăng xuất"""
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    """View cho trang hồ sơ"""
    user = request.user
    context = {
        'title': _('Hồ sơ'),
        'user': user,
        'profile': user,
        'form': None
    }
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _('Cập nhật hồ sơ thành công!'))
                return redirect('home:profile')
            except Exception as e:
                messages.error(request, _('Có lỗi xảy ra khi cập nhật hồ sơ. Vui lòng thử lại.'))
                if settings.DEBUG:
                    messages.error(request, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = UserProfileForm(instance=user)
    
    context['form'] = form
    return render(request, 'app_home_fe/profile.html', context)

@login_required
def home_be_view(request):
    """
    View function cho trang home_be.html
    """
    # Lấy thông tin thống kê
    total_students = User.objects.filter(role__name='student').count()
    total_teachers = User.objects.filter(role__name='teacher').count()
    total_subjects = Department.objects.count()
    total_classes = Department.objects.count()

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_subjects': total_subjects,
        'total_classes': total_classes,
    }
    return render(request, 'app_home/home_be.html', context)