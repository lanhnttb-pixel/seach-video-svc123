# Video Tools - Tìm kiếm & Xử lý Video

Ứng dụng web cho phép tìm kiếm video trên nhiều nền tảng toàn cầu và xử lý video (chia nhỏ video).

## Tính năng

1. **Tìm kiếm video trên nhiều nền tảng**
   - Hỗ trợ 40+ nền tảng video từ nhiều quốc gia
   - Tự động dịch từ khóa tiếng Việt sang các ngôn ngữ khác
   - Tùy chọn nền tảng tìm kiếm và ngôn ngữ dịch

2. **Chia nhỏ video**
   - Chia video thành nhiều phần có độ dài bằng nhau
   - Hỗ trợ định dạng MP4, AVI, MKV, MOV
   - Tạo file ZIP để tải xuống tất cả các phần

## Cài đặt

### Cài đặt trên máy cá nhân

1. **Cài đặt Python**
   - Khuyến nghị sử dụng WinPython 64-bit hoặc Python 3.8+
   - Đảm bảo pip đã được cài đặt

2. **Cài đặt FFmpeg**
   - Tải FFmpeg từ [ffmpeg.org](https://www.ffmpeg.org/download.html)
   - Hoặc sử dụng lệnh: `winget install FFmpeg` (Windows)

3. **Cài đặt các thư viện Python**
   ```
   pip install -r requirements.txt
   ```

4. **Chạy ứng dụng**
   ```
   streamlit run main.py
   ```

### Triển khai trên Render.com

1. Đẩy mã nguồn lên GitHub (không bao gồm file FFmpeg)
2. Tạo tài khoản trên [Render.com](https://render.com)
3. Tạo dịch vụ mới và kết nối với repository GitHub
4. Cấu hình như sau:
   - **Environment**: Python
   - **Build Command**: `chmod +x render-build.sh && ./render-build.sh`
   - **Start Command**: `streamlit run main.py`
5. Nhấp vào "Create Web Service"

## Yêu cầu

- Python 3.8+
- FFmpeg
- Các thư viện được liệt kê trong `requirements.txt`

## Giấy phép

MIT License 