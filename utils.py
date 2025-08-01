"""
أدوات مساعدة للبوت
"""
import re
import logging
from urllib.parse import urlparse

# إعداد نظام السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def is_valid_url(url):
    """
    التحقق من صحة الرابط
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_urls_from_text(text):
    """
    استخراج الروابط من النص
    """
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    urls = url_pattern.findall(text)
    return urls

def get_supported_platforms():
    """
    قائمة المنصات المدعومة
    """
    return [
        "YouTube", "Instagram", "TikTok", "Twitter/X", 
        "Facebook", "Reddit", "Pinterest", "Vimeo",
        "Dailymotion", "Twitch", "SoundCloud"
    ]

def format_file_size(size_bytes):
    """
    تنسيق حجم الملف
    """
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def clean_filename(filename):
    """
    تنظيف اسم الملف من الأحرف غير المسموحة
    """
    # إزالة الأحرف غير المسموحة
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    # تقصير الاسم إذا كان طويلاً جداً
    if len(cleaned) > 100:
        cleaned = cleaned[:100]
    return cleaned

def is_supported_platform(url):
    """
    التحقق من دعم المنصة
    """
    supported_domains = [
        'youtube.com', 'youtu.be', 'instagram.com', 'tiktok.com',
        'twitter.com', 'x.com', 'facebook.com', 'reddit.com',
        'pinterest.com', 'vimeo.com', 'dailymotion.com',
        'twitch.tv', 'soundcloud.com'
    ]
    
    try:
        domain = urlparse(url).netloc.lower()
        return any(supported in domain for supported in supported_domains)
    except:
        return False