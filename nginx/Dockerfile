# Use lightweight Nginx base image
FROM nginx:alpine


# Create directories (optional, can be mounted instead)
RUN mkdir -p /usr/share/nginx/html/static
RUN mkdir -p /usr/share/nginx/html/media

# Expose HTTP and HTTPS ports
EXPOSE 80
EXPOSE 443

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
