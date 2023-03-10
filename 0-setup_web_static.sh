#!/usr/bin/env bash
"""Prepare web servers"""
# Update package list and install Nginx
apt-get update
apt-get -y install nginx

# Create necessary directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership and group of directories
chown -R ubuntu:ubuntu /data/
chmod -R 755 /data/

# Update Nginx configuration file
sed -i '/listen 80 default_server;/a \ \n    location /hbnb_static {\n        alias /data/web_static/current/;\n        index index.html;\n    }' /etc/nginx/sites-available/default

# Restart Nginx
systemctl restart nginx

exit 0

