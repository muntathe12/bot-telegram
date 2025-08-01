"""
فحص صحة البوت والتأكد من جاهزيته للعمل
"""
import os
import sys
import asyncio
import importlib.util
from pathlib import Path

class HealthChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
    
    def check(self, name, condition, error_msg=None, warning_msg=None):
        """تشغيل فحص واحد"""
        self.total_checks += 1
        print(f"🔍 {name}...", end=" ")
        
        if condition:
            print("✅")
            self.success_count += 1
            return True
        else:
            if error_msg:
                print("❌")
                self.errors.append(f"{name}: {error_msg}")
            elif warning_msg:
                print("⚠️")
                self.warnings.append(f"{name}: {warning_msg}")
            return False
    
    async def run_all_checks(self):
        """تشغيل جميع الفحوصات"""
        print("🏥 فحص صحة البوت...")
        print("=" * 50)
        
        # فحص Python version
        python_version = sys.version_info
        self.check(
            "إصدار Python",
            python_version >= (3, 8),
            f"يتطلب Python 3.8+، الحالي: {python_version.major}.{python_version.minor}"
        )
        
        # فحص الملفات الأساسية
        required_files = [
            "main.py", "download.py", "utils.py", 
            "requirements.txt", "Procfile", "README.md"
        ]
        
        for file in required_files:
            self.check(
                f"ملف {file}",
                Path(file).exists(),
                f"الملف {file} غير موجود"
            )
        
        # فحص المكتبات المطلوبة
        required_packages = [
            ("telegram", "python-telegram-bot"),
            ("yt_dlp", "yt-dlp"),
            ("requests", "requests"),
            ("aiohttp", "aiohttp"),
            ("aiofiles", "aiofiles")
        ]
        
        for package, pip_name in required_packages:
            try:
                importlib.import_module(package.replace('-', '_'))
                self.check(f"مكتبة {pip_name}", True)
            except ImportError:
                self.check(
                    f"مكتبة {pip_name}",
                    False,
                    f"غير مثبتة. قم بتشغيل: pip install {pip_name}"
                )
        
        # فحص متغيرات البيئة
        bot_token = os.getenv('BOT_TOKEN')
        env_file_exists = Path('.env').exists()
        
        self.check(
            "ملف .env",
            env_file_exists,
            warning_msg="ملف .env غير موجود. أنشئه من .env.example"
        )
        
        self.check(
            "متغير BOT_TOKEN",
            bot_token is not None and len(bot_token) > 10,
            "BOT_TOKEN غير موجود أو غير صحيح في متغيرات البيئة"
        )
        
        # فحص استيراد الوحدات
        try:
            from main import main, start_command, help_command
            self.check("استيراد main.py", True)
        except Exception as e:
            self.check("استيراد main.py", False, str(e))
        
        try:
            from download import downloader
            self.check("استيراد download.py", True)
        except Exception as e:
            self.check("استيراد download.py", False, str(e))
        
        try:
            from utils import is_valid_url
            self.check("استيراد utils.py", True)
        except Exception as e:
            self.check("استيراد utils.py", False, str(e))
        
        # فحص وظائف الأدوات المساعدة
        try:
            from utils import is_valid_url, extract_urls_from_text
            
            # اختبار التحقق من الروابط
            valid_test = is_valid_url("https://youtube.com/watch?v=test")
            invalid_test = not is_valid_url("invalid-url")
            
            self.check(
                "وظيفة التحقق من الروابط",
                valid_test and invalid_test,
                "وظيفة is_valid_url لا تعمل بشكل صحيح"
            )
            
            # اختبار استخراج الروابط
            urls = extract_urls_from_text("Test https://youtube.com/watch?v=123 link")
            self.check(
                "وظيفة استخراج الروابط",
                len(urls) == 1 and "youtube.com" in urls[0],
                "وظيفة extract_urls_from_text لا تعمل بشكل صحيح"
            )
            
        except Exception as e:
            self.check("اختبار الأدوات المساعدة", False, str(e))
        
        # فحص اتصال yt-dlp (اختياري)
        if bot_token:
            try:
                from download import downloader
                print("🔍 اختبار yt-dlp...", end=" ")
                
                # اختبار بسيط للحصول على معلومات فيديو
                info = await downloader.get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                if info and 'title' in info:
                    print("✅")
                    self.success_count += 1
                else:
                    print("⚠️")
                    self.warnings.append("yt-dlp: قد يكون هناك قيود على الشبكة أو المنطقة")
                self.total_checks += 1
                
            except Exception as e:
                print("⚠️")
                self.warnings.append(f"yt-dlp: {str(e)}")
                self.total_checks += 1
        
        # عرض النتائج
        self.show_results()
    
    def show_results(self):
        """عرض نتائج الفحص"""
        print("\n" + "=" * 50)
        print("📊 نتائج الفحص:")
        print(f"✅ نجح: {self.success_count}/{self.total_checks}")
        
        if self.errors:
            print(f"❌ أخطاء: {len(self.errors)}")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print(f"⚠️ تحذيرات: {len(self.warnings)}")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        print("\n" + "=" * 50)
        
        if not self.errors:
            print("🎉 البوت جاهز للعمل!")
            print("\n📋 الخطوات التالية:")
            print("1. python main.py - لتشغيل البوت")
            print("2. python test_bot.py - لاختبار الوظائف")
            print("3. ارفع على GitHub ونشر على Render")
        else:
            print("🔧 يرجى إصلاح الأخطاء أولاً:")
            print("1. pip install -r requirements.txt")
            print("2. cp .env.example .env")
            print("3. أضف BOT_TOKEN في ملف .env")
        
        return len(self.errors) == 0

async def main():
    """تشغيل فحص الصحة"""
    checker = HealthChecker()
    success = await checker.run_all_checks()
    
    # إنهاء البرنامج بكود الخطأ المناسب
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())