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
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    def translate(self, text, src='vi', dest='zh-cn'):
        # Kiểm tra nếu text rỗng
        if not text or text.strip() == "":
            return ""
            
        # Kiểm tra nếu không có API key
        if not self.api_key:
            return None
            
        # Điều chỉnh prompt dựa trên ngôn ngữ đích
        if dest == 'zh-cn':
            prompt = f"Dịch câu sau từ tiếng Việt sang tiếng Trung giản thể (chỉ trả về bản dịch, không giải thích): {text}"
        elif dest == 'en':
            prompt = f"Dịch câu sau từ tiếng Việt sang tiếng Anh (chỉ trả về bản dịch, không giải thích): {text}"
        elif dest == 'kr':
            prompt = f"Dịch câu sau từ tiếng Việt sang tiếng Hàn (chỉ trả về bản dịch, không giải thích): {text}"
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
            import numpy as np
            from datetime import timedelta
            import subprocess
            import tempfile
            
            # Kiểm tra định dạng file
            if not any(input_file.lower().endswith(fmt) for fmt in self.supported_formats):
                return False, "Định dạng file không được hỗ trợ", None
            
            # Tạo thư mục tạm để lưu các phần video
            with tempfile.TemporaryDirectory() as temp_dir:
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
                
                # Danh sách lưu các file đã chia
                split_files = []
                
                # Chia video
                for i in range(num_segments):
                    start_time = i * segment_length_seconds
                    duration_time = min(segment_length_seconds, duration - start_time)
                    
                    output_path = os.path.join(temp_dir, f"part_{i+1}.mp4")
                    
                    command = [
                        'ffmpeg',
                        '-ss', str(timedelta(seconds=start_time)),
                        '-i', input_file,
                        '-t', str(timedelta(seconds=duration_time)),
                        '-c', 'copy',
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
                            timeout=300
                        )
                        
                        if process.returncode != 0:
                            return False, f"Lỗi khi xử lý phần {i+1}: {process.stderr.decode()}", None
                            
                        # Đọc file đã tạo vào bộ nhớ
                        with open(output_path, 'rb') as f:
                            split_files.append({
                                'name': f"part_{i+1}.mp4",
                                'data': f.read()
                            })
                            
                    except subprocess.TimeoutExpired:
                        return False, f"Quá thời gian xử lý phần {i+1}, vui lòng thử lại", None
                    
                    time.sleep(0.5)
                
                return True, f"Đã chia thành {num_segments} phần", split_files
            
        except Exception as e:
            return False, f"Lỗi khi chia video: {str(e)}", None

