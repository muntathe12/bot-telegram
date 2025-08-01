# 🎬 بوت تيليغرام لتحميل الفيديوهات

بوت تيليغرام متكامل لتحميل مقاطع الفيديو من جميع المنصات الشهيرة باستخدام Python و yt-dlp.

## ✨ المميزات

- 🌐 **دعم أكثر من 1000+ موقع** بما في ذلك:
  - YouTube (Videos & Shorts)
  - Instagram (Reels & Posts)
  - TikTok
  - Twitter / X
  - Facebook
  - Reddit
  - Pinterest
  - Vimeo, Dailymotion, Twitch وأكثر

- 🚀 **سهل الاستخدام**: أرسل الرابط واحصل على الفيديو
- 📱 **واجهة عربية**: جميع الرسائل باللغة العربية
- ⚡ **سريع وموثوق**: تحميل بأفضل جودة ممكنة
- 🔄 **معالجة الأخطاء**: رسائل خطأ واضحة ومفيدة
- 📊 **معلومات الفيديو**: عرض العنوان، المدة، الحجم، إلخ
- 🗂️ **تنظيف تلقائي**: حذف الملفات المؤقتة تلقائياً

## 🛠️ التثبيت والإعداد

### 1. إنشاء بوت تيليغرام

1. تحدث مع [@BotFather](https://t.me/BotFather) على تيليغرام
2. أرسل `/newbot` واتبع التعليمات
3. احفظ رمز البوت (Bot Token)

### 2. التثبيت المحلي

```bash
# استنساخ المشروع
git clone https://github.com/yourusername/telegram-video-bot.git
cd telegram-video-bot

# تثبيت المتطلبات
pip install -r requirements.txt

# إنشاء ملف متغيرات البيئة
cp .env.example .env

# تحرير ملف .env وإضافة رمز البوت
# BOT_TOKEN=your_bot_token_here

# تشغيل البوت
python main.py
```

### 3. النشر على Render.com

#### الخطوة 1: رفع الكود على GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/telegram-video-bot.git
git push -u origin main
```

#### الخطوة 2: إعداد Render
1. اذهب إلى [Render.com](https://render.com) وسجل دخولك
2. اضغط "New" → "Web Service"
3. اربط حساب GitHub واختر المشروع
4. املأ الإعدادات:
   - **Name**: `telegram-video-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

#### الخطوة 3: إضافة متغيرات البيئة
في إعدادات Render، أضف:
- **Key**: `BOT_TOKEN`
- **Value**: رمز البوت من BotFather

#### الخطوة 4: النشر
اضغط "Create Web Service" وانتظر اكتمال النشر.

## 📋 الأوامر المتاحة

- `/start` - رسالة الترحيب والتعليمات
- `/help` - دليل الاستخدام التفصيلي
- `/platforms` - قائمة المنصات المدعومة

## 🎯 كيفية الاستخدام

1. ابدأ محادثة مع البوت
2. أرسل `/start` للحصول على التعليمات
3. أرسل رابط أي فيديو من المنصات المدعومة
4. انتظر التحميل واستلم الفيديو!

### أمثلة على الروابط المدعومة:
```
https://youtube.com/watch?v=dQw4w9WgXcQ
https://instagram.com/p/ABC123/
https://tiktok.com/@user/video/123456789
https://twitter.com/user/status/123456789
https://facebook.com/watch?v=123456789
```

## 🏗️ هيكل المشروع

```
telegram-video-bot/
├── main.py              # الملف الرئيسي للبوت (نمط v20+)
├── download.py          # وحدة تحميل الفيديوهات
├── utils.py             # أدوات مساعدة
├── requirements.txt     # المكتبات المطلوبة
├── Procfile            # إعدادات Render
├── .env.example        # مثال على متغيرات البيئة
├── test_bot.py         # اختبارات البوت
├── health_check.py     # فحص صحة البوت
├── setup.py            # إعداد سريع
├── simple_example.py   # مثال بسيط على النمط الجديد
├── run.bat / run.sh    # ملفات تشغيل سريع
└── README.md           # هذا الملف
```

## 🔄 النمط الجديد (python-telegram-bot v20+)

البوت يستخدم النمط الصحيح لإصدار 20+ من المكتبة:

```python
from telegram.ext import ApplicationBuilder

async def main():
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # تشغيل البوت - النمط المحدث
    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        await application.updater.idle()
    finally:
        # تنظيف الموارد
        if application.updater.running:
            await application.updater.stop()
        if application.running:
            await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## ⚙️ الإعدادات المتقدمة

### تخصيص جودة التحميل
في ملف `download.py`، يمكنك تعديل إعدادات الجودة:

```python
'format': 'best[height<=720]/best',  # أفضل جودة حتى 720p
```

### تخصيص حد حجم الملف
```python
if file_size > 50 * 1024 * 1024:  # 50MB
```

### إضافة منصات جديدة
البوت يدعم تلقائياً جميع المنصات المدعومة من yt-dlp. لإضافة دعم خاص لمنصة معينة، عدّل في `utils.py`:

```python
supported_domains = [
    'newplatform.com',  # أضف المنصة الجديدة هنا
    # ... باقي المنصات
]
```

## 🐛 استكشاف الأخطاء

### مشاكل شائعة وحلولها:

1. **"فشل في تحميل الفيديو"**
   - تأكد من صحة الرابط
   - تأكد من أن الفيديو عام وليس خاص
   - جرب مرة أخرى بعد قليل

2. **"الملف كبير جداً"**
   - البوت يدعم ملفات حتى 50MB
   - يمكن تقليل الجودة في الإعدادات

3. **"المنصة غير مدعومة"**
   - تحقق من قائمة المنصات المدعومة
   - تأكد من أن الرابط صحيح

## 🔧 التطوير والمساهمة

### إضافة ميزات جديدة
1. Fork المشروع
2. أنشئ branch جديد (`git checkout -b feature/amazing-feature`)
3. اعمل التغييرات المطلوبة
4. Commit التغييرات (`git commit -m 'Add amazing feature'`)
5. Push إلى Branch (`git push origin feature/amazing-feature`)
6. افتح Pull Request

### اختبار التطوير
```bash
# تشغيل البوت في وضع التطوير
python main.py

# اختبار شامل للبوت
python test_bot.py

# فحص صحة البوت
python health_check.py

# اختبار وحدة التحميل
python -c "import asyncio; from download import downloader; asyncio.run(downloader.get_video_info('https://youtube.com/watch?v=dQw4w9WgXcQ'))"
```

## 📝 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 🤝 الدعم

- 🐛 **الإبلاغ عن الأخطاء**: [GitHub Issues](https://github.com/yourusername/telegram-video-bot/issues)
- 💡 **اقتراح ميزات**: [GitHub Discussions](https://github.com/yourusername/telegram-video-bot/discussions)
- 📧 **التواصل**: [your.email@example.com](mailto:your.email@example.com)

## 🙏 شكر وتقدير

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - مكتبة Telegram Bot API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - أداة تحميل الفيديوهات
- [Render.com](https://render.com) - منصة الاستضافة

---

⭐ **إذا أعجبك المشروع، لا تنس إعطاؤه نجمة على GitHub!**