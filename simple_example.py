"""
مثال بسيط على النمط الصحيح لـ python-telegram-bot v20+
"""
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start"""
    await update.message.reply_text('مرحباً! هذا مثال بسيط على البوت')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /hello"""
    await update.message.reply_text(f'مرحباً {update.effective_user.first_name}!')

async def main():
    """الدالة الرئيسية"""
    # رمز البوت
    token = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    
    # إنشاء التطبيق
    application = ApplicationBuilder().token(token).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hello", hello))
    
    # تشغيل البوت - النمط المحدث
    print("🚀 تشغيل البوت...")
    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        await application.updater.idle()
    except KeyboardInterrupt:
        print("🛑 تم إيقاف البوت")
    finally:
        # تنظيف الموارد
        if application.updater.running:
            await application.updater.stop()
        if application.running:
            await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    asyncio.run(main())