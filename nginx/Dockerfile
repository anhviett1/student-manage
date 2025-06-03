<<<<<<< HEAD
# Use lightweight Nginx base image
FROM nginx:alpine


# Create directories (optional, can be mounted instead)
RUN mkdir -p /usr/share/nginx/html/static
RUN mkdir -p /usr/share/nginx/html/media

# Expose HTTP and HTTPS ports
=======
FROM nginx:stable-alpine

# Cài đặt curl cho healthcheck
RUN apk add --no-cache curl

# Copy nginx config
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

>>>>>>> 7ee0b4ac6d7b4e7ceca6d7faa9cdde2ade62a9bb
EXPOSE 80

<<<<<<< HEAD
# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
=======
CMD ["nginx", "-g", "daemon off;"] 
>>>>>>> 7ee0b4ac6d7b4e7ceca6d7faa9cdde2ade62a9bb
