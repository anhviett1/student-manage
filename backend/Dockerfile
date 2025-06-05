# Sử dụng image Python 3.11-slim
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

# Copy project files
COPY . .


RUN python manage.py collectstatic --noinput
# Cấp quyền thực thi
RUN chmod +x /app/manage.py

# Khởi chạy ứng dụng
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--forwarded-allow-ips", "*", \
     "api.student_be.wsgi:application"]

# Make manage.py executable
RUN chmod +x /app/manage.py

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=api.student_be.settings

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["gunicorn", "api.student_be.wsgi:application", "--bind", "0.0.0.0:8000"]

