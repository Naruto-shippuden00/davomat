"""Start va yordam handlerlari"""
from telegram import Update
from telegram.ext import ContextTypes
from bot.models import get_session, User
from bot.keyboards import get_main_keyboard
from bot.utils.auth import get_user_by_telegram_id, get_role_name
from config import EMOJI_HELP

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start buyrug'i handler"""
    telegram_id = update.effective_user.id
    
    async for session in get_session():
        user = await get_user_by_telegram_id(session, telegram_id)
        
        if not user:
            await update.message.reply_text(
                "👋 Assalomu alaykum!\n\n"
                "Siz hali ro'yxatdan o'tmagansiz. "
                "Iltimos, maktab ma'muriyatiga murojaat qilib, "
                "ro'yxatdan o'ting.\n\n"
                "📞 Yordam uchun: /yordam"
            )
            return
        
        role_name = get_role_name(user.role)
        keyboard = get_main_keyboard(user.role)
        
        welcome_message = f"""
👋 Assalomu alaykum, {user.full_name}!

Siz {role_name} sifatida tizimga kirdingiz.

📱 Quyidagi tugmalar orqali botdan foydalanishingiz mumkin:
"""
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=keyboard
        )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam buyrug'i handler"""
    telegram_id = update.effective_user.id
    
    async for session in get_session():
        user = await get_user_by_telegram_id(session, telegram_id)
        
        if not user:
            help_text = f"""
{EMOJI_HELP} YORDAM

Bu bot maktab o'quvchilarining davomatini boshqarish uchun mo'ljallangan.

Bot dan foydalanish uchun ro'yxatdan o'tish kerak.
Iltimos, maktab ma'muriyatiga murojaat qiling.

📞 Qo'shimcha savol bo'lsa: @support
"""
        else:
            role_name = get_role_name(user.role)
            
            if user.role in ["admin", "teacher", "class_teacher"]:
                help_text = f"""
{EMOJI_HELP} YORDAM - {role_name}

📚 ASOSIY BUYRUQLAR:
━━━━━━━━━━━━━━━━━━━━

/davomat - Bugungi davomatni boshlash
  • O'quvchilar ro'yxatini ko'rish
  • Har bir o'quvchi holatini belgilash
  • Kechikkanlar uchun sabab yozish

/hisobot - Hisobotlarni ko'rish
  • Kunlik davomat
  • Haftalik statistika
  • Oylik hisobot
  • Sinf bo'yicha tahlil

/oquvchilar - O'quvchilar boshqaruvi
  • Ro'yxatni ko'rish
  • Yangi o'quvchi qo'shish
  • Ma'lumotlarni tahrirlash

/sozlamalar - Sozlamalar
  • Sinf sozlamalari
  • Fan sozlamalari
  • Profil sozlamalari

📝 QISQA YO'LLAR:
━━━━━━━━━━━━━━━━━━━━
Tugmalar orqali tez kirish imkoniyati:
📅 Davomat boshlash
📊 Hisobotlar
👥 O'quvchilar
⚙️ Sozlamalar

💡 MASLAHATLAR:
━━━━━━━━━━━━━━━━━━━━
• Davomat har kuni dars boshida belgilang
• Kechikkanlar uchun sabab yozing
• Ota-onalarga avtomatik xabar yuboriladi
• Haftalik hisobotlarni tekshirib turing

📞 Yordam: @support
"""
            else:  # parent
                help_text = f"""
{EMOJI_HELP} YORDAM - {role_name}

📚 ASOSIY FUNKSIYALAR:
━━━━━━━━━━━━━━━━━━━━

📊 Farzandim davomati
  • Kunlik davomat
  • Haftalik statistika
  • Oylik hisobot

🔔 XABARNOMALAR:
━━━━━━━━━━━━━━━━━━━━
Sizga quyidagi holatlarda xabar yuboriladi:
  • Farzandingiz darsga kelmasa
  • Farzandingiz kechiksa
  • Oylik hisobot tayyor bo'lganda

📞 Yordam: @support
"""
        
        await update.message.reply_text(help_text)
