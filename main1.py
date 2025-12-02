import streamlit as st
from googletrans import Translator
from PIL import Image
import requests
from io import BytesIO
import json
import re
from urllib.parse import quote
import os
import time
from pathlib import Path
import tempfile
import io
import zipfile
import subprocess
import urllib.request

class VideoDownloader:
    def __init__(self):
        # Thêm từ điển ánh xạ các từ khóa phổ biến
        self.keyword_mapping = {
            "hoạt hình xuyên không": "穿越动漫",
            "hoạt hình tu tiên": "修仙动漫",
            "tu tiên": "修仙",
            "xuyên không": "穿越",
            "hoạt hình": "动漫",
            "hài hước": "搞笑",
            "nhạc trẻ": "流行音乐",
            "phim": "电影",
            "game": "游戏",
            "anime": "动画",
            "tiên hiệp": "仙侠",
            "kiếm hiệp": "武侠",
            "tu chân": "修真",
            "tu tiên giả tưởng": "修仙玄幻"
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Cấu hình cho các nền tảng video toàn cầu
        self.platforms = {
            "YouTube": {
                "func": self.search_youtube,
                "color": "#FF0000",
                "icon": "📺"
            },
            "Vimeo": {
                "func": self.search_vimeo,
                "color": "#1AB7EA",
                "icon": "🎥"
            },
            "Dailymotion": {
                "func": self.search_dailymotion,
                "color": "#0066DC",
                "icon": "🎬"
            },
            "Douyin": {
                "func": self.search_douyin,
                "color": "#FF4B4B",
                "icon": "🎵"
            },
            "Bilibili": {
                "func": self.search_bilibili,
                "color": "#FB7299",
                "icon": "🎮"
            },
            "Niconico": {
                "func": self.search_niconico,
                "color": "#252525",
                "icon": "🎪"
            },
            "Twitch": {
                "func": self.search_twitch,
                "color": "#6441A4",
                "icon": "🎮"
            },
            "Facebook": {
                "func": self.search_facebook,
                "color": "#1877F2",
                "icon": "📱"
            },
            "Instagram": {
                "func": self.search_instagram,
                "color": "#E4405F",
                "icon": "📸"
            },
            "TikTok": {
                "func": self.search_tiktok,
                "color": "#000000",
                "icon": "🎵"
            },
            "xigua": {
                "func": self.search_xigua,
                "color": "#1E88E5",
                "icon": "📺"
            },
            "Youku": {
                "func": self.search_youku,
                "color": "#2196F3",
                "icon": "🇨🇳"
            },
            "WeTV": {
                "func": self.search_wetv,
                "color": "#4CAF50",
                "icon": "🇨🇳"
            },
            "iQIYI": {
                "func": self.search_iqiyi,
                "color": "#00C853",
                "icon": "🇨🇳"
            },
            "Naver TV": {
                "func": self.search_navertv,
                "color": "#00C853",
                "icon": "🇰🇷"
            },
            "Kakao TV": {
                "func": self.search_kakaotv,
                "color": "#FFC107",
                "icon": "🇰🇷"
            },
            "Rutube": {
                "func": self.search_rutube,
                "color": "#E53935",
                "icon": "🇷🇺"
            },
            "VK Video": {
                "func": self.search_vkvideo,
                "color": "#1976D2",
                "icon": "🇷🇺"
            },
            "Hotstar": {
                "func": self.search_hotstar,
                "color": "#039BE5",
                "icon": "🇮🇳"
            },
            "JioTV": {
                "func": self.search_jiotv,
                "color": "#3949AB",
                "icon": "🇮🇳"
            },
            "Globo Play": {
                "func": self.search_globoplay,
                "color": "#4CAF50",
                "icon": "🇧🇷"
            },
            "DailyTube": {
                "func": self.search_dailytube,
                "color": "#FFC107",
                "icon": "🇹🇭"
            },
            "Vidio": {
                "func": self.search_vidio,
                "color": "#FF5722",
                "icon": "🇮🇩"
            },
            "TudouVideo": {
                "func": self.search_tudou,
                "color": "#FF9800",
                "icon": "🇨🇳"
            },
            "YY Live": {
                "func": self.search_yylive,
                "color": "#00BCD4",
                "icon": "🇨🇳"
            },
            "Odnoklassniki": {
                "func": self.search_odnoklassniki,
                "color": "#FF9800",
                "icon": "🇷🇺"
            },
            "Abema TV": {
                "func": self.search_abematv,
                "color": "#F44336",
                "icon": "🇯🇵"
            },
            "TVer": {
                "func": self.search_tver,
                "color": "#4CAF50",
                "icon": "🇯🇵"
            },
            "GYAO!": {
                "func": self.search_gyao,
                "color": "#E91E63",
                "icon": "🇯🇵"
            },
            "Afreeca TV": {
                "func": self.search_afreecatv,
                "color": "#FF5722",
                "icon": "🇰🇷"
            },
            "Pandora TV": {
                "func": self.search_pandoratv,
                "color": "#9C27B0",
                "icon": "🇷🇷"
            },
            "VTV Go": {
                "func": self.search_vtvgo,
                "color": "#0D47A1",
                "icon": "🇻🇳"
            },
            "SCTV": {
                "func": self.search_sctv,
                "color": "#1565C0",
                "icon": "🇻🇳"
            },
            "FPT Play": {
                "func": self.search_fptplay,
                "color": "#D50000",
                "icon": "🇻🇳"
            },
            "VIVA TV": {
                "func": self.search_vivatv,
                "color": "#7B1FA2",
                "icon": "🇻🇳"
            },
            "HTV": {
                "func": self.search_htv,
                "color": "#0097A7",
                "icon": "🇻🇳"
            },
            "Keeng": {
                "func": self.search_keeng,
                "color": "#F57F17",
                "icon": "🇻🇳"
            },
            "Liên Quân Garena": {
                "func": self.search_lienquan,
                "color": "#33691E",
                "icon": "🇻🇳"
            },
            "MyTV": {
                "func": self.search_mytv,
                "color": "#880E4F",
                "icon": "🇻🇳"
            },
            "VieON": {
                "func": self.search_vieon,
                "color": "#3E2723",
                "icon": "🇻🇳"
            },
            "Zing TV": {
                "func": self.search_zingtv,
                "color": "#004D40",
                "icon": "🇻🇳"
            },
            "K+": {
                "func": self.search_kplus,
                "color": "#1A237E",
                "icon": "🇻🇳"
            },
            "TVB": {
                "func": self.search_tvb,
                "color": "#01579B",
                "icon": "🇭🇰"
            },
            "Sohu TV": {
                "func": self.search_sohu,
                "color": "#B71C1C",
                "icon": "🇨🇳"
            },
            "ABS-CBN": {
                "func": self.search_abscbn,
                "color": "#4A148C",
                "icon": "🇵🇭"
            },
            "BBC iPlayer": {
                "func": self.search_bbciplayer,
                "color": "#006064",
                "icon": "🇬🇧"
            },
            "France TV": {
                "func": self.search_francetv,
                "color": "#0D47A1",
                "icon": "🇫🇷"
            },
            "ARD Mediathek": {
                "func": self.search_ardmediathek,
                "color": "#00695C",
                "icon": "🇩🇪"
            },
            "RAI Play": {
                "func": self.search_raiplay,
                "color": "#311B92",
                "icon": "🇮🇹"
            },
            "RTVE Play": {
                "func": self.search_rtveplay,
                "color": "#BF360C",
                "icon": "🇪🇸"
            },
            "CBC Gem": {
                "func": self.search_cbcgem,
                "color": "#827717",
                "icon": "🇨🇦"
            }
        }

    def search_douyin(self, keyword):
        """Tìm kiếm video trên Douyin"""
        encoded_keyword = quote(keyword)
        search_url = f"https://www.douyin.com/search/{encoded_keyword}"
        return search_url
    
    def search_xigua(self, keyword):
        """Tìm kiếm video trên Xigua"""
        encoded_keyword = quote(keyword)
        search_url = f"https://www.ixigua.com/search/{encoded_keyword}"
        return search_url

    def search_bilibili(self, keyword):
        """Tìm kiếm video trên Bilibili"""
        encoded_keyword = quote(keyword)
        search_url = f"https://search.bilibili.com/all?keyword={encoded_keyword}"
        return search_url

    def search_youku(self, keyword):
        """Tìm kiếm video trên Youku"""
        encoded_keyword = quote(keyword)
        search_url = f"https://so.youku.com/search_video/q_{encoded_keyword}"
        return search_url

    def search_weibo(self, keyword):
        """Tìm kiếm video trên Weibo"""
        encoded_keyword = quote(keyword)
        search_url = f"https://s.weibo.com/video?q={encoded_keyword}"
        return search_url
        
    def search_kuaishou(self, keyword):
        """Tìm kiếm video trên Kuaishou"""
        encoded_keyword = quote(keyword)
        search_url = f"https://www.kuaishou.com/search/video?searchKey={encoded_keyword}"
        return search_url

    # Các hàm tìm kiếm mới
    def search_youtube(self, keyword):
        encoded_keyword = quote(keyword)
        return f"https://www.youtube.com/results?search_query={encoded_keyword}"

    def search_vimeo(self, keyword):
        encoded_keyword = quote(keyword)
        return f"https://vimeo.com/search?q={encoded_keyword}"

    def search_dailymotion(self, keyword):
        encoded_keyword = quote(keyword)
        return f"https://www.dailymotion.com/search/{encoded_keyword}"

    def search_niconico(self, keyword):
        encoded_keyword = quote(keyword)
        return f"https://www.nicovideo.jp/search/{encoded_keyword}"

    def search_twitch(self, keyword):
        encoded_keyword = quote(keyword)
        return f"https://www.twitch.tv/search?term={encoded_keyword}"

    def search_facebook(self, keyword):
        encoded_keyword = quote(keyword)
        return f"https://www.facebook.com/search/videos/?q={encoded_keyword}"

    def search_instagram(self, keyword):
        encoded_keyword = quote(keyword)
        return f"https://www.instagram.com/explore/tags/{encoded_keyword}"

    def search_tiktok(self, keyword):
        encoded_keyword = quote(keyword)
        return f"https://www.tiktok.com/search?q={encoded_keyword}"

    # Các trang video quốc tế
    def search_wetv(self, keyword):
        """Tìm kiếm video trên WeTV"""
        encoded_keyword = quote(keyword)
        return f"https://wetv.vip/search?keyword={encoded_keyword}"
    
    def search_iqiyi(self, keyword):
        """Tìm kiếm video trên iQIYI"""
        encoded_keyword = quote(keyword)
        return f"https://www.iq.com/search?query={encoded_keyword}"
    
    def search_navertv(self, keyword):
        """Tìm kiếm video trên Naver TV"""
        encoded_keyword = quote(keyword)
        return f"https://tv.naver.com/search/clip?query={encoded_keyword}"
    
    def search_kakaotv(self, keyword):
        """Tìm kiếm video trên Kakao TV"""
        encoded_keyword = quote(keyword)
        return f"https://tv.kakao.com/search?q={encoded_keyword}"
        
    def search_rutube(self, keyword):
        """Tìm kiếm video trên Rutube"""
        encoded_keyword = quote(keyword)
        return f"https://rutube.ru/search/?query={encoded_keyword}"
        
    def search_vkvideo(self, keyword):
        """Tìm kiếm video trên VK Video"""
        encoded_keyword = quote(keyword)
        return f"https://vk.com/video?q={encoded_keyword}"
        
    def search_hotstar(self, keyword):
        """Tìm kiếm video trên Hotstar"""
        encoded_keyword = quote(keyword)
        return f"https://www.hotstar.com/in/search?q={encoded_keyword}"
        
    def search_jiotv(self, keyword):
        """Tìm kiếm video trên JioTV"""
        encoded_keyword = quote(keyword)
        return f"https://www.jiocinema.com/search/{encoded_keyword}"
        
    def search_globoplay(self, keyword):
        """Tìm kiếm video trên Globo Play"""
        encoded_keyword = quote(keyword)
        return f"https://globoplay.globo.com/busca/?q={encoded_keyword}"
        
    def search_dailytube(self, keyword):
        """Tìm kiếm video trên DailyTube"""
        encoded_keyword = quote(keyword)
        return f"https://www.dailytube.io/search?q={encoded_keyword}"
        
    def search_vidio(self, keyword):
        """Tìm kiếm video trên Vidio"""
        encoded_keyword = quote(keyword)
        return f"https://www.vidio.com/search?q={encoded_keyword}"
    
    def search_tudou(self, keyword):
        """Tìm kiếm video trên Tudou"""
        encoded_keyword = quote(keyword)
        return f"https://www.tudou.com/s/{encoded_keyword}"
        
    def search_yylive(self, keyword):
        """Tìm kiếm video trên YY Live"""
        encoded_keyword = quote(keyword)
        return f"https://www.yy.com/search/{encoded_keyword}"
        
    def search_odnoklassniki(self, keyword):
        """Tìm kiếm video trên Odnoklassniki"""
        encoded_keyword = quote(keyword)
        return f"https://ok.ru/video/search?st.query={encoded_keyword}"
        
    def search_abematv(self, keyword):
        """Tìm kiếm video trên Abema TV"""
        encoded_keyword = quote(keyword)
        return f"https://abema.tv/search?q={encoded_keyword}"
        
    def search_tver(self, keyword):
        """Tìm kiếm video trên TVer"""
        encoded_keyword = quote(keyword)
        return f"https://tver.jp/search?q={encoded_keyword}"
        
    def search_gyao(self, keyword):
        """Tìm kiếm video trên GYAO!"""
        encoded_keyword = quote(keyword)
        return f"https://gyao.yahoo.co.jp/search?keyword={encoded_keyword}"
        
    def search_afreecatv(self, keyword):
        """Tìm kiếm video trên Afreeca TV"""
        encoded_keyword = quote(keyword)
        return f"https://www.afreecatv.com/search.html?szSearchType=total&szSearch={encoded_keyword}"
        
    def search_pandoratv(self, keyword):
        """Tìm kiếm video trên Pandora TV"""
        encoded_keyword = quote(keyword)
        return f"https://www.pandora.tv/search?keyword={encoded_keyword}"

    # Các trang video bản địa
    def search_vtvgo(self, keyword):
        """Tìm kiếm video trên VTV Go"""
        encoded_keyword = quote(keyword)
        return f"https://vtvgo.vn/tim-kiem.html?keyword={encoded_keyword}"
        
    def search_sctv(self, keyword):
        """Tìm kiếm video trên SCTV"""
        encoded_keyword = quote(keyword)
        return f"https://sctv.com.vn/tim-kiem.html?keyword={encoded_keyword}"
        
    def search_fptplay(self, keyword):
        """Tìm kiếm video trên FPT Play"""
        encoded_keyword = quote(keyword)
        return f"https://fptplay.vn/tim-kiem/{encoded_keyword}"
        
    def search_vivatv(self, keyword):
        """Tìm kiếm video trên VIVA TV"""
        encoded_keyword = quote(keyword)
        return f"https://vivatv.vn/tim-kiem?q={encoded_keyword}"
        
    def search_htv(self, keyword):
        """Tìm kiếm video trên HTV"""
        encoded_keyword = quote(keyword)
        return f"https://www.htv.com.vn/tim-kiem?q={encoded_keyword}"
        
    def search_keeng(self, keyword):
        """Tìm kiếm video trên Keeng"""
        encoded_keyword = quote(keyword)
        return f"https://keeng.vn/tim-kiem?q={encoded_keyword}"
        
    def search_lienquan(self, keyword):
        """Tìm kiếm video liên quan đến Liên Quân Mobile"""
        encoded_keyword = quote(keyword)
        return f"https://lienquan.garena.vn/tim-kiem?keyword={encoded_keyword}"
        
    def search_mytv(self, keyword):
        """Tìm kiếm video trên MyTV"""
        encoded_keyword = quote(keyword)
        return f"https://www.mytv.com.vn/tim-kiem?q={encoded_keyword}"
        
    def search_vieon(self, keyword):
        """Tìm kiếm video trên VieON"""
        encoded_keyword = quote(keyword)
        return f"https://vieon.vn/tim-kiem?q={encoded_keyword}"
        
    def search_zingtv(self, keyword):
        """Tìm kiếm video trên Zing TV"""
        encoded_keyword = quote(keyword)
        return f"https://tv.zing.vn/tim-kiem?q={encoded_keyword}"
        
    def search_kplus(self, keyword):
        """Tìm kiếm video trên K+"""
        encoded_keyword = quote(keyword)
        return f"https://kplus.vn/tim-kiem?q={encoded_keyword}"
        
    def search_tvb(self, keyword):
        """Tìm kiếm video trên TVB"""
        encoded_keyword = quote(keyword)
        return f"https://www.tvb.com/search?q={encoded_keyword}"
        
    def search_sohu(self, keyword):
        """Tìm kiếm video trên Sohu TV"""
        encoded_keyword = quote(keyword)
        return f"https://tv.sohu.com/s?wd={encoded_keyword}"
        
    def search_abscbn(self, keyword):
        """Tìm kiếm video trên ABS-CBN"""
        encoded_keyword = quote(keyword)
        return f"https://ent.abs-cbn.com/search?q={encoded_keyword}"
        
    def search_bbciplayer(self, keyword):
        """Tìm kiếm video trên BBC iPlayer"""
        encoded_keyword = quote(keyword)
        return f"https://www.bbc.co.uk/iplayer/search?q={encoded_keyword}"
        
    def search_francetv(self, keyword):
        """Tìm kiếm video trên France TV"""
        encoded_keyword = quote(keyword)
        return f"https://www.france.tv/recherche/?q={encoded_keyword}"
        
    def search_ardmediathek(self, keyword):
        """Tìm kiếm video trên ARD Mediathek"""
        encoded_keyword = quote(keyword)
        return f"https://www.ardmediathek.de/suche/{encoded_keyword}"
        
    def search_raiplay(self, keyword):
        """Tìm kiếm video trên RAI Play"""
        encoded_keyword = quote(keyword)
        return f"https://www.raiplay.it/cerca.html?q={encoded_keyword}"
        
    def search_rtveplay(self, keyword):
        """Tìm kiếm video trên RTVE Play"""
        encoded_keyword = quote(keyword)
        return f"https://www.rtve.es/play/buscador/?q={encoded_keyword}"
        
    def search_cbcgem(self, keyword):
        """Tìm kiếm video trên CBC Gem"""
        encoded_keyword = quote(keyword)
        return f"https://gem.cbc.ca/search?q={encoded_keyword}"

class GeminiTranslator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    def translate(self, text, src='vi', dest='zh-cn'):
        # Kiểm tra nếu text rỗng
        if not text or text.strip() == "":
            return ""
            
        # Điều chỉnh prompt dựa trên ngôn ngữ đích
        if dest == 'zh-cn':
            prompt = f"Dịch câu sau từ tiếng Việt sang tiếng Trung giản thể (chỉ trả về bản dịch, không giải thích): {text}"
        elif dest == 'en':
            prompt = f"Dịch câu sau từ tiếng Việt sang tiếng Anh (chỉ trả về bản dịch, không giải thích): {text}"
        elif dest == 'ja':
            prompt = f"Dịch câu sau từ tiếng Việt sang tiếng Nhật (chỉ trả về bản dịch, không giải thích): {text}"
        else:
            prompt = f"Dịch câu sau từ tiếng Việt sang {dest} (chỉ trả về bản dịch, không giải thích): {text}"
        
        try:
            response = requests.post(
                f"{self.url}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                json={
                    "contents": [{
                        "parts":[{"text": prompt}]
                    }]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    translated_text = result['candidates'][0]['content']['parts'][0]['text']
                    # Loại bỏ các ký tự không cần thiết và khoảng trắng
                    translated_text = translated_text.strip().strip('"').strip("'")
                    return translated_text
            return None
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return None

class VideoSplitter:
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mkv', '.mov']
        
    def split_video(self, input_file, segment_length):
        try:
            import cv2
            import subprocess
            from datetime import timedelta
            
            # Kiểm tra định dạng file
            if not any(input_file.lower().endswith(fmt) for fmt in self.supported_formats):
                return False, "Định dạng file không được hỗ trợ", None
            
            # Đọc video để lấy thông tin
            cap = cv2.VideoCapture(input_file)
            if not cap.isOpened():
                return False, "Không thể mở file video", None
                
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps
            cap.release()
            
            # Tính số phần cần chia
            segment_length_seconds = segment_length * 60
            num_segments = int(duration / segment_length_seconds) + (1 if duration % segment_length_seconds != 0 else 0)
            
            # Tạo thư mục tạm
            temp_dir = os.path.join(os.getcwd(), "temp_segments")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Danh sách lưu các file đã chia
            split_files = []
            
            # Chia video với tùy chọn tối ưu
            for i in range(num_segments):
                start_time = i * segment_length_seconds
                duration_time = min(segment_length_seconds, duration - start_time)
                
                output_path = os.path.join(temp_dir, f"part_{i+1}.mp4")
                
                # Thêm tùy chọn để sử dụng ít bộ nhớ hơn
                command = [
                    'ffmpeg',
                    '-ss', str(timedelta(seconds=start_time)),
                    '-i', input_file,
                    '-t', str(timedelta(seconds=duration_time)),
                    '-c:v', 'libx264',  # Fast encoding for video
                    '-preset', 'ultrafast',  # Fastest preset
                    '-c:a', 'aac',  # Fast encoding for audio
                    '-b:a', '128k',  # Lower audio bitrate
                    '-avoid_negative_ts', '1',
                    '-y',
                    output_path
                ]
                
                st.text(f"Đang xử lý phần {i+1}/{num_segments}...")
                
                try:
                    process = subprocess.run(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=600  # Tăng timeout lên 10 phút mỗi phần
                    )
                    
                    if process.returncode != 0:
                        # Xóa các file tạm đã tạo
                        for file in os.listdir(temp_dir):
                            os.remove(os.path.join(temp_dir, file))
                        os.rmdir(temp_dir)
                        return False, f"Lỗi khi xử lý phần {i+1}: {process.stderr.decode()}", None
                        
                    # Đọc file đã tạo vào bộ nhớ
                    with open(output_path, 'rb') as f:
                        split_files.append({
                            'name': f"part_{i+1}.mp4",
                            'data': f.read()
                        })
                    
                    # Xóa file phần để giải phóng dung lượng
                    os.remove(output_path)
                    
                except subprocess.TimeoutExpired:
                    # Xóa các file tạm
                    for file in os.listdir(temp_dir):
                        os.remove(os.path.join(temp_dir, file))
                    os.rmdir(temp_dir)
                    return False, f"Quá thời gian xử lý phần {i+1}, vui lòng thử lại", None
                
                # Cập nhật tiến trình
                st.progress((i+1)/num_segments)
            
            # Xóa thư mục tạm khi hoàn thành
            os.rmdir(temp_dir)
            return True, f"Đã chia thành {num_segments} phần", split_files
            
        except Exception as e:
            # Đảm bảo dọn dẹp nếu có lỗi
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, file))
                os.rmdir(temp_dir)
            return False, f"Lỗi khi chia video: {str(e)}", None

def check_ffmpeg_installed():
    """Kiểm tra FFmpeg đã được cài đặt chưa"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        return result.returncode == 0
    except:
        return False

def main():
    # Cấu hình trang
    st.set_page_config(
        page_title="Video Tools - Tìm kiếm & Xử lý Video",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Thêm CSS tùy chỉnh cho các nút nền tảng
    st.markdown("""
    <style>
    .horizontal-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
    }
    .platform-button {
        padding: 10px 15px;
        border-radius: 8px;
        color: white;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s;
        display: inline-flex;
        align-items: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .platform-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar cho công cụ
    with st.sidebar:
        st.title("🛠️ Công cụ Video")
        
        # Tạo tabs cho các công cụ khác nhau
        tool_tab = st.radio(
            "Chọn công cụ:",
            ["🔍 Tìm kiếm video"],
            index=0  # Mặc định chọn công cụ chia video
        )
        
        # Thêm phần lịch sử tìm kiếm
        if tool_tab == "🔍 Tìm kiếm video":
            st.markdown("---")
            st.subheader("📜 Lịch sử tìm kiếm")
            
            # Khởi tạo lịch sử tìm kiếm trong session state nếu chưa có
            if 'search_history' not in st.session_state:
                st.session_state.search_history = []
                
            # Hiển thị lịch sử tìm kiếm
            if st.session_state.search_history:
                for i, item in enumerate(st.session_state.search_history[-5:]):  # Chỉ hiển thị 5 mục gần nhất
                    if st.button(f"{item}", key=f"history_{i}"):
                        # Điền từ khóa vào ô tìm kiếm
                        st.session_state.search_input = item
                        st.experimental_rerun()
            else:
                st.caption("Chưa có lịch sử tìm kiếm")

    # Nội dung chính
    if tool_tab == "✂️ Chia nhỏ video":
        st.header("✂️ Chia nhỏ video")
        st.markdown("---")
        
        # Kiểm tra FFmpeg
        if not check_ffmpeg_installed():
            st.error("❌ FFmpeg chưa được cài đặt. Vui lòng liên hệ quản trị viên.")
            st.stop()
        
        # Tạo 2 cột cho phần upload và cấu hình
        col1, col2 = st.columns([2, 1])
        
        with col1:
            upload_option = st.radio(
                "Chọn cách tải video:",
                ["Tải lên từ máy tính", "Nhập URL video"]
            )

        if upload_option == "Tải lên từ máy tính":
            uploaded_file = st.file_uploader(
                "Tải lên video cần chia:",
                type=['mp4', 'avi', 'mkv', 'mov'],
                help="Hỗ trợ định dạng: MP4, AVI, MKV, MOV"
            )
            file_input = uploaded_file
        else:
            video_url = st.text_input(
                "Nhập URL video:",
                placeholder="https://example.com/video.mp4"
            )
            
            if video_url and st.button("Tải video từ URL"):
                with st.spinner("Đang tải video từ URL..."):
                    try:
                        # Tạo thư mục tạm
                        temp_dir = os.path.join(os.getcwd(), "temp")
                        os.makedirs(temp_dir, exist_ok=True)
                        temp_path = os.path.join(temp_dir, "downloaded_video.mp4")
                        
                        # Tải video từ URL
                        urllib.request.urlretrieve(video_url, temp_path)
                        
                        st.success("✅ Đã tải video thành công!")
                        file_input = temp_path
                    except Exception as e:
                        st.error(f"❌ Lỗi khi tải video: {str(e)}")
                        file_input = None
            else:
                file_input = None
        
        with col2:
            segment_length = st.number_input(
                "Độ dài mỗi phần (phút):",
                min_value=1,
                value=5,
                help="Mỗi phần video sẽ có độ dài bằng nhau"
            )
        
        if file_input is not None:
            # Kiểm tra kích thước file
            file_size_mb = file_input.size / (1024 * 1024)
            if file_size_mb > 1000:  # Nếu lớn hơn 1GB
                st.warning(f"⚠️ File có kích thước lớn ({file_size_mb:.1f}MB). Quá trình xử lý có thể mất nhiều thời gian.")
            
            try:
                # Tiếp tục với quá trình xử lý
                splitter = VideoSplitter()
                success, message, split_files = splitter.split_video(file_input, segment_length)
                
                if success and split_files:
                    # Tạo container hiển thị kết quả
                    result_container = st.container()
                    with result_container:
                        st.success("✅ " + message)
                        
                        # Hiển thị thông tin các phần
                        with st.expander("Danh sách các phần đã chia", expanded=True):
                            for i, file in enumerate(split_files, 1):
                                st.text(f"Phần {i}: {file['name']}")
                        
                        # Tạo ZIP và nút tải xuống
                        st.markdown("---")
                        with st.container():
                            zip_buffer = io.BytesIO()
                            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_STORED) as zip_file:
                                for file in split_files:
                                    zip_file.writestr(file['name'], file['data'])
                            
                            original_name = os.path.splitext(file_input.name)[0]
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col2:
                                st.download_button(
                                    label="📥 TẢI XUỐNG TẤT CẢ CÁC PHẦN",
                                    data=zip_buffer.getvalue(),
                                    file_name=f"{original_name}_split.zip",
                                    mime="application/zip",
                                    use_container_width=True
                                )
                else:
                    st.error("❌ " + message)
                    
            except Exception as e:
                st.error(f"❌ Lỗi khi xử lý file: {str(e)}")

    else:  # Phần tìm kiếm video
        st.header("🔍 Tìm kiếm video toàn cầu")
        st.markdown("---")
        
        # Khởi tạo các đối tượng
        downloader = VideoDownloader()
        
        # Kiểm tra API key trước khi khởi tạo
        api_key = "AIzaSyBIYdOa-hcuktO4mxra9XnHKF-pd154nkw"
        translator = GeminiTranslator(api_key=api_key)
        
        # Form tìm kiếm
        with st.form(key='search_form'):
            # Phần cấu hình tìm kiếm
            selected_platforms = st.multiselect(
                "Chọn nền tảng tìm kiếm:",
                list(downloader.platforms.keys()),
                default=["Douyin", "Vimeo", "Dailymotion", "xigua", "Bilibili", "Niconico", "YouTube"]
            )
            
            # Thêm danh sách các ngôn ngữ hỗ trợ để dịch
            available_languages = {
                'en': 'Tiếng Anh',
                'zh-cn': 'Tiếng Trung',
                'ja': 'Tiếng Nhật',
                'ko': 'Tiếng Hàn',
                'fr': 'Tiếng Pháp',
                'de': 'Tiếng Đức',
                'es': 'Tiếng Tây Ban Nha',
                'ru': 'Tiếng Nga'
            }
            
            # Cho phép người dùng chọn ngôn ngữ muốn dịch
            selected_languages = st.multiselect(
                "Chọn ngôn ngữ muốn dịch sang:",
                options=list(available_languages.keys()),
                default=['en', 'zh-cn', 'ja'],
                format_func=lambda x: available_languages[x]
            )
            
            # Tạo layout 2 cột cho input và nút tìm kiếm
            col1, col2 = st.columns([4, 1])  # Tỷ lệ 4:1 giữa input và nút
            
            with col1:
                keyword = st.text_input(
                    "Nhập từ khóa tìm kiếm bằng tiếng Việt:",
                    placeholder="Ví dụ: nhạc trẻ, phim hành động...",
                    key="search_input"
                )
            
            with col2:
                search_button = st.form_submit_button(
                    "🔎 Tìm kiếm",
                    use_container_width=True,
                    type="primary"
                )

        if search_button and keyword:
            try:
                with st.spinner('Đang dịch từ khóa...'):
                    # Dịch từ khóa sang các ngôn ngữ được chọn
                    translated_keywords = {}
                    
                    for lang_code in selected_languages:
                        translated_keywords[lang_code] = translator.translate(keyword, src='vi', dest=lang_code) or keyword
                    
                    # Đảm bảo các ngôn ngữ cơ bản luôn có sẵn để sử dụng nếu cần
                    if 'en' not in translated_keywords:
                        translated_keywords['en'] = keyword
                    if 'zh-cn' not in translated_keywords:
                        translated_keywords['zh-cn'] = keyword
                    if 'ja' not in translated_keywords:
                        translated_keywords['ja'] = keyword
                    
                    # Kiểm tra nếu dịch thất bại
                    if any(not val for val in translated_keywords.values()):
                        st.warning("⚠️ Một số bản dịch có thể không hoàn chỉnh. Kết quả tìm kiếm có thể bị ảnh hưởng.")
                    
                    # Hiển thị bản dịch
                    if selected_languages:
                        with st.expander("🔄 Xem các bản dịch", expanded=False):
                            st.write("Từ khóa gốc (Tiếng Việt):", keyword)
                            for lang_code in selected_languages:
                                st.write(f"{available_languages[lang_code]}:", translated_keywords[lang_code])

                # Lưu từ khóa vào lịch sử tìm kiếm
                if keyword not in st.session_state.search_history:
                    st.session_state.search_history.append(keyword)
                    # Giới hạn lịch sử tìm kiếm tối đa 10 mục
                    if len(st.session_state.search_history) > 10:
                        st.session_state.search_history.pop(0)

                # Hiển thị kết quả tìm kiếm
                st.markdown("### 🔍 Kết quả tìm kiếm:")
                
                # Container cho các nút
                buttons_html = '<div class="horizontal-container">'
                for platform in selected_platforms:
                    config = downloader.platforms[platform]
                    # Chọn ngôn ngữ phù hợp cho từng nền tảng
                    if platform in ["Bilibili", "Douyin", "TikTok"]:
                        search_keyword = translated_keywords.get('zh-cn', keyword)
                    elif platform in ["Niconico"]:
                        search_keyword = translated_keywords.get('ja', keyword)
                    else:
                        search_keyword = translated_keywords.get('en', keyword)
                        
                    search_url = config["func"](search_keyword)
                    buttons_html += f'<a href="{search_url}" target="_blank" class="platform-button" style="background-color: {config["color"]}">{config["icon"]} {platform}</a>'
                buttons_html += '</div>'
                
                # Render kết quả
                st.markdown(buttons_html, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Có lỗi xảy ra: {str(e)}")

        # Thông tin nền tảng
        with st.expander("ℹ️ Thông tin các nền tảng", expanded=False):
            st.markdown("""
            ### Các nền tảng video Trung Quốc
            - **Douyin**: Nền tảng video ngắn phổ biến nhất TQ
            - **Xigua**: Video dài, nội dung chất lượng cao
            - **Bilibili**: Video anime, game, giải trí
            - **Youku**: Phim, TV shows, video dài
            - **WeTV**: Nền tảng video phim của Tencent
            - **iQIYI**: Nền tảng phim và video giải trí lớn
            - **TudouVideo**: Nền tảng chia sẻ video phổ biến
            - **YY Live**: Nền tảng livestream và video
            - **Sohu TV**: Cổng thông tin video và giải trí
            
            ### Các nền tảng video Hàn Quốc
            - **Naver TV**: Nền tảng video của Naver
            - **Kakao TV**: Nền tảng video của Kakao
            - **Afreeca TV**: Nền tảng livestream và video
            - **Pandora TV**: Nền tảng chia sẻ video phổ biến
            
            ### Các nền tảng video Nhật Bản
            - **Niconico**: Nền tảng chia sẻ video và livestream
            - **Abema TV**: Dịch vụ phát sóng TV trực tuyến
            - **TVer**: Nền tảng xem lại chương trình TV
            - **GYAO!**: Dịch vụ xem video miễn phí của Yahoo Japan
            
            ### Các nền tảng video Việt Nam
            - **VTV Go**: Nền tảng của Đài truyền hình Việt Nam
            - **SCTV**: Truyền hình cáp Saigontourist
            - **FPT Play**: Dịch vụ xem phim và TV của FPT
            - **VIVA TV**: Nền tảng video giải trí
            - **HTV**: Đài truyền hình TP.HCM
            - **Keeng**: Dịch vụ nhạc và video của MobiFone
            - **MyTV**: Dịch vụ truyền hình của VNPT
            - **VieON**: Nền tảng video giải trí của Galaxy
            - **Zing TV**: Nền tảng video của VNG
            - **K+**: Dịch vụ truyền hình trả tiền
            
            ### Các nền tảng video toàn cầu
            - **YouTube**: Nền tảng video lớn nhất thế giới
            - **Vimeo**: Video chất lượng cao, nghệ thuật
            - **Dailymotion**: Nền tảng chia sẻ video lớn
            - **Twitch**: Nền tảng phát trực tiếp game
            - **Facebook**: Mạng xã hội với tính năng video
            - **Instagram**: Chia sẻ ảnh và video ngắn
            - **TikTok**: Video ngắn và xu hướng
            """)

if __name__ == "__main__":
    main()
