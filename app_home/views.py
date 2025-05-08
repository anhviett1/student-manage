from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from app_student.models import Student
from app_teacher.models import Teacher
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from rest_framework import status, serializers

User = get_user_model()

# Signal handler được vô hiệu hóa - Admin sẽ tạo Student/Teacher từ trang admin
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     # Bỏ qua tự động tạo profile nếu là superuser
#     if instance.is_superuser:
#         return
# 
#     if created:
#         if hasattr(instance, 'role') and instance.role == 'student':
#             Student.objects.create(
#                 user=instance,
#                 first_name=instance.first_name if hasattr(instance, 'first_name') else instance.username,
#                 last_name=instance.last_name if hasattr(instance, 'last_name') else '',
#                 email=instance.email,
#                 phone_number='',  # Default empty phone
#                 date_of_birth='2000-01-01',  # Default date
#                 address='',
#                 city='',
#                 state=''
#             )
#         elif hasattr(instance, 'role') and instance.role == 'teacher':
#             Teacher.objects.create(
#                 user=instance,
#                 first_name=instance.first_name if hasattr(instance, 'first_name') else instance.username,
#                 last_name=instance.last_name if hasattr(instance, 'last_name') else '',
#                 email=instance.email,
#                 phone_number='',  # Default empty phone
#                 date_of_birth='2000-01-01',  # Default date
#                 address='',
#                 city='',
#                 state='',
#                 subject='',
#                 salary=0
#             )
#         elif hasattr(instance, 'role') and instance.role == 'admin':
#             # Admin profile creation logic if needed
#             pass
#     else:
#         if hasattr(instance, 'role') and instance.role == 'student':
#             try:
#                 student_profile = Student.objects.get(user=instance)
#                 student_profile.save()
#             except Student.DoesNotExist:
#                 pass
#         elif hasattr(instance, 'role') and instance.role == 'teacher':
#             try:
#                 teacher_profile = Teacher.objects.get(user=instance)
#                 teacher_profile.save()
#             except Teacher.DoesNotExist:
#                 pass
#         elif hasattr(instance, 'role') and instance.role == 'admin':
#             # Admin profile update logic if needed
#             pass

class HomeApiEndpointSerializer(serializers.Serializer):
    message = serializers.CharField()
    api_endpoints = serializers.DictField(child=serializers.CharField())

class HomeAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = HomeApiEndpointSerializer
    
    def get(self, request, format=None):
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

def home_view(request):
    return render(request, 'home.html')
