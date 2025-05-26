# Build stage
FROM node:18.19.0-alpine as build-stage

WORKDIR /app

# Cài đặt các dependencies cần thiết
RUN apk add --no-cache python3 make g++ curl

# Copy package files
COPY package*.json ./

# Kiểm tra và hiển thị phiên bản Node.js và npm
RUN node -v && npm -v

# Cài đặt dependencies
RUN npm install && \
    npm cache clean --force

# Copy source code
COPY . .

# Kiểm tra cấu trúc thư mục
RUN ls -la

# Build ứng dụng
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage

# Cài đặt curl cho healthcheck
RUN apk add --no-cache curl

# Copy build files
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 