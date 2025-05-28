# Sử dụng image Python 3.11
FROM python:3.11

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Cài đặt các dependencies hệ thống
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Cài đặt các dependencies Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip/*

# Tạo các thư mục cần thiết
RUN mkdir -p /app/staticfiles /app/media

# Copy toàn bộ source code
COPY . .

# Cấp quyền thực thi
RUN chmod +x /app/manage.py

# Expose port
EXPOSE 8088

# Khởi chạy ứng dụng
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8088", \
     "--workers", "3", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--forwarded-allow-ips", "*", \
     "api.student_be.wsgi:application"]