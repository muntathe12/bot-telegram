import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text("👋 أهلاً بك في البوت!")

def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("❌ لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")
        return
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    logger.info("🚀 بدء تشغيل البوت...")
    application.run_polling()  # بدون await أو asyncio.run

if __name__ == "__main__":
    main()