def main():
    # Điều chỉnh cấu hình trang để tối ưu không gian
    st.set_page_config(
        page_title="Video Tools - Tìm kiếm & Xử lý Video",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Xử lý callback từ SePay sau khi thanh toán và auth_token từ app desktop
    try:
        # Kiểm tra query parameters từ URL
        query_params = st.query_params
        payment_success = query_params.get('payment_success', [None])[0] if isinstance(query_params.get('payment_success'), list) else query_params.get('payment_success')
        payment_error = query_params.get('payment_error', [None])[0] if isinstance(query_params.get('payment_error'), list) else query_params.get('payment_error')
        payment_cancel = query_params.get('payment_cancel', [None])[0] if isinstance(query_params.get('payment_cancel'), list) else query_params.get('payment_cancel')
        payment_id = query_params.get('payment_id', [None])[0] if isinstance(query_params.get('payment_id'), list) else query_params.get('payment_id')
        auth_token = query_params.get('auth_token', [None])[0] if isinstance(query_params.get('auth_token'), list) else query_params.get('auth_token')
        tab = query_params.get('tab', [None])[0] if isinstance(query_params.get('tab'), list) else query_params.get('tab')
    except:
        payment_success = None
        payment_error = None
        payment_cancel = None
        payment_id = None
        auth_token = None
        tab = None
    
    # Nếu có auth_token và tab=payment, tự động chuyển đến tab thanh toán và tạo payment
    if auth_token and tab == 'payment' and 'payment_created' not in st.session_state:
        st.session_state.auth_token_from_desktop = auth_token
        st.session_state.auto_create_payment = True
        st.session_state.payment_created = False
    
    if payment_success and payment_id:
        st.success("✅ Thanh toán thành công!")
        st.balloons()
        
        API_BASE_URL = os.getenv('API_BASE_URL', 'https://web-admin-srt212.onrender.com')
        
        # Kiểm tra trạng thái thanh toán
        with st.spinner("Đang kiểm tra trạng thái thanh toán..."):
            try:
                check_response = requests.get(
                    f"{API_BASE_URL}/api/check_payment/{payment_id}",
                    timeout=10
                )
                if check_response.status_code == 200:
                    payment_status = check_response.json()
                    if payment_status.get('status') == 'completed':
                        st.success("🎉 Tài khoản của bạn đã được nâng cấp Pro thành công!")
                        
                        # Hiển thị thông tin
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"**Payment ID:** {payment_id}")
                            st.info(f"**Trạng thái:** {payment_status.get('status', 'N/A')}")
                        with col2:
                            if payment_status.get('completed_at'):
                                st.info(f"**Hoàn tất lúc:** {payment_status.get('completed_at')}")
                        
                        # Hướng dẫn cập nhật app desktop
                        st.markdown("---")
                        st.markdown("### 📱 Cập nhật thông tin trên App Desktop")
                        st.warning("""
                        **Quan trọng:** Để sử dụng tính năng Pro, bạn cần cập nhật thông tin trên ứng dụng desktop:
                        
                        1. Mở ứng dụng desktop của bạn
                        2. Nhấn nút "Kiểm tra thanh toán" hoặc "Làm mới tài khoản"
                        3. Ứng dụng sẽ tự động cập nhật thông tin Pro từ server
                        """)
                        
                        # Hiển thị auth_token để người dùng có thể copy
                        if auth_token:
                            st.markdown("---")
                            st.markdown("### 🔑 Thông tin xác thực")
                            st.code(auth_token, language=None)
                            st.caption("Lưu ý: Auth token này đã được sử dụng để tạo thanh toán. Bạn không cần nhập lại.")
                    else:
                        st.warning(f"⏳ Đơn thanh toán đang chờ xử lý. Trạng thái: {payment_status.get('status', 'unknown')}")
                        st.info("Vui lòng đợi vài phút, sau đó kiểm tra lại trong ứng dụng desktop.")
            except Exception as e:
                st.error(f"❌ Lỗi khi kiểm tra trạng thái: {str(e)}")
                st.info("Vui lòng kiểm tra trạng thái thanh toán trong ứng dụng desktop.")
        
        return
    
    if payment_error and payment_id:
        st.error("❌ Thanh toán thất bại!")
        st.info("Vui lòng thử lại hoặc liên hệ hỗ trợ nếu vấn đề vẫn tiếp tục.")
        return
    
    if payment_cancel and payment_id:
        st.warning("⚠️ Bạn đã hủy thanh toán.")
        st.info("Bạn có thể tạo đơn thanh toán mới bất cứ lúc nào.")
        return

    # Thêm CSS để tối ưu không gian hiển thị
    st.markdown("""
    <style>
    /* Giảm padding của sidebar */
    .css-1d391kg, .css-1lcbmhc {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Giảm kích thước tiêu đề */
    .sidebar .block-container h1 {
        font-size: 1.5rem;
        margin-top: 0;
        margin-bottom: 0.5rem;
    }

    /* Giảm khoảng cách giữa các phần tử */
    .sidebar .block-container > div {
        margin-bottom: 0.5rem;
    }

    /* Giảm kích thước của các nút radio */
    .stRadio > div {
        margin-bottom: 0.2rem;
    }

    /* Giảm kích thước của các nút trong lịch sử tìm kiếm */
    .sidebar .stButton button {
        padding: 0.2rem 0.5rem;
        font-size: 0.8rem;
        min-height: 0;
    }

    /* Giảm kích thước của subheader */
    .sidebar .block-container h3 {
        font-size: 1rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Tùy chỉnh cho các nút nền tảng */
    .horizontal-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 15px;
    }
    .platform-button {
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    .platform-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }

    /* Tùy chỉnh cho thông báo */
    .notification-box {
        background-color: #f8f9fa;
        border-left: 3px solid #ff9800;
        padding: 10px;
        margin-bottom: 15px;
        border-radius: 3px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        font-size: 0.8em;
    }
    .download-button {
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        border-radius: 3px;
        margin-top: 5px;
        font-size: 0.8em;
    }
    .download-button:hover {
        background-color: #45a049;
    }

    /* Tùy chỉnh cho nút tải ứng dụng */
    .app-download-box {
        background-color: #e8f5e9;
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .app-download-box h3 {
        color: #2e7d32;
        font-size: 1rem;
        margin-top: 0;
        margin-bottom: 5px;
    }
    .app-download-box p {
        font-size: 0.8rem;
        margin-bottom: 5px;
    }
    .app-download-button {
        display: inline-block;
        background-color: #2e7d32;
        color: white;
        padding: 5px 10px;
        text-decoration: none;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    /* API key input container */
    .api-key-container {
        background-color: #f3f4f6;
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 10px;
        border-left: 3px solid #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar cho công cụ
    with st.sidebar:
        st.title("🛠️ Công cụ Video - Liên Hệ Zalo : 0986234983")
        
        # Tạo tabs cho các công cụ khác nhau
        # Nếu có auth_token từ desktop, mặc định chọn tab thanh toán
        default_index = 3 if (auth_token and tab == 'payment') else 0
        tool_tab = st.radio(
            "Chọn công cụ:",
            ["🔍 Tìm kiếm video", "✂️ Chia nhỏ video", "🔊 Lồng tiếng video", "💳 Thanh toán"],
            index=default_index  # Mặc định chọn tab thanh toán nếu có auth_token
        )
        
        # Hiển thị box tải ứng dụng tương ứng với công cụ đã chọn
        if tool_tab == "✂️ Chia nhỏ video":
            st.markdown("""
            <div class="app-download-box">
                <h3>📥 Ứng dụng Chia Nhỏ Video</h3>
                <p>Tải về phiên bản desktop để chia nhỏ video mà không cần kết nối internet.</p>
                <a href="https://up-4.net/d/xbq1" target="_blank" class="app-download-button">Tải về ngay</a>
            </div>
            """, unsafe_allow_html=True)
        elif tool_tab == "🔊 Lồng tiếng video":
            st.markdown("""
            <div class="app-download-box">
                <h3>📥 Ứng dụng Lồng Tiếng Đa Ngôn Ngữ v10.0</h3>
                <p>Tải về phiên bản desktop để lồng tiếng đa ngôn ngữ cho tất cả các video trên thế giới.</p>
                <p>Phần mềm AI tự động lồng tiếng video miễn phí</p>
                <a href='https://up-4.net/d/ymIO' target=_blank> tải v6.9</a>
                <p>thư viện</p>
                <a href="https://up-4.net/d/yQ3c">Tải thêm thư viên small v0.1</a>
            </div>
            """, unsafe_allow_html=True)
        
        # Thêm phần lịch sử tìm kiếm chỉ khi đang ở tab tìm kiếm video
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
            
            # Thêm thông báo nhắc nhở ở dưới lịch sử tìm kiếm
            st.markdown("---")
            st.markdown("""
            <div class="notification-box">
                <div style="text-align: center; margin-bottom: 5px;">
                    <a href="https://coccoc.com/download" target="_blank" class="download-button">Tải Cốc Cốc</a>
                    <a href="https://www.internetdownloadmanager.com/download.html" target="_blank" class="download-button" style="margin-left: 5px;">Tải IDM</a>
                </div>
                <h4 style="margin-top: 5px; font-size: 0.9em;">⚠️ Lưu ý quan trọng</h4>
                <p style="margin: 3px 0; font-size: 0.8em;">Để tải video tốt nhất, bạn nên:</p>
                <ul style="margin: 3px 0; padding-left: 15px; font-size: 0.8em;">
                    <li>Sử dụng <strong>Cốc Cốc</strong> để tải video từ nhiều nền tảng</li>
                    <li>Cài đặt <strong>IDM</strong> để tăng tốc độ tải xuống</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # Nội dung chính
    if tool_tab == "✂️ Chia nhỏ video":
        st.header("✂️ Chia nhỏ video")
        st.markdown("---")
        
        st.info("Vui lòng tải về ứng dụng Chia Nhỏ Video từ thanh bên để sử dụng tính năng này.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### ✨ Tính năng nổi bật:
            - ⚡ Xử lý nhanh không phụ thuộc Internet
            - 🎯 Chia video theo độ dài cụ thể
            - 🎬 Giữ nguyên chất lượng video gốc
            - 📱 Hỗ trợ xuất video cho điện thoại
            - 🔄 Tự động tạo thư mục chứa các video đã chia
            - 🎞️ Hỗ trợ nhiều định dạng video phổ biến
            """)
        
        with col2:
            st.markdown("""
            ### 📝 Hướng dẫn sử dụng:
            1. Tải và cài đặt ứng dụng Chia Nhỏ Video
            2. Mở ứng dụng và chọn video cần chia
            3. Đặt độ dài cho mỗi phần (phút)
            4. Chọn thư mục lưu các phần video
            5. Nhấn nút "Bắt đầu chia" và đợi xử lý
            """)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center">
            <p style="color: #777; font-size: 0.9em;">Ứng dụng Chia Nhỏ Video cho phép bạn chia các file video lớn thành các phần nhỏ hơn mà không làm giảm chất lượng. Đặc biệt hữu ích khi cần chia sẻ video trên các nền tảng có giới hạn kích thước file.</p>
        </div>
        """, unsafe_allow_html=True)

    elif tool_tab == "🔊 Lồng tiếng video":
        st.header("🔊 Lồng tiếng video đa ngôn ngữ")
        st.markdown("---")
        
        st.info("Vui lòng tải về ứng dụng Lồng Tiếng Đa Ngôn Ngữ v10.0 từ thanh bên để sử dụng tính năng này.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### ✨ Tính năng nổi bật:
            - 🌐 Hỗ trợ hơn 40 ngôn ngữ
            - 🎵 Công nghệ AI tách âm thanh thành văn bản
            - 🎤 Sử dụng giọng đọc miễn phí và thêm giọng đọc theo yêu cầu
            - 🔄 Tự động tạo lồng tiếng mà không cần phụ đề
            - 🔊 Có thể thay đổi logo và nhạc nền theo yêu cầu
            - 💡 Thông minh nhận diện ngôn ngữ gốc
            - 🎞️ Hỗ trợ nhiều định dạng video phổ biến
            """)
        
        with col2:
            st.markdown("""
            ### 📝 Hướng dẫn sử dụng:
            1. Tải và cài đặt ứng dụng
            2. Chọn video cần lồng tiếng (video dưới 5 phút tránh bị request hệ thống do miễn phí api)
            3. Chọn ngôn ngữ nguồn và đích
            4. Chọn chế độ dịch
            5. Đổi API key sau mỗi lần dịch tránh request
            6. Thay đổi nhạc và logo thương hiệu nếu muốn
            7. Chọn giữ lại âm thanh gốc nếu muốn(gợi ý đặt 5,6)
            8. Chọn " Bắt đầu xử lý" và đợi kết quả
            """)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center">
            <p style="color: #777; font-size: 0.9em;">Phiên bản v10.0 mới nhất với nhiều cải tiến quan trọng về chất lượng giọng nói và tính chính xác trong việc đồng bộ môi. Sử dụng mô hình AI tiên tiến để tạo ra giọng nói tự nhiên nhất.</p>
        </div>
        """, unsafe_allow_html=True)

    elif tool_tab == "💳 Thanh toán":
        st.header("💳 Nâng Cấp Tài Khoản Pro")
        st.markdown("---")
        
        # Cấu hình API URL
        API_BASE_URL = os.getenv('API_BASE_URL', 'https://web-admin-srt212.onrender.com')
        
        # Form thanh toán
        with st.form("payment_form"):
            st.markdown("### Thông tin thanh toán")
            
            # Nếu có auth_token từ URL (từ app desktop), sử dụng nó
            if auth_token:
                st.info(f"✅ Đã nhận auth_token từ ứng dụng desktop")
                auth_token_input = st.text_input(
                    "Auth Token:",
                    value=auth_token,
                    type="password",
                    help="Auth token từ ứng dụng desktop",
                    disabled=True
                )
                auth_token_value = auth_token
            else:
                auth_token_input = st.text_input(
                    "Auth Token:",
                    type="password",
                    help="Nhập auth_token từ ứng dụng desktop của bạn"
                )
                auth_token_value = auth_token_input
            
            col1, col2 = st.columns(2)
            with col1:
                amount = st.number_input(
                    "Số tiền (VND):",
                    min_value=99000,
                    value=99000,
                    step=99000,
                    help="Số tiền tối thiểu: 99.000 VND"
                )
            with col2:
                st.markdown("### Gói dịch vụ")
                if amount == 99000:
                    st.info("**1 tháng Pro**\n\n- Xử lý video không giới hạn\n- Hỗ trợ đa ngôn ngữ")
                elif amount == 198000:
                    st.info("**2 tháng Pro**\n\n- Xử lý video không giới hạn\n- Hỗ trợ đa ngôn ngữ")
                elif amount == 297000:
                    st.info("**3 tháng Pro**\n\n- Xử lý video không giới hạn\n- Hỗ trợ đa ngôn ngữ")
                elif amount >= 449000:
                    st.info("**6 tháng Pro**\n\n- Xử lý video không giới hạn\n- Hỗ trợ đa ngôn ngữ")
                elif amount >= 799000:
                    st.info("**12 tháng Pro**\n\n- Xử lý video không giới hạn\n- Hỗ trợ đa ngôn ngữ")
            
            submit_button = st.form_submit_button("💳 Thanh Toán", use_container_width=True)
            
            # Tự động tạo payment nếu có auth_token từ desktop và chưa tạo
            auto_create = (auth_token and tab == 'payment' and 
                         'payment_created' not in st.session_state)
            
            if submit_button or auto_create:
                if not auth_token_value:
                    st.error("⚠️ Vui lòng nhập Auth Token!")
                else:
                    with st.spinner("Đang tạo đơn thanh toán..."):
                        try:
                            # Gọi API tạo payment
                            response = requests.post(
                                f"{API_BASE_URL}/api/create_payment",
                                json={
                                    "auth_token": auth_token_value,
                                    "amount": amount
                                },
                                timeout=30
                            )
                            
                            if response.status_code == 200:
                                data = response.json()
                                if data.get('success'):
                                    # Lưu thông tin vào session
                                    st.session_state.payment_data = data
                                    st.session_state.checkout_data = data.get('checkout_data')
                                    st.session_state.checkout_url = data.get('checkout_url')
                                    st.session_state.payment_id = data.get('payment_id')
                                    st.session_state.payment_created = True
                                    
                                    st.success("✅ Đơn thanh toán đã được tạo thành công!")
                                    st.info("📋 Vui lòng hoàn tất thanh toán bằng cách nhấn nút bên dưới")
                                    
                                    # Tự động redirect đến SePay nếu từ app desktop
                                    if auto_create:
                                        st.markdown(f'<meta http-equiv="refresh" content="2;url={st.session_state.checkout_url}">', unsafe_allow_html=True)
                                        st.info("🔄 Đang chuyển đến trang thanh toán SePay...")
                                else:
                                    st.error(f"❌ Lỗi: {data.get('message', 'Không thể tạo đơn thanh toán')}")
                            else:
                                error_data = response.json() if response.content else {}
                                st.error(f"❌ Lỗi: {error_data.get('message', 'Không thể kết nối đến server')}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ Lỗi kết nối: {str(e)}")
                        except Exception as e:
                            st.error(f"❌ Lỗi: {str(e)}")
        
        # Hiển thị nút thanh toán nếu đã tạo payment
        if 'checkout_url' in st.session_state and st.session_state.checkout_url:
            st.markdown("---")
            st.markdown("### 📋 Thông tin đơn hàng")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Payment ID:** {st.session_state.payment_id}")
                st.info(f"**Số tiền:** {amount:,} VND")
            with col2:
                st.info(f"**Trạng thái:** Chờ thanh toán")
            
            # Tạo form HTML để submit đến SePay
            checkout_data = st.session_state.checkout_data
            if checkout_data:
                form_html = f'''
                <form id="sepay-form" action="{st.session_state.checkout_url}" method="POST">
                '''
                for key, value in checkout_data.items():
                    form_html += f'<input type="hidden" name="{key}" value="{value}">'
                form_html += '''
                </form>
                <script>
                    document.getElementById("sepay-form").submit();
                </script>
                '''
                st.markdown(form_html, unsafe_allow_html=True)
                
                # Nút submit thủ công (backup)
                st.markdown("---")
                if st.button("🚀 Thanh Toán Ngay", use_container_width=True, type="primary"):
                    st.markdown(form_html, unsafe_allow_html=True)
        
        # Hiển thị thông báo từ callback
        if payment_success:
            payment_id = query_params.get('payment_id', [None])[0] if isinstance(query_params.get('payment_id'), list) else query_params.get('payment_id')
            auth_token_callback = query_params.get('auth_token', [None])[0] if isinstance(query_params.get('auth_token'), list) else query_params.get('auth_token')
            
            st.success(f"✅ Thanh toán thành công cho đơn hàng {payment_id}!")
            st.info("📱 Vui lòng kiểm tra ứng dụng desktop để cập nhật thông tin Pro.")
            
            # Hiển thị thông tin payment
            if payment_id:
                try:
                    check_response = requests.get(
                        f"{API_BASE_URL}/api/check_payment/{payment_id}",
                        timeout=10
                    )
                    if check_response.status_code == 200:
                        payment_status = check_response.json()
                        if payment_status.get('status') == 'completed':
                            st.success("🎉 Tài khoản của bạn đã được nâng cấp Pro thành công!")
                            
                            # Hiển thị thông tin
                            col1, col2 = st.columns(2)
                            with col1:
                                st.info(f"**Payment ID:** {payment_id}")
                                st.info(f"**Trạng thái:** {payment_status.get('status', 'N/A')}")
                            with col2:
                                if payment_status.get('completed_at'):
                                    st.info(f"**Hoàn tất lúc:** {payment_status.get('completed_at')}")
                            
                            # Hướng dẫn cập nhật app desktop
                            st.markdown("---")
                            st.markdown("### 📱 Cập nhật thông tin trên App Desktop")
                            st.warning("""
                            **Quan trọng:** Để sử dụng tính năng Pro, bạn cần cập nhật thông tin trên ứng dụng desktop:
                            
                            1. Mở ứng dụng desktop của bạn
                            2. Nhấn nút "Kiểm tra thanh toán" hoặc "Làm mới tài khoản"
                            3. Ứng dụng sẽ tự động cập nhật thông tin Pro từ server
                            """)
                except Exception as e:
                    st.warning(f"Không thể kiểm tra trạng thái thanh toán: {str(e)}")
        
        elif payment_error:
            st.error("❌ Thanh toán thất bại. Vui lòng thử lại.")
        elif payment_cancel:
            st.warning("⚠️ Thanh toán đã bị hủy.")

    else:  # Phần tìm kiếm video
        st.header("🔍 Tìm kiếm video toàn cầu")
        st.markdown("---")
        
        # Khởi tạo các đối tượng
        downloader = VideoDownloader()
        
        # Khởi tạo session state để lưu API key
        if 'gemini_api_key' not in st.session_state:
            st.session_state.gemini_api_key = "AIzaSyCHyVRFSCB8m2muEBYhqShBXEd9H8hgmSQ"  # API key mặc định
        
        # Thêm phần nhập API key
        with st.expander("🔑 Cài đặt API Key Gemini", expanded=False):
            st.markdown("""
            <div class="api-key-container">
                <p style="margin: 0 0 5px 0; font-size: 0.9em;">Nhập API key Gemini để sử dụng dịch thuật. Nếu dịch không hoạt động, hãy thử đổi API key mới.</p>
                <p style="margin: 0; font-size: 0.8em; color: #666;">Lấy API key tại: <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a></p>
            </div>
            """, unsafe_allow_html=True)
            
            new_api_key = st.text_input(
                "API Key Gemini:",
                value=st.session_state.gemini_api_key,
                type="password",
                help="Nhập API key của Google Gemini để sử dụng chức năng dịch"
            )
            
            if st.button("💾 Lưu API Key"):
                st.session_state.gemini_api_key = new_api_key
                st.success("✅ Đã lưu API key mới!")
        
        # Khởi tạo translator với API key từ session state
        translator = GeminiTranslator(api_key=st.session_state.gemini_api_key)
        
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
                    translation_failed = False
                    
                    for lang_code in selected_languages:
                        translated_keyword = translator.translate(keyword, src='vi', dest=lang_code)
                        if translated_keyword:
                            translated_keywords[lang_code] = translated_keyword
                        else:
                            translation_failed = True
                            translated_keywords[lang_code] = keyword
                    
                    # Đảm bảo các ngôn ngữ cơ bản luôn có sẵn để sử dụng nếu cần
                    if 'en' not in translated_keywords:
                        translated_keywords['en'] = keyword
                    if 'zh-cn' not in translated_keywords:
                        translated_keywords['zh-cn'] = keyword
                    if 'ja' not in translated_keywords:
                        translated_keywords['ja'] = keyword
                    
                    # Hiển thị cảnh báo nếu dịch thất bại
                    if translation_failed:
                        st.warning("""
                        ⚠️ Dịch thuật không thành công! Có thể do:
                        - API key không hợp lệ hoặc đã hết hạn
                        - Đã vượt quá giới hạn sử dụng API
                        
                        Hãy thử mở mục "🔑 Cài đặt API Key Gemini" và đổi API key mới.
                        """)
                    
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





