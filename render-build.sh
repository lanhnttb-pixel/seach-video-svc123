#!/usr/bin/env bash

# Cài đặt FFmpeg
apt-get update
apt-get install -y ffmpeg

# Cài đặt các thư viện Python
pip install -r requirements.txt

# Tạo thư mục temp
mkdir -p temp
mkdir -p temp_segments
chmod 777 temp
chmod 777 temp_segments

# Cấu hình Nginx (nếu có)
if [ -f /etc/nginx/nginx.conf ]; then
  echo "Configuring Nginx for large uploads..."
  sudo sed -i 's/client_max_body_size [0-9]*m;/client_max_body_size 10240m;/' /etc/nginx/nginx.conf
  sudo sed -i 's/proxy_read_timeout [0-9]*;/proxy_read_timeout 1800;/' /etc/nginx/nginx.conf
  sudo service nginx restart
fi 