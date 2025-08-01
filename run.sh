#!/bin/bash

echo "🚀 بوت تحميل الفيديوهات من تيليغرام"
echo "====================================="

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت! يرجى تثبيت Python 3.8+ أولاً"
    exit 1
fi

# التحقق من pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 غير متوفر!"
    exit 1
fi

echo "✅ Python متوفر"

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip3 install -r requirements.txt

# التحقق من ملف .env
if [ ! -f .env ]; then
    echo "⚠️ ملف .env غير موجود"
    echo "📝 تشغيل الإعداد..."
    python3 setup.py
fi

# فحص صحة البوت
echo "🏥 فحص صحة البوت..."
python3 health_check.py
if [ $? -ne 0 ]; then
    echo "❌ فشل فحص الصحة! يرجى إصلاح الأخطاء أولاً"
    exit 1
fi

# تشغيل البوت
echo "🚀 تشغيل البوت..."
python3 main.py