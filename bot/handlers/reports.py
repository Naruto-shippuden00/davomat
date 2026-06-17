"""Hisobot handlerlari"""
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select
from datetime import date
from bot.models import get_session, Class
from bot.keyboards import get_report_keyboard, get_class_selection_keyboard
from bot.utils.auth import check_user_permission
from bot.utils.reports import generate_daily_report, generate_weekly_report, generate_monthly_report
from config import ROLE_TEACHER, ROLE_CLASS_TEACHER, ROLE_ADMIN, ROLE_PARENT, EMOJI_CHART

async def reports_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hisobotlar menyu handler"""
    telegram_id = update.effective_user.id
    
    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN, ROLE_TEACHER, ROLE_CLASS_TEACHER, ROLE_PARENT]
        )
        
        if not has_permission:
            await update.message.reply_text(message)
            return
        
        # Ota-ona uchun alohida
        if user.role == ROLE_PARENT:
            await show_parent_report(update, context, session, user)
            return
        
        # O'qituvchilar uchun
        keyboard = get_report_keyboard()
        await update.message.reply_text(
            f"{EMOJI_CHART} Hisobot turini tanlang:",
            reply_markup=keyboard
        )

async def show_parent_report(update: Update, context: ContextTypes.DEFAULT_TYPE, session, parent):
    """Ota-ona uchun farzandi hisobotini ko'rsatish"""
    from sqlalchemy import and_
    from bot.models import Student, Attendance
    from datetime import timedelta
    from config import EMOJI_PRESENT, EMOJI_ABSENT, EMOJI_LATE
    
    # Farzandni topish
    students_result = await session.execute(
        select(Student).where(
            Student.parent_id == parent.id,
            Student.is_active == True
        )
    )
    students = students_result.scalars().all()
    
    if not students:
        await update.message.reply_text(
            "❌ Sizning farzandingiz topilmadi.\n"
            "Iltimos, administrator bilan bog'laning."
        )
        return
    
    student = students[0]  # Birinchi farzand
    
    # Oxirgi 7 kunlik davomat
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    
    attendances_result = await session.execute(
        select(Attendance).where(
            and_(
                Attendance.student_id == student.id,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        ).order_by(Attendance.date.desc())
    )
    attendances = attendances_result.scalars().all()
    
    # Statistika
    present = len([a for a in attendances if a.status == "keldi"])
    absent = len([a for a in attendances if a.status == "kelmadi"])
    late = len([a for a in attendances if a.status == "kechikdi"])
    total = len(attendances)
    
    present_percent = (present / total * 100) if total > 0 else 0
    
    report = f"""
📊 FARZANDINGIZ DAVOMATI

👤 O'quvchi: {student.full_name}
📅 Davr: {start_date.strftime("%d.%m.%Y")} - {end_date.strftime("%d.%m.%Y")}

📈 STATISTIKA:
━━━━━━━━━━━━━━━━━━━━
{EMOJI_PRESENT} Keldi: {present}
{EMOJI_ABSENT} Kelmadi: {absent}
{EMOJI_LATE} Kechikdi: {late}
📊 Davomat foizi: {present_percent:.1f}%

📋 OXIRGI KUNLAR:
━━━━━━━━━━━━━━━━━━━━
"""
    
    for attendance in attendances[:7]:  # Oxirgi 7 kun
        status_emoji = ""
        if attendance.status == "keldi":
            status_emoji = EMOJI_PRESENT
        elif attendance.status == "kelmadi":
            status_emoji = EMOJI_ABSENT
        elif attendance.status == "kechikdi":
            status_emoji = EMOJI_LATE
        
        report += f"{status_emoji} {attendance.date.strftime('%d.%m.%Y')}\n"
    
    await update.message.reply_text(report)

async def reports_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hisobot callback handleri"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    telegram_id = update.effective_user.id
    
    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN, ROLE_TEACHER, ROLE_CLASS_TEACHER]
        )
        
        if not has_permission:
            await query.message.edit_text(message)
            return
        
        # Sinf tanlash
        if data.startswith("select_class_"):
            class_id = int(data.split("_")[2])
            context.user_data['report_class_id'] = class_id
            
            # Hisobot turini olish
            report_type = context.user_data.get('report_type')
            
            if report_type == "today":
                report = await generate_daily_report(session, class_id)
            elif report_type == "week":
                report = await generate_weekly_report(session, class_id)
            elif report_type == "month":
                report = await generate_monthly_report(session, class_id)
            else:
                report = "❌ Xatolik yuz berdi"
            
            await query.message.edit_text(report)
            context.user_data.clear()
        
        # Bugungi hisobot
        elif data == "report_today":
            context.user_data['report_type'] = "today"
            await show_class_selection(update, context, session, user)
        
        # Haftalik hisobot
        elif data == "report_week":
            context.user_data['report_type'] = "week"
            await show_class_selection(update, context, session, user)
        
        # Oylik hisobot
        elif data == "report_month":
            context.user_data['report_type'] = "month"
            await show_class_selection(update, context, session, user)
        
        # Sinf statistikasi
        elif data == "report_class":
            context.user_data['report_type'] = "week"
            await show_class_selection(update, context, session, user)

async def show_class_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, session, user):
    """Sinf tanlash ekranini ko'rsatish"""
    # Sinflarni olish
    if user.role == ROLE_CLASS_TEACHER:
        classes_result = await session.execute(
            select(Class).where(Class.class_teacher_id == user.id)
        )
    else:
        classes_result = await session.execute(select(Class))
    
    classes = classes_result.scalars().all()
    
    if not classes:
        await update.callback_query.message.edit_text(
            "❌ Sinflar topilmadi."
        )
        return
    
    if len(classes) == 1:
        # Faqat bitta sinf bo'lsa, to'g'ridan-to'g'ri hisobot yaratish
        class_id = classes[0].id
        report_type = context.user_data.get('report_type')
        
        if report_type == "today":
            report = await generate_daily_report(session, class_id)
        elif report_type == "week":
            report = await generate_weekly_report(session, class_id)
        elif report_type == "month":
            report = await generate_monthly_report(session, class_id)
        else:
            report = "❌ Xatolik yuz berdi"
        
        await update.callback_query.message.edit_text(report)
        context.user_data.clear()
    else:
        # Bir nechta sinf bo'lsa, tanlash
        keyboard = get_class_selection_keyboard(classes)
        await update.callback_query.message.edit_text(
            "📚 Qaysi sinf uchun hisobot ko'rasiz?",
            reply_markup=keyboard
        )
