"""
إعداد سريع للبوت
"""
import os
import sys

def create_env_file():
    """
    إنشاء ملف .env إذا لم يكن موجوداً
    """
    if os.path.exists('.env'):
        print("✅ ملف .env موجود بالفعل")
        return
    
    print("📝 إنشاء ملف .env...")
    
    bot_token = input("🤖 أدخل رمز البوت (BOT_TOKEN): ").strip()
    
    if not bot_token:
        print("❌ يجب إدخال رمز البوت!")
        return False
    
    env_content = f"""# متغيرات البيئة للبوت
BOT_TOKEN={bot_token}
LOG_LEVEL=INFO
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ تم إنشاء ملف .env بنجاح!")
    return True

def check_requirements():
    """
    التحقق من تثبيت المتطلبات
    """
    print("🔍 التحقق من المتطلبات...")
    
    required_packages = [
        'telegram',
        'yt_dlp',
        'requests',
        'aiohttp',
        'aiofiles'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 المكتبات المفقودة: {', '.join(missing_packages)}")
        print("💡 قم بتشغيل: pip install -r requirements.txt")
        return False
    
    print("✅ جميع المتطلبات متوفرة!")
    return True

def main():
    """
    الإعداد الرئيسي
    """
    print("🚀 مرحباً بك في إعداد بوت تحميل الفيديوهات!")
    print("=" * 50)
    
    # التحقق من Python version
    if sys.version_info < (3, 8):
        print("❌ يتطلب Python 3.8 أو أحدث!")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # التحقق من المتطلبات
    if not check_requirements():
        print("\n💡 قم بتثبيت المتطلبات أولاً:")
        print("pip install -r requirements.txt")
        return
    
    # إنشاء ملف .env
    if not create_env_file():
        return
    
    print("\n" + "=" * 50)
    print("🎉 تم الإعداد بنجاح!")
    print("\n📋 الخطوات التالية:")
    print("1. تأكد من صحة رمز البوت في ملف .env")
    print("2. شغل البوت: python main.py")
    print("3. اختبر البوت بإرسال رابط فيديو")
    print("\n🌐 للنشر على Render:")
    print("1. ارفع الكود على GitHub")
    print("2. أنشئ Web Service في Render")
    print("3. أضف BOT_TOKEN في متغيرات البيئة")
    print("4. انشر المشروع!")

if __name__ == "__main__":
    main()