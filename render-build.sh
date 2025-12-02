#!/usr/bin/env bash

# Cài đặt các thư viện Python
pip install -r requirements.txt

# Tạo thư mục temp
mkdir -p temp
mkdir -p temp_segments
chmod 777 temp
chmod 777 temp_segments

# Lưu ý: FFmpeg cần được cài đặt qua apt.txt hoặc trong Dockerfile
# Render không hỗ trợ apt-get trong build script
# Nếu cần FFmpeg, thêm file apt.txt với nội dung: ffmpeg 
