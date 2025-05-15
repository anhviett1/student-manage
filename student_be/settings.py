# student_be/settings.py
from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-kssc$dtafz&%p+jx_h8-dt)n+u+7@u=0!3cr5x0!fhsrp5takc')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow localhost and 127.0.0.1 for development
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'allauth',
    'allauth.account',
    
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'drf_spectacular',
    'corsheaders',
    
    'api_gateway',
    'app_student',
    'app_teacher',
    'app_home',
    'app_class',
    'app_score',
    'app_subject',
    'app_enrollment',
    'app_activity',
    'app_semester',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'student_be.middleware.CloseConnectionMiddleware',
]

# Remove duplicate SecurityMiddleware (it was listed twice in your original settings)
# Ensure middleware order is correct as per Django documentation

ROOT_URLCONF = 'student_be.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'student_be.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'student_manage_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', '123456'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 0,  # Close connections immediately after each request
        'OPTIONS': {
            'connect_timeout': 5,
            'application_name': 'django_app',
            'client_encoding': 'UTF8',
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'  # Corrected to match your requirement
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'app_home.User'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    
}

# Simple JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# DRF Spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Student Management API',
    'DESCRIPTION': 'API for managing students, teachers, classes, subjects, scores, and enrollments',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'displayRequestDuration': True,
        'filter': True,
        'docExpansion': 'list',  # Các endpoint được mở theo danh sách
        'deepLinking': True,
        'displayOperationId': False,
        'persistAuthorization': True,
        'defaultModelsExpandDepth': -1,  # Đóng tất cả các model
        'defaultModelExpandDepth': 1,  # Mở model đến cấp độ 1
    },
    'TAGS': [
        {'name': 'Students', 'description': 'Quản lý sinh viên', 'x-displayName': '📚 Quản lý sinh viên'},
        {'name': 'Teachers', 'description': 'Quản lý giáo viên', 'x-displayName': '👨‍🏫 Quản lý giáo viên'},
        {'name': 'Subjects', 'description': 'Quản lý môn học', 'x-displayName': '📝 Quản lý môn học'},
        {'name': 'Classes', 'description': 'Quản lý lớp học', 'x-displayName': '🏫 Quản lý lớp học'},
        {'name': 'Scores', 'description': 'Quản lý điểm số', 'x-displayName': '📊 Quản lý điểm số'},
        {'name': 'Enrollments', 'description': 'Quản lý đăng ký học', 'x-displayName': '📋 Quản lý đăng ký học'},
        {'name': 'Semesters', 'description': 'Quản lý học kỳ', 'x-displayName': '🗓️ Quản lý học kỳ'},
        {'name': 'Activities', 'description': 'Quản lý hoạt động', 'x-displayName': '📆 Quản lý hoạt động'},
        {'name': 'Home', 'description': 'Quản lý người dùng và trang chủ', 'x-displayName': '🏠 Trang chủ'},
    ],
    'TAG_NAMESPACES': True,  # Use namespace as tags for better organization
    'ENUM_NAME_OVERRIDES': {},
}

