# Hệ thống Quản lý Sinh viên (Student Management System)

Hệ thống quản lý sinh viên toàn diện với các tính năng quản lý sinh viên, giảng viên, môn học, điểm số và đăng ký học, được xây dựng trên Django và Django REST Framework.

## 📋 Tính năng chính

- **Quản lý sinh viên**: Thêm, sửa, xóa, tìm kiếm và quản lý thông tin sinh viên
- **Quản lý giảng viên**: Theo dõi thông tin và lịch dạy của giảng viên
- **Quản lý môn học**: Tạo và quản lý thông tin môn học, tín chỉ và điều kiện tiên quyết
- **Quản lý lớp học**: Sắp xếp lớp học, điểm danh và quản lý thời khóa biểu
- **Quản lý học kỳ**: Tạo và quản lý thông tin các học kỳ trong năm học
- **Quản lý điểm số**: Nhập, xuất và phân tích điểm số của sinh viên
- **Đăng ký học**: Hỗ trợ sinh viên đăng ký và quản lý môn học
- **Theo dõi hoạt động**: Ghi nhận các hoạt động của người dùng trong hệ thống
- **Xác thực JWT**: Bảo mật API với JSON Web Tokens
- **API Documentation**: Tài liệu API tự động với Swagger/ReDoc

## 👥 Phân quyền người dùng

### 1. Admin
- **Quyền quản lý**:
  - Quản lý sinh viên (CRUD)
  - Quản lý giảng viên (CRUD)
  - Quản lý lớp học (CRUD)
  - Quản lý môn học (CRUD)
  - Quản lý điểm số (CRUD)
  - Quản lý đăng ký học (CRUD)
  - Quản lý học kỳ (CRUD)
  - Xem báo cáo và thống kê

### 2. Giảng viên
- **Quyền quản lý**:
  - Xem thông tin lớp học
  - Xem thông tin môn học
  - Nhập và cập nhật điểm số
  - Xem lịch giảng dạy
  - Quản lý lịch giảng dạy

### 3. Sinh viên
- **Quyền truy cập**:
  - Xem thông tin cá nhân
  - Xem điểm số của mình
  - Đăng ký môn học
  - Xem lịch học

## 🔒 Permissions

### Admin Permissions
```python
permissions = [
    ("can_manage_students", "Có thể quản lý sinh viên"),
    ("can_manage_teachers", "Có thể quản lý giảng viên"),
    ("can_manage_classes", "Có thể quản lý lớp học"),
    ("can_manage_subjects", "Có thể quản lý môn học"),
    ("can_manage_scores", "Có thể quản lý điểm số"),
    ("can_manage_enrollments", "Có thể quản lý đăng ký"),
    ("can_view_reports", "Có thể xem báo cáo"),
]
```

### Teacher Permissions
```python
permissions = [
    ("can_view_teacher_details", "Có thể xem thông tin giảng viên"),
    ("can_manage_teacher", "Có thể quản lý giảng viên"),
    ("can_view_teacher_schedule", "Có thể xem lịch giảng dạy"),
    ("can_manage_teacher_schedule", "Có thể quản lý lịch giảng dạy"),
]
```

### Student Permissions
```python
permissions = [
    ("can_view_student_details", "Có thể xem thông tin sinh viên"),
    ("can_view_student_grades", "Có thể xem điểm sinh viên"),
]
```

## 🚀 Cài đặt với Docker

### 1. Yêu cầu hệ thống
- Docker
- Docker Compose
- Git

### 2. Cài đặt

1. Clone repository:
```bash
git clone https://github.com/your-username/student-manage.git
cd student-manage
```

2. Tạo file .env:
```bash
cp .env.example .env
```

3. Chỉnh sửa các biến môi trường trong file .env:
```env
# Backend
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=student_manage
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=db
DB_PORT=5432

# Frontend
VITE_API_URL=http://localhost:8088/api
```

4. Build và chạy containers:
```bash
docker-compose up -d --build
```

5. Tạo superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

### 3. Truy cập ứng dụng
- Frontend: http://localhost:80
- Backend API: http://localhost:8088
- Admin Panel: http://localhost:8088/admin
- API Documentation: http://localhost:8088/api/docs/

## 🏗️ Cấu trúc dự án

```
student-manage/
├── frontend/           # Vue.js frontend
│   ├── src/
│   │   ├── components/ # Vue components
│   │   ├── views/     # Page views
│   │   ├── stores/    # Pinia stores
│   │   ├── services/  # API services
│   │   └── router/    # Vue Router
│   └── Dockerfile     # Frontend Dockerfile
│
├── backend/           # Django backend
│   ├── api/          # Django apps
│   │   ├── app_home/        # User management
│   │   ├── app_student/     # Student management
│   │   ├── app_teacher/     # Teacher management
│   │   ├── app_subject/     # Subject management
│   │   ├── app_class/       # Class management
│   │   ├── app_score/       # Score management
│   │   ├── app_enrollment/  # Enrollment management
│   │   └── app_semester/    # Semester management
│   └── Dockerfile    # Backend Dockerfile
│
└── docker-compose.yml # Docker Compose configuration
```

## 🧪 Testing

### Backend Tests
```bash
docker-compose exec backend python manage.py test
```

### Frontend Tests
```bash
docker-compose exec frontend npm run test
```

## 📚 API Documentation

API documentation có sẵn tại:
- Swagger UI: http://localhost:8088/api/docs/
- ReDoc: http://localhost:8088/api/redoc/

## 🛠️ Bảo trì

- Backup database thường xuyên
- Cập nhật dependencies định kỳ
- Theo dõi logs để phát hiện và giải quyết vấn đề
- Kiểm tra bảo mật và cập nhật các lỗ hổng

## 📄 License

MIT License

## 📞 Liên hệ

Nếu bạn có câu hỏi hoặc góp ý, vui lòng liên hệ: example@example.com