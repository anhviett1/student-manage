# Build stage
FROM node:18-alpine as build-stage

WORKDIR /app

# Cài đặt dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build ứng dụng với production mode
ENV NODE_ENV=production
RUN npm run build

# Production stage
FROM nginx:stable-alpine

# Copy build files từ build-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html


# Tạo thư mục và set quyền
RUN mkdir -p /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]