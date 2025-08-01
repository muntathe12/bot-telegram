"""
وحدة تحميل الفيديوهات باستخدام yt-dlp
"""
import os
import tempfile
import asyncio
import logging
from typing import Optional, Dict, Any
import yt_dlp
from utils import clean_filename, format_file_size

logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        
    def get_ydl_opts(self, output_path: str) -> Dict[str, Any]:
        """
        إعدادات yt-dlp
        """
        return {
            'outtmpl': output_path,
            'format': 'best[height<=720]/best',  # أفضل جودة حتى 720p
            'noplaylist': True,
            'extractaudio': False,
            'audioformat': 'mp3',
            'embed_subs': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': True,
            'no_warnings': False,
            'quiet': False,
            'verbose': False,
            # إعدادات إضافية للمنصات المختلفة
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls']
                },
                'instagram': {
                    'api_version': 'v1'
                }
            },
            # تجاوز القيود الجغرافية
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            # إعدادات الشبكة
            'socket_timeout': 30,
            'retries': 3,
            # تحديد User-Agent
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }
    
    async def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على معلومات الفيديو
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'skip_download': True
            }
            
            def extract_info():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    return ydl.extract_info(url, download=False)
            
            # تشغيل في thread منفصل لتجنب blocking
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, extract_info)
            
            if info:
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'filesize': info.get('filesize', 0),
                    'ext': info.get('ext', 'mp4'),
                    'platform': info.get('extractor', 'Unknown')
                }
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على معلومات الفيديو: {str(e)}")
            return None
    
    async def download_video(self, url: str, progress_callback=None) -> Optional[str]:
        """
        تحميل الفيديو وإرجاع مسار الملف
        """
        try:
            # إنشاء اسم ملف مؤقت
            temp_filename = f"video_{hash(url) % 10000}"
            output_path = os.path.join(self.temp_dir, f"{temp_filename}.%(ext)s")
            
            # إعدادات التحميل
            ydl_opts = self.get_ydl_opts(output_path)
            
            # إضافة callback للتقدم إذا تم توفيره
            if progress_callback:
                ydl_opts['progress_hooks'] = [progress_callback]
            
            def download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
                    # البحث عن الملف المحمل
                    for file in os.listdir(self.temp_dir):
                        if file.startswith(temp_filename):
                            return os.path.join(self.temp_dir, file)
                    return None
            
            # تشغيل التحميل في thread منفصل
            loop = asyncio.get_event_loop()
            downloaded_file = await loop.run_in_executor(None, download)
            
            if downloaded_file and os.path.exists(downloaded_file):
                # التحقق من حجم الملف
                file_size = os.path.getsize(downloaded_file)
                if file_size > 50 * 1024 * 1024:  # 50MB
                    logger.warning(f"الملف كبير جداً: {format_file_size(file_size)}")
                    # يمكن ضغط الفيديو هنا إذا لزم الأمر
                
                logger.info(f"تم تحميل الفيديو بنجاح: {downloaded_file}")
                return downloaded_file
            else:
                logger.error("فشل في العثور على الملف المحمل")
                return None
                
        except yt_dlp.DownloadError as e:
            logger.error(f"خطأ في تحميل الفيديو: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"خطأ غير متوقع في التحميل: {str(e)}")
            return None
    
    def cleanup_file(self, file_path: str):
        """
        حذف الملف المؤقت
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"تم حذف الملف المؤقت: {file_path}")
        except Exception as e:
            logger.error(f"خطأ في حذف الملف: {str(e)}")
    
    async def download_and_get_info(self, url: str, progress_callback=None) -> Optional[Dict[str, Any]]:
        """
        تحميل الفيديو والحصول على معلوماته
        """
        try:
            # الحصول على معلومات الفيديو أولاً
            info = await self.get_video_info(url)
            if not info:
                return None
            
            # تحميل الفيديو
            file_path = await self.download_video(url, progress_callback)
            if not file_path:
                return None
            
            # إضافة مسار الملف للمعلومات
            info['file_path'] = file_path
            info['file_size'] = os.path.getsize(file_path)
            
            return info
            
        except Exception as e:
            logger.error(f"خطأ في تحميل الفيديو والحصول على المعلومات: {str(e)}")
            return None

# إنشاء instance عام للاستخدام
downloader = VideoDownloader()