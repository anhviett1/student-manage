# Sử dụng image Nginx Alpine (nhẹ)
FROM nginx:alpine

# Xóa cấu hình mặc định
RUN rm /etc/nginx/conf.d/default.conf

# Copy file cấu hình Nginx của chúng ta
COPY nginx.conf /etc/nginx/conf.d

# Tạo thư mục cho các file tĩnh (nếu cần)
RUN mkdir -p /usr/share/nginx/html/static
RUN mkdir -p /usr/share/nginx/html/media

# Expose port 80 (HTTP) và 443 (HTTPS - nếu cần)
EXPOSE 80
EXPOSE 443

# Khởi chạy Nginx
CMD ["nginx", "-g", "daemon off;"]