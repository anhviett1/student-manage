FROM nginx:stable-alpine
RUN apk add --no-cache curl

# Create directories (optional, can be mounted instead)
RUN mkdir -p /usr/share/nginx/html/static
RUN mkdir -p /usr/share/nginx/html/media

# Expose HTTP and HTTPS ports

# Copy nginx config
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 

