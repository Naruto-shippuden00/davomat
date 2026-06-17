"""Admin handlerlari"""
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from sqlalchemy import select
from bot.models import get_session, User, Class, Student, Subject
from bot.utils.auth import check_user_permission, get_role_name
from config import ROLE_ADMIN, EMOJI_STUDENTS, EMOJI_SETTINGS

async def admin_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin menyu"""
    telegram_id = update.effective_user.id
    
    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN]
        )
        
        if not has_permission:
            await update.message.reply_text(message)
            return
        
        keyboard = [
            [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users")],
            [InlineKeyboardButton("🏫 Sinflar", callback_data="admin_classes")],
            [InlineKeyboardButton("📚 Fanlar", callback_data="admin_subjects")],
            [InlineKeyboardButton("👨‍🎓 O'quvchilar", callback_data="admin_students")],
            [InlineKeyboardButton("📊 Umumiy statistika", callback_data="admin_stats")]
        ]
        
        await update.message.reply_text(
            f"{EMOJI_SETTINGS} Admin panel\n\nBo'limni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def students_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchilar ro'yxati"""
    telegram_id = update.effective_user.id
    
    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN, ROLE_CLASS_TEACHER]
        )
        
        if not has_permission:
            await update.message.reply_text(message)
            return
        
        # Sinflarni olish
        if user.role == ROLE_ADMIN:
            classes_result = await session.execute(select(Class))
        else:
            classes_result = await session.execute(
                select(Class).where(Class.class_teacher_id == user.id)
            )
        
        classes = classes_result.scalars().all()
        
        if not classes:
            await update.message.reply_text(
                "❌ Sinflar topilmadi."
            )
            return
        
        response = f"{EMOJI_STUDENTS} O'QUVCHILAR RO'YXATI\n\n"
        
        for class_obj in classes:
            students_result = await session.execute(
                select(Student).where(
                    Student.class_id == class_obj.id,
                    Student.is_active == True
                ).order_by(Student.full_name)
            )
            students = students_result.scalars().all()
            
            response += f"📚 {class_obj.name} sinf ({len(students)} ta o'quvchi)\n"
            response += "━━━━━━━━━━━━━━━━━━━━\n"
            
            for i, student in enumerate(students, 1):
                response += f"{i}. {student.full_name}\n"
            
            response += "\n"
        
        # Telegram xabar uzunligi chegarasi
        if len(response) > 4000:
            # Uzun xabarlarni bo'lib yuborish
            parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(response)

async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sozlamalar"""
    telegram_id = update.effective_user.id
    
    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN, ROLE_TEACHER, ROLE_CLASS_TEACHER]
        )
        
        if not has_permission:
            await update.message.reply_text(message)
            return
        
        role_name = get_role_name(user.role)
        
        settings_text = f"""
{EMOJI_SETTINGS} SOZLAMALAR

👤 Profil ma'lumotlari:
━━━━━━━━━━━━━━━━━━━━
Ism: {user.full_name}
Rol: {role_name}
Telegram: @{user.username or 'N/A'}
Telefon: {user.phone or 'N/A'}

"""
        
        if user.role in [ROLE_CLASS_TEACHER, ROLE_ADMIN]:
            # Sinflar ma'lumoti
            classes_result = await session.execute(
                select(Class).where(Class.class_teacher_id == user.id)
            )
            classes = classes_result.scalars().all()
            
            if classes:
                settings_text += "🏫 Sizning sinflaringiz:\n"
                for class_obj in classes:
                    settings_text += f"  • {class_obj.name}\n"
        
        settings_text += "\n💡 Sozlamalarni o'zgartirish uchun administrator bilan bog'laning."
        
        await update.message.reply_text(settings_text)

# Admin handlers ro'yxati
admin_handlers = [
    admin_menu_handler,
    students_list_handler,
    settings_handler
]
