# 🚀 دليل البدء السريع

## 1️⃣ الإعداد المحلي (5 دقائق)

### الخطوة 1: إنشاء البوت
1. تحدث مع [@BotFather](https://t.me/BotFather)
2. أرسل `/newbot`
3. اختر اسم ومعرف للبوت
4. احفظ رمز البوت (Token)

### الخطوة 2: تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### الخطوة 3: إعداد متغيرات البيئة
```bash
# تشغيل الإعداد التلقائي
python setup.py

# أو إنشاء ملف .env يدوياً
cp .env.example .env
# ثم عدّل BOT_TOKEN في ملف .env
```

### الخطوة 4: تشغيل البوت
```bash
python main.py
```

### الخطوة 5: اختبار البوت
```bash
# اختبار اختياري
python test_bot.py
```

## 2️⃣ النشر على Render (10 دقائق)

### الخطوة 1: رفع على GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main
```

### الخطوة 2: إعداد Render
1. اذهب إلى [render.com](https://render.com)
2. اضغط "New" → "Web Service"
3. اربط GitHub واختر المشروع
4. الإعدادات:
   - **Name**: `telegram-video-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### الخطوة 3: متغيرات البيئة
أضف في Render:
- **Key**: `BOT_TOKEN`
- **Value**: رمز البوت من BotFather

### الخطوة 4: النشر
اضغط "Create Web Service" ✅

## 3️⃣ الاستخدام

### أوامر البوت:
- `/start` - البداية
- `/help` - المساعدة  
- `/platforms` - المنصات المدعومة

### إرسال الروابط:
```
https://youtube.com/watch?v=VIDEO_ID
https://instagram.com/p/POST_ID/
https://tiktok.com/@user/video/VIDEO_ID
https://twitter.com/user/status/TWEET_ID
```

## 4️⃣ استكشاف الأخطاء

### مشاكل شائعة:
- **"BOT_TOKEN not found"** → تأكد من إضافة رمز البوت
- **"Failed to download"** → تحقق من صحة الرابط
- **"File too large"** → الحد الأقصى 50MB

### سجلات الأخطاء:
```bash
# عرض السجلات في Render
# Dashboard → Service → Logs
```

## 5️⃣ التخصيص

### تغيير جودة التحميل:
في `download.py`:
```python
'format': 'best[height<=480]/best',  # 480p بدلاً من 720p
```

### تغيير حد حجم الملف:
```python
if file_size > 20 * 1024 * 1024:  # 20MB بدلاً من 50MB
```

### إضافة منصات جديدة:
في `utils.py`:
```python
supported_domains = [
    'newsite.com',  # أضف هنا
    # ... باقي المنصات
]
```

## 6️⃣ الدعم

- 🐛 **مشاكل**: [GitHub Issues](https://github.com/USERNAME/REPO/issues)
- 💡 **اقتراحات**: [GitHub Discussions](https://github.com/USERNAME/REPO/discussions)
- 📧 **تواصل**: your.email@example.com

---
⭐ **لا تنس إعطاء نجمة للمشروع على GitHub!**