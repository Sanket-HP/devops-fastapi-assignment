FROM nginx:1.27-alpine

# Remove default package configuration
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy our optimized, custom NGINX configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
