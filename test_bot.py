"""
ملف اختبار البوت محلياً
"""
import asyncio
import os
from download import downloader
from utils import is_valid_url, extract_urls_from_text

async def test_video_info():
    """
    اختبار الحصول على معلومات الفيديو
    """
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # YouTube
        "https://youtu.be/dQw4w9WgXcQ",  # YouTube Short URL
    ]
    
    for url in test_urls:
        print(f"\n🔍 اختبار الرابط: {url}")
        
        if not is_valid_url(url):
            print("❌ الرابط غير صحيح")
            continue
        
        try:
            info = await downloader.get_video_info(url)
            if info:
                print(f"✅ العنوان: {info['title']}")
                print(f"📺 المنصة: {info['platform']}")
                print(f"👤 المنشئ: {info['uploader']}")
                print(f"⏱️ المدة: {info['duration']} ثانية")
            else:
                print("❌ فشل في الحصول على معلومات الفيديو")
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")

async def test_download():
    """
    اختبار تحميل فيديو (اختياري - قد يستغرق وقتاً)
    """
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"\n📥 اختبار تحميل: {test_url}")
    
    try:
        result = await downloader.download_and_get_info(test_url)
        if result:
            print(f"✅ تم التحميل بنجاح!")
            print(f"📁 المسار: {result['file_path']}")
            print(f"📊 الحجم: {result['file_size']} بايت")
            
            # حذف الملف المؤقت
            downloader.cleanup_file(result['file_path'])
            print("🗑️ تم حذف الملف المؤقت")
        else:
            print("❌ فشل في التحميل")
    except Exception as e:
        print(f"❌ خطأ في التحميل: {str(e)}")

def test_utils():
    """
    اختبار الأدوات المساعدة
    """
    print("\n🧪 اختبار الأدوات المساعدة:")
    
    # اختبار استخراج الروابط
    test_text = "شاهد هذا الفيديو https://youtube.com/watch?v=123 وهذا أيضاً https://tiktok.com/@user/video/456"
    urls = extract_urls_from_text(test_text)
    print(f"📝 النص: {test_text}")
    print(f"🔗 الروابط المستخرجة: {urls}")
    
    # اختبار التحقق من الروابط
    test_urls = [
        "https://youtube.com/watch?v=123",
        "invalid-url",
        "https://tiktok.com/@user/video/456"
    ]
    
    for url in test_urls:
        valid = is_valid_url(url)
        print(f"🔍 {url} -> {'✅ صحيح' if valid else '❌ غير صحيح'}")

async def main():
    """
    تشغيل جميع الاختبارات
    """
    print("🚀 بدء اختبار البوت...")
    
    # اختبار الأدوات المساعدة
    test_utils()
    
    # اختبار معلومات الفيديو
    await test_video_info()
    
    # اختبار التحميل (اختياري)
    download_test = input("\n❓ هل تريد اختبار التحميل؟ (قد يستغرق وقتاً) [y/N]: ")
    if download_test.lower() in ['y', 'yes', 'نعم']:
        await test_download()
    
    print("\n✅ انتهى الاختبار!")

if __name__ == "__main__":
    asyncio.run(main())