"""
بوت تيليغرام لتحميل الفيديوهات من جميع المنصات
"""
import os
import asyncio
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction, ParseMode
from download import downloader
from utils import is_valid_url, extract_urls_from_text, get_supported_platforms, format_file_size, is_supported_platform

# إعداد نظام السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# معالجات الأوامر والرسائل
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج أمر /start
    """
    welcome_message = """
🎬 **مرحباً بك في بوت تحميل الفيديوهات!**

📱 **كيفية الاستخدام:**
• أرسل رابط أي فيديو من المنصات المدعومة
• سأقوم بتحميله وإرساله لك مباشرة!

🌟 **المنصات المدعومة:**
• YouTube (فيديوهات و Shorts)
• Instagram (Reels و Posts)
• TikTok
• Twitter / X
• Facebook
• Reddit
• Pinterest
• وأكثر من 1000+ موقع آخر!

📋 **الأوامر المتاحة:**
/help - عرض المساعدة
/platforms - قائمة المنصات المدعومة

🚀 **ابدأ الآن بإرسال رابط الفيديو!**
    """
    
    keyboard = [
        [InlineKeyboardButton("📋 المنصات المدعومة", callback_data="platforms")],
        [InlineKeyboardButton("❓ المساعدة", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج أمر /help
    """
    help_message = """
❓ **كيفية استخدام البوت:**

1️⃣ **إرسال الرابط:**
   • انسخ رابط الفيديو من أي منصة مدعومة
   • أرسله في رسالة للبوت

2️⃣ **انتظار التحميل:**
   • سيبدأ البوت في تحميل الفيديو
   • ستظهر رسالة "جارٍ التحميل..."

3️⃣ **استلام الفيديو:**
   • سيتم إرسال الفيديو مباشرة
   • مع معلومات الفيديو (العنوان، المدة، إلخ)

⚠️ **ملاحظات مهمة:**
• الحد الأقصى لحجم الفيديو: 50MB
• يتم تحميل أفضل جودة متاحة (حتى 720p)
• الروابط المختصرة مدعومة
• يمكن إرسال عدة روابط في رسالة واحدة

🔧 **في حالة وجود مشاكل:**
• تأكد من صحة الرابط
• تأكد من أن المنصة مدعومة
• جرب مرة أخرى بعد قليل

📞 **للدعم الفني:**
تواصل مع المطور عبر GitHub
    """
    
    await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)

async def platforms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج أمر /platforms
    """
    platforms = get_supported_platforms()
    platforms_text = "\n".join([f"• {platform}" for platform in platforms])
    
    message = f"""
🌐 **المنصات المدعومة:**

{platforms_text}

**وأكثر من 1000+ موقع آخر!**

✅ **أمثلة على الروابط المدعومة:**
• https://youtube.com/watch?v=...
• https://instagram.com/p/...
• https://tiktok.com/@user/video/...
• https://twitter.com/user/status/...
• https://facebook.com/watch?v=...

💡 **نصيحة:** يمكنك إرسال أي رابط فيديو وسأحاول تحميله!
    """
    
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج الرسائل النصية (الروابط)
    """
    message_text = update.message.text
    user_id = update.effective_user.id
    
    # استخراج الروابط من النص
    urls = extract_urls_from_text(message_text)
    
    if not urls:
        await update.message.reply_text(
            "❌ لم أجد أي رابط في رسالتك!\n\n"
            "📝 أرسل رابط فيديو من أي منصة مدعومة وسأقوم بتحميله لك."
        )
        return
    
    # معالجة كل رابط
    for url in urls:
        await process_video_url(update, url)

async def process_video_url(update: Update, url: str):
    """
    معالجة رابط فيديو واحد
    """
    try:
        # التحقق من صحة الرابط
        if not is_valid_url(url):
            await update.message.reply_text(f"❌ الرابط غير صحيح: {url}")
            return
        
        # إرسال رسالة "جارٍ التحميل"
        status_message = await update.message.reply_text(
            f"⏳ **جارٍ التحميل...**\n\n"
            f"🔗 الرابط: `{url}`\n"
            f"⏱️ قد يستغرق الأمر بضع ثوانٍ...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # إظهار أن البوت يكتب
        await update.message.chat.send_action(ChatAction.UPLOAD_VIDEO)
        
        # تحميل الفيديو
        video_info = await downloader.download_and_get_info(url)
        
        if not video_info:
            await status_message.edit_text(
                f"❌ **فشل في تحميل الفيديو**\n\n"
                f"🔗 الرابط: `{url}`\n\n"
                f"**الأسباب المحتملة:**\n"
                f"• الرابط غير صحيح أو منتهي الصلاحية\n"
                f"• المنصة غير مدعومة\n"
                f"• الفيديو محمي أو خاص\n"
                f"• مشكلة مؤقتة في الخادم\n\n"
                f"💡 جرب مرة أخرى أو تأكد من الرابط",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # تحديث رسالة الحالة
        await status_message.edit_text(
            f"📤 **جارٍ رفع الفيديو...**\n\n"
            f"🎬 العنوان: {video_info['title'][:50]}...\n"
            f"📊 الحجم: {format_file_size(video_info['file_size'])}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # إرسال الفيديو
        with open(video_info['file_path'], 'rb') as video_file:
            caption = create_video_caption(video_info, url)
            
            await update.message.reply_video(
                video=video_file,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN,
                supports_streaming=True
            )
        
        # حذف رسالة الحالة
        await status_message.delete()
        
        # تنظيف الملف المؤقت
        downloader.cleanup_file(video_info['file_path'])
        
    except Exception as e:
        logger.error(f"خطأ في معالجة الرابط {url}: {str(e)}")
        await update.message.reply_text(
            f"❌ **حدث خطأ غير متوقع**\n\n"
            f"🔗 الرابط: `{url}`\n"
            f"🐛 الخطأ: `{str(e)}`\n\n"
            f"💡 جرب مرة أخرى أو تواصل مع المطور",
            parse_mode=ParseMode.MARKDOWN
        )

def create_video_caption(video_info: dict, url: str) -> str:
    """
    إنشاء وصف للفيديو
    """
    title = video_info.get('title', 'Unknown')[:100]
    duration = video_info.get('duration', 0)
    uploader = video_info.get('uploader', 'Unknown')[:30]
    platform = video_info.get('platform', 'Unknown')
    file_size = format_file_size(video_info.get('file_size', 0))
    
    # تنسيق المدة
    if duration > 0:
        minutes = duration // 60
        seconds = duration % 60
        duration_str = f"{minutes:02d}:{seconds:02d}"
    else:
        duration_str = "غير محدد"
    
    caption = f"""
🎬 **{title}**

📺 **المنصة:** {platform}
👤 **المنشئ:** {uploader}
⏱️ **المدة:** {duration_str}
📊 **الحجم:** {file_size}

🔗 **الرابط الأصلي:** [اضغط هنا]({url})

🤖 **تم التحميل بواسطة:** @YourBotUsername
    """
    
    return caption.strip()

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """
    معالج الأخطاء العام
    """
    logger.error(f"خطأ في البوت: {context.error}")
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "❌ **حدث خطأ غير متوقع**\n\n"
            "🔄 جرب مرة أخرى أو تواصل مع المطور\n"
            "📞 GitHub: [رابط المشروع](https://github.com/yourusername/telegram-video-bot)",
            parse_mode=ParseMode.MARKDOWN
        )

async def main():
    """
    الدالة الرئيسية - النمط الصحيح لإصدار 20+
    """
    # الحصول على رمز البوت من متغيرات البيئة
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        logger.error("❌ لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")
        logger.error("💡 تأكد من إضافة BOT_TOKEN في إعدادات Render أو ملف .env")
        return
    
    # إنشاء التطبيق باستخدام ApplicationBuilder
    application = ApplicationBuilder().token(bot_token).build()
    
    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("platforms", platforms_command))
    
    # إضافة معالج الرسائل النصية (الروابط)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # إضافة معالج الأخطاء
    application.add_error_handler(error_handler)
    
    # تشغيل البوت - النمط المحدث
    logger.info("🚀 بدء تشغيل البوت...")
    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling(drop_pending_updates=True)
        await application.updater.idle()
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {str(e)}")
    finally:
        # تنظيف الموارد
        if application.updater.running:
            await application.updater.stop()
        if application.running:
            await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    asyncio.run(main())