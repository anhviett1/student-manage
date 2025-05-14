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

## 🔧 Yêu cầu hệ thống

- **Python**: 3.9+
- **PostgreSQL**: 12+
- **Django**: 4.2+
- **Django REST Framework**: 3.14+
- **Docker** và **Docker Compose** (tùy chọn)

## 🚀 Cài đặt

### Cài đặt với Docker (Khuyến nghị)

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
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=student_manage
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=db
DB_PORT=5432
```

4. Chạy với Docker Compose:
```bash
docker-compose up -d
```

5. Tạo superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

### Cài đặt thủ công

1. Tạo môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Tạo file .env trong thư mục gốc và cấu hình:
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=student_manage
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
```

4. Tạo database PostgreSQL:
```bash
# Đăng nhập vào PostgreSQL
psql -U postgres

# Tạo database
CREATE DATABASE student_manage;
```

5. Chạy migrations:
```bash
python manage.py migrate
```

6. Tạo superuser:
```bash
python manage.py createsuperuser
```

7. Chạy server:
```bash
python manage.py runserver
```

## 🖥️ Sử dụng

1. Truy cập admin panel tại `http://localhost:8000/admin`
2. Đăng nhập với tài khoản superuser
3. Bắt đầu quản lý hệ thống
4. API có thể được truy cập tại `http://localhost:8000/api/v1/`

## 📚 API Documentation

API documentation có sẵn tại:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

API được phân loại theo các tag sau:
- 📚 Quản lý sinh viên (Students)
- 👨‍🏫 Quản lý giáo viên (Teachers)
- 📝 Quản lý môn học (Subjects)
- 🏫 Quản lý lớp học (Classes)
- 📊 Quản lý điểm số (Scores)
- 📋 Quản lý đăng ký học (Enrollments)
- 🗓️ Quản lý học kỳ (Semesters)
- 📆 Quản lý hoạt động (Activities)
- 🏠 Trang chủ (Home)

## 🏗️ Cấu trúc dự án

```
student-manage/
├── api_gateway/         # API gateway và routing
├── app_activity/        # Quản lý hoạt động
├── app_class/           # Quản lý lớp học
├── app_enrollment/      # Quản lý đăng ký học
├── app_home/            # Quản lý người dùng và trang chủ
├── app_score/           # Quản lý điểm số
├── app_semester/        # Quản lý học kỳ
├── app_student/         # Quản lý sinh viên
├── app_subject/         # Quản lý môn học
├── app_teacher/         # Quản lý giảng viên
├── templates/           # Templates HTML
├── static/              # Static files (CSS, JS, images)
├── media/               # Uploaded files
├── student_be/          # Backend configuration
│   ├── settings.py      # Cấu hình chính của project
│   ├── urls.py          # URL routing
│   ├── middleware.py    # Custom middleware
│   └── utils.py         # Utility functions
├── manage.py            # Django CLI
├── requirements.txt     # Dependencies
├── Dockerfile           # Cấu hình Docker
└── docker-compose.yml   # Cấu hình Docker Compose
```

## 📝 Mô tả các ứng dụng

- **app_home**: Quản lý người dùng, xác thực và trang chủ
- **app_student**: Quản lý thông tin sinh viên và hồ sơ học tập
- **app_teacher**: Quản lý giảng viên và phân công giảng dạy
- **app_subject**: Quản lý môn học, tín chỉ và yêu cầu điều kiện
- **app_class**: Quản lý lớp học, thời khóa biểu và phòng học
- **app_score**: Quản lý điểm số, tính toán GPA và theo dõi tiến độ học tập
- **app_enrollment**: Quản lý đăng ký học của sinh viên
- **app_semester**: Quản lý học kỳ và năm học
- **app_activity**: Theo dõi hoạt động của người dùng trong hệ thống

## 🧪 Phát triển

### Quy trình phát triển

1. Tạo nhánh mới:
```bash
git checkout -b feature/your-feature
```

2. Viết mã và kiểm tra:
```bash
python manage.py test
```

3. Commit changes:
```bash
git commit -m "Add your feature"
```

4. Push to GitHub:
```bash
git push origin feature/your-feature
```

5. Tạo Pull Request trên GitHub

### Coding Standards

- Tuân thủ PEP 8 cho Python code
- Sử dụng docstrings cho classes và functions
- Viết unit tests cho mọi chức năng mới
- Đặt tên biến và hàm bằng tiếng Anh, rõ ràng và mô tả

## 🧰 Testing

Chạy toàn bộ test suite:
```bash
python manage.py test
```

Chạy test cho một ứng dụng cụ thể:
```bash
python manage.py test app_student
```

Coverage report:
```bash
coverage run --source='.' manage.py test
coverage report
```

## 🚢 Deployment

### Chuẩn bị cho Production

1. Cập nhật cài đặt trong settings.py:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
```

2. Cấu hình HTTPS với Let's Encrypt

3. Collect static files:
```bash
python manage.py collectstatic
```

### Deployment với Docker

1. Cập nhật biến môi trường trong file .env.prod
2. Build và run containers:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Deployment với Gunicorn và Nginx

1. Cài đặt Gunicorn và Nginx
2. Cấu hình Gunicorn service
3. Cấu hình Nginx để proxy requests đến Gunicorn

## 🛠️ Bảo trì

- Backup database thường xuyên
- Cập nhật dependencies định kỳ
- Theo dõi logs để phát hiện và giải quyết vấn đề
- Kiểm tra bảo mật và cập nhật các lỗ hổng

## 📜 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Tạo Pull Request

## 📄 License

MIT License

## 📞 Liên hệ

Nếu bạn có câu hỏi hoặc góp ý, vui lòng liên hệ: example@example.com