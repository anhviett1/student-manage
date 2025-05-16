# Sử dụng image Python 3.10
FROM python:3.10

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn
COPY . .

# Tạo thư mục static và media
RUN mkdir -p /app/static /app/media

# Mở cổng
EXPOSE 8088

# Chạy ứng dụng với Gunicorn
CMD ["gunicorn", "student_be.wsgi:application", "--bind", "0.0.0.0:8088"]