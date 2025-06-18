"""
API Documentation module for Student Management System.

This module provides auto-generated documentation for the Student Management API using drf_spectacular.
It includes customization for Swagger and ReDoc outputs, as well as detailed descriptions for each endpoint.
"""

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Schema generation endpoint
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI documentation
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # ReDoc documentation
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Documentation customization settings
spectacular_settings = {
    "TITLE": "Student Management API",
    "DESCRIPTION": """
        ## Hệ thống Quản lý Sinh viên API
        
        API này cung cấp các endpoints để quản lý dữ liệu về sinh viên, giảng viên, lớp học, môn học và các hoạt động khác trong môi trường giáo dục.
        
        ### Xác thực
        Sử dụng JWT (JSON Web Tokens) cho xác thực API. Để lấy token, sử dụng endpoint `/api/v1/token/`.
        
        ### Phiên bản
        Phiên bản hiện tại: 1.0.0
    """,
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v1",
    # Swagger UI customization
    "SWAGGER_UI_SETTINGS": {
        "displayRequestDuration": True,
        "filter": True,
        "docExpansion": "list",
        "deepLinking": True,
        "displayOperationId": False,
        "persistAuthorization": True,
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": 1,
    },
    # Tags customization with emojis and descriptions
    "TAGS": [
        {
            "name": "students",
            "description": "Quản lý sinh viên",
            "x-displayName": "📚 Quản lý sinh viên",
        },
        {
            "name": "teachers",
            "description": "Quản lý giáo viên",
            "x-displayName": "👨‍🏫 Quản lý giáo viên",
        },
        {
            "name": "subjects",
            "description": "Quản lý môn học",
            "x-displayName": "📝 Quản lý môn học",
        },
        {
            "name": "classes",
            "description": "Quản lý lớp học",
            "x-displayName": "🏫 Quản lý lớp học",
        },
        {"name": "scores", "description": "Quản lý điểm số", "x-displayName": "📊 Quản lý điểm số"},
        {
            "name": "enrollments",
            "description": "Quản lý đăng ký học",
            "x-displayName": "📋 Quản lý đăng ký học",
        },
        {"name": "semesters", "description": "Quản lý học kỳ", "x-displayName": "🗓️ Quản lý học kỳ"},
        {
            "name": "activities",
            "description": "Quản lý hoạt động",
            "x-displayName": "📆 Quản lý hoạt động",
        },
        {
            "name": "home",
            "description": "Quản lý người dùng và trang chủ",
            "x-displayName": "🏠 Trang chủ",
        },
        {"name": "auth", "description": "Xác thực và phân quyền", "x-displayName": "🔒 Xác thực"},
    ],
    # Use namespace as tags for better organization
    "TAG_NAMESPACES": True,
    # Custom responses
    "GENERIC_RESPONSE_DEFINITIONS": {
        "StandardError": {
            "type": "object",
            "properties": {
                "detail": {"type": "string"},
                "code": {"type": "string"},
            },
        },
        "ValidationError": {
            "type": "object",
            "properties": {"field_name": {"type": "array", "items": {"type": "string"}}},
        },
    },
    # Components for documentation
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_SPLIT_RESPONSE": True,
    # Additional customization
    "ENUM_NAME_OVERRIDES": {},
    "PREPROCESSING_HOOKS": [],
    "POSTPROCESSING_HOOKS": [],
}


def get_schema_view():
    """
    Returns the schema view with authentication classes.

    This function can be used to add authentication classes to schema view if needed.
    """
    return SpectacularAPIView.as_view()


def render_documentation():
    """
    Function to handle any custom documentation rendering.
    """
    pass


# API version information
API_VERSION = "1.0.0"
API_BASE_PATH = "/api/v1/"

# Documentation sections
DOCUMENTATION_SECTIONS = {
    "authentication": {
        "title": "Authentication",
        "description": "Xác thực bằng JWT token",
        "endpoints": [
            {"path": "/api/v1/token/", "method": "POST", "description": "Lấy JWT token"},
            {
                "path": "/api/v1/token/refresh/",
                "method": "POST",
                "description": "Làm mới JWT token",
            },
            {
                "path": "/api/v1/token/verify/",
                "method": "POST",
                "description": "Xác thực JWT token",
            },
        ],
    },
    "students": {
        "title": "Student Management",
        "description": "Quản lý thông tin sinh viên",
        "endpoints": [
            {
                "path": "/api/v1/students/",
                "method": "GET",
                "description": "Lấy danh sách sinh viên",
            },
            {
                "path": "/api/v1/students/{id}/",
                "method": "GET",
                "description": "Lấy thông tin chi tiết sinh viên",
            },
            {"path": "/api/v1/students/", "method": "POST", "description": "Tạo sinh viên mới"},
            {
                "path": "/api/v1/students/{id}/",
                "method": "PUT",
                "description": "Cập nhật thông tin sinh viên",
            },
            {"path": "/api/v1/students/{id}/", "method": "DELETE", "description": "Xóa sinh viên"},
        ],
    },
    "teachers": {
        "title": "Teacher Management",
        "description": "Quản lý thông tin giáo viên",
        "endpoints": [
            {
                "path": "/api/v1/teachers/",
                "method": "GET",
                "description": "Lấy danh sách giáo viên",
            },
            {
                "path": "/api/v1/teachers/{id}/",
                "method": "GET",
                "description": "Lấy thông tin chi tiết giáo viên",
            },
            {"path": "/api/v1/teachers/", "method": "POST", "description": "Tạo giáo viên mới"},
            {
                "path": "/api/v1/teachers/{id}/",
                "method": "PUT",
                "description": "Cập nhật thông tin giáo viên",
            },
            {"path": "/api/v1/teachers/{id}/", "method": "DELETE", "description": "Xóa giáo viên"},
        ],
    },
    # Add other sections as needed
}
