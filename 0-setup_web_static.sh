#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

# Exit on error
set -e

# Update package list and install Nginx
sudo apt-get update
sudo apt-get install -y nginx

# Remove existing Nginx default configuration file
sudo rm /etc/nginx/sites-enabled/default || true

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create fake HTML file
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html >/dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership and group of directories
sudo chown -R ubuntu:ubuntu /data/
sudo chmod -R 755 /data/

# Update Nginx configuration file
sudo printf %s "\
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" | sudo tee /etc/nginx/sites-available/default >/dev/null

# Create symbolic link to enable the Nginx configuration
sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Restart Nginx
sudo systemctl restart nginx

exit 0

