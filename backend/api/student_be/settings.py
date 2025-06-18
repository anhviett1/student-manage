from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-kssc-dummykey-p+jx_h8-dt-nu-7@u=0-3cr5x0-fhsrp5takc"
)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # Set to True only for development
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Add CORS_ORIGIN_WHITELIST as a fallback
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "drf_spectacular",
    
    "api.app_student",
    "api.app_teacher",
    "api.app_home",
    "api.app_class",
    "api.app_score",
    "api.app_subject",
    "api.app_enrollment",
    "api.app_activity",
    "api.app_semester",
    "api.app_schedule",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS middleware should be as high as possible
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "api.student_be.urls"
WSGI_APPLICATION = "api.student_be.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Chỉ dùng template trong ứng dụng
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "student_manage_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "123456"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

LANGUAGE_CODE = "vi-vn"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "app_home.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Student Management API",
    "DESCRIPTION": "API for managing students, teachers, classes, subjects, scores, and enrollments",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v1",
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "displayRequestDuration": True,
        "filter": True,
        "docExpansion": "list",
        "deepLinking": True,
        "displayOperationId": True,
        "persistAuthorization": True,
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": 1,
    },
    "TAGS": [
        {"name": "Department", "description": "Quản lý khoa", "x-displayName": "📚 Quản lý khoa"},
        {
            "name": "Students",
            "description": "Quản lý sinh viên",
            "x-displayName": "📚 Quản lý sinh viên",
        },
        {
            "name": "Teachers",
            "description": "Quản lý giáo viên",
            "x-displayName": "👨‍🏫 Quản lý giáo viên",
        },
        {
            "name": "Subjects",
            "description": "Quản lý môn học",
            "x-displayName": "📝 Quản lý môn học",
        },
        {
            "name": "Classes",
            "description": "Quản lý lớp học",
            "x-displayName": "🏫 Quản lý lớp học",
        },
        {
            "name": "Schedule",
            "description": "Quản lý thời khóa biểu",
            "x-displayName": "🗓️ Quản lý thời khóa biểu",

        },
        {"name": "Semesters", "description": "Quản lý học kỳ", "x-displayName": "🗓️ Quản lý học kỳ"},
        {
            "name": "Enrollments",
            "description": "Quản lý đăng ký học",
            "x-displayName": "📋 Quản lý đăng ký học",
        },
        {"name": "Scores", "description": "Quản lý điểm số", "x-displayName": "📊 Quản lý điểm số"},
        {
            "name": "Activities",
            "description": "Quản lý hoạt động",
            "x-displayName": "📆 Quản lý hoạt động",
        },
    ],
    "TAG_NAMESPACES": True,
    "ENUM_NAME_OVERRIDES": {},
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

ADMIN_URL = "admin/"
ADMIN_SITE_HEADER = "Hệ thống Quản lý Sinh viên"
ADMIN_SITE_TITLE = "Quản lý Sinh viên"
ADMIN_INDEX_TITLE = "Trang quản trị"

LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "admin:index"
LOGOUT_REDIRECT_URL = "admin:login"
