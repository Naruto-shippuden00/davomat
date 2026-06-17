"""Asosiy bot fayl"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from bot.models import init_db
from bot.handlers.start import start_handler, help_handler
from bot.handlers.attendance import attendance_handler, attendance_callback_handler
from bot.handlers.reports import reports_handler, reports_callback_handler
from bot.handlers.admin import admin_menu_handler, students_list_handler, settings_handler
from config import BOT_TOKEN, EMOJI_CALENDAR, EMOJI_CHART, EMOJI_STUDENTS, EMOJI_SETTINGS, EMOJI_HELP

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text xabarlarni qayta ishlash"""
    text = update.message.text
    
    if EMOJI_CALENDAR in text or "Davomat" in text:
        await attendance_handler(update, context)
    elif EMOJI_CHART in text or "Hisobot" in text or "davomat" in text.lower():
        await reports_handler(update, context)
    elif EMOJI_STUDENTS in text or "O'quvchi" in text:
        await students_list_handler(update, context)
    elif EMOJI_SETTINGS in text or "Sozlama" in text:
        await settings_handler(update, context)
    elif EMOJI_HELP in text or "Yordam" in text:
        await help_handler(update, context)
    else:
        await update.message.reply_text(
            "❓ Buyruq tushunilmadi.\n"
            "Yordam uchun /yordam buyrug'ini yuboring."
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Xatolarni qayta ishlash"""
    logger.error(f"Exception while handling an update: {context.error}")
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.\n"
            "Agar muammo davom etsa, administrator bilan bog'laning."
        )

async def post_init(application: Application):
    """Bot ishga tushgandan keyin"""
    logger.info("Ma'lumotlar bazasini ishga tushirish...")
    await init_db()
    logger.info("Ma'lumotlar bazasi tayyor!")
    
    # Railway uchun - admin foydalanuvchi yaratish
    from bot.models import get_session, User
    from config import ADMIN_TELEGRAM_ID, ROLE_ADMIN
    from sqlalchemy import select
    
    async for session in get_session():
        # Admin borligini tekshirish
        result = await session.execute(
            select(User).where(User.telegram_id == ADMIN_TELEGRAM_ID)
        )
        admin = result.scalar_one_or_none()
        
        if not admin and ADMIN_TELEGRAM_ID:
            # Admin yaratish
            admin = User(
                telegram_id=ADMIN_TELEGRAM_ID,
                username="admin",
                full_name="Administrator",
                role=ROLE_ADMIN
            )
            session.add(admin)
            await session.commit()
            logger.info(f"Admin foydalanuvchi yaratildi: {ADMIN_TELEGRAM_ID}")
        break

def main():
    """Botni ishga tushirish"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN topilmadi! .env faylini tekshiring.")
        return
    
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("yordam", help_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("davomat", attendance_handler))
    application.add_handler(CommandHandler("hisobot", reports_handler))
    application.add_handler(CommandHandler("oquvchilar", students_list_handler))
    application.add_handler(CommandHandler("sozlamalar", settings_handler))
    application.add_handler(CommandHandler("admin", admin_menu_handler))
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(attendance_callback_handler, pattern="^(select_class_|select_subject_|student_|status_|late_reason_|save_attendance|confirm_)"))
    application.add_handler(CallbackQueryHandler(reports_callback_handler, pattern="^(report_|select_class_)"))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushmoqda...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
