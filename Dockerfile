# Sử dụng Python image
FROM python:3.10.11

# Cài đặt thư mục làm việc
WORKDIR /app

# Copy code vào container
COPY . /app/

# Cài đặt các thư viện cần thiết
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Migrate và runserver mặc định (hoặc để docker-compose run)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
