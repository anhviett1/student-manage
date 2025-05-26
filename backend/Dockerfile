# Sử dụng image Python 3.10
FROM python:3.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip/*

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

# Copy project files
COPY . .

# Set permissions
RUN chmod +x /app/manage.py

# Expose port
EXPOSE 8088

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8088/health/ || exit 1

# Run application
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8088", \
     "--workers", "3", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "api.wsgi:application"]