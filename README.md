# Hệ thống Quản lý Sinh viên

Hệ thống quản lý sinh viên toàn diện với các tính năng quản lý sinh viên, giảng viên, môn học, điểm số và đăng ký học.

## Tính năng chính

- Quản lý sinh viên
- Quản lý giảng viên
- Quản lý môn học
- Quản lý lớp học
- Quản lý học kỳ
- Quản lý điểm số
- Đăng ký học
- Theo dõi hoạt động

## Yêu cầu hệ thống

- Python 3.8+
- PostgreSQL 12+
- Docker và Docker Compose (tùy chọn)

## Cài đặt

### Cài đặt với Docker (Khuyến nghị)

1. Clone repository:
```bash
git clone https://github.com/your-username/student-manage.git
cd student-manage
```

2. Tạo file .env:
```bash
cp .env.example .env
# Chỉnh sửa các biến môi trường trong file .env
```

3. Chạy với Docker Compose:
```bash
docker-compose up -d
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

3. Tạo file .env và cấu hình database

4. Chạy migrations:
```bash
python manage.py migrate
```

5. Tạo superuser:
```bash
python manage.py createsuperuser
```

6. Chạy server:
```bash
python manage.py runserver
```

## Sử dụng

1. Truy cập admin panel tại `http://localhost:8000/admin`
2. Đăng nhập với tài khoản superuser
3. Bắt đầu quản lý hệ thống

## API Documentation

API documentation có sẵn tại:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Cấu trúc dự án

```
student-manage/
├── app_activity/        # Quản lý hoạt động
├── app_class/          # Quản lý lớp học
├── app_enrollment/     # Quản lý đăng ký học
├── app_home/          # Trang chủ
├── app_score/         # Quản lý điểm số
├── app_semester/      # Quản lý học kỳ
├── app_student/       # Quản lý sinh viên
├── app_subject/       # Quản lý môn học
├── app_teacher/       # Quản lý giảng viên
├── templates/         # Templates
├── static/           # Static files
├── media/            # Uploaded files
└── student_be/       # Backend configuration
```

## Phát triển

1. Tạo nhánh mới:
```bash
git checkout -b feature/your-feature
```

2. Commit changes:
```bash
git commit -m "Add your feature"
```

3. Push to GitHub:
```bash
git push origin feature/your-feature
```

## Testing

Chạy tests:
```bash
python manage.py test
```

## Deployment

1. Cấu hình production settings
2. Collect static files:
```bash
python manage.py collectstatic
```
3. Deploy với Docker hoặc server của bạn

## Bảo trì

- Backup database thường xuyên
- Kiểm tra logs
- Cập nhật dependencies
- Kiểm tra bảo mật

## Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License