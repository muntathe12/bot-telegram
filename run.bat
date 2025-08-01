@echo off
echo 🚀 بوت تحميل الفيديوهات من تيليغرام
echo =====================================

REM التحقق من Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت! يرجى تثبيت Python 3.8+ أولاً
    pause
    exit /b 1
)

REM التحقق من pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip غير متوفر!
    pause
    exit /b 1
)

echo ✅ Python متوفر

REM تثبيت المتطلبات
echo 📦 تثبيت المتطلبات...
pip install -r requirements.txt

REM التحقق من ملف .env
if not exist .env (
    echo ⚠️ ملف .env غير موجود
    echo 📝 تشغيل الإعداد...
    python setup.py
)

REM فحص صحة البوت
echo 🏥 فحص صحة البوت...
python health_check.py
if errorlevel 1 (
    echo ❌ فشل فحص الصحة! يرجى إصلاح الأخطاء أولاً
    pause
    exit /b 1
)

REM تشغيل البوت
echo 🚀 تشغيل البوت...
python main.py

pause