FROM nginx:stable-alpine

# Cài đặt curl cho healthcheck
RUN apk add --no-cache curl

# Copy nginx config
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 