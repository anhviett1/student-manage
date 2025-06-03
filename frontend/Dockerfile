# Build stage
FROM node:18-alpine as build-stage

WORKDIR /app

# Cài đặt các dependencies cần thiết
RUN apk add --no-cache python3 make g++ curl

# Copy package files
COPY package*.json ./

# Kiểm tra phiên bản Node.js và npm
RUN node -v && npm -v

# Cài đặt dependencies
RUN npm install && \
    npm cache clean --force

# Copy source code
COPY . .

# Build ứng dụng
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage

# Cài đặt curl cho healthcheck
RUN apk add --no-cache curl

# Copy build files từ build-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html


# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]