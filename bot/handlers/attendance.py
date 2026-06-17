"""Davomat handlerlari"""
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select, and_
from datetime import date, datetime, time
from bot.models import get_session, Student, Class, Subject, Attendance, User
from bot.keyboards import (
    get_attendance_keyboard, 
    get_status_keyboard, 
    get_late_reason_keyboard,
    get_confirmation_keyboard,
    get_class_selection_keyboard,
    get_subject_selection_keyboard
)
from bot.utils.auth import check_user_permission
from bot.utils.notifications import send_parent_notification
from config import ROLE_TEACHER, ROLE_CLASS_TEACHER, ROLE_ADMIN, EMOJI_CALENDAR

async def attendance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Davomat boshlash handler"""
    telegram_id = update.effective_user.id
    
    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN, ROLE_TEACHER, ROLE_CLASS_TEACHER]
        )
        
        if not has_permission:
            await update.message.reply_text(message)
            return
        
        # Sinflarni olish
        if user.role == ROLE_CLASS_TEACHER:
            # Sinf rahbari faqat o'z sinfini ko'radi
            classes_result = await session.execute(
                select(Class).where(Class.class_teacher_id == user.id)
            )
        else:
            # Admin va o'qituvchi barcha sinflarni ko'radi
            classes_result = await session.execute(select(Class))
        
        classes = classes_result.scalars().all()
        
        if not classes:
            await update.message.reply_text(
                "❌ Sizga biriktirilgan sinf topilmadi.\n"
                "Iltimos, administrator bilan bog'laning."
            )
            return
        
        if len(classes) == 1:
            # Faqat bitta sinf bo'lsa, to'g'ridan-to'g'ri fan tanlashga o'tish
            context.user_data['selected_class_id'] = classes[0].id
            await show_subject_selection(update, context, session)
        else:
            # Bir nechta sinf bo'lsa, sinf tanlash
            keyboard = get_class_selection_keyboard(classes)
            await update.message.reply_text(
                f"{EMOJI_CALENDAR} Qaysi sinf uchun davomat belgilaysiz?",
                reply_markup=keyboard
            )

async def show_subject_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, session):
    """Fan tanlash ekranini ko'rsatish"""
    subjects_result = await session.execute(select(Subject))
    subjects = subjects_result.scalars().all()
    
    if not subjects:
        text = "❌ Fanlar topilmadi. Iltimos, administrator bilan bog'laning."
        if update.callback_query:
            await update.callback_query.message.edit_text(text)
        else:
            await update.message.reply_text(text)
        return
    
    keyboard = get_subject_selection_keyboard(subjects)
    text = "📚 Qaysi fan uchun davomat belgilaysiz?"
    
    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=keyboard)
    else:
        await update.message.reply_text(text, reply_markup=keyboard)

async def show_attendance_list(update: Update, context: ContextTypes.DEFAULT_TYPE, session):
    """O'quvchilar ro'yxatini ko'rsatish"""
    class_id = context.user_data.get('selected_class_id')
    subject_id = context.user_data.get('selected_subject_id')
    
    if not class_id or not subject_id:
        await update.callback_query.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")
        return
    
    # Sinfni olish
    class_obj = await session.get(Class, class_id)
    subject = await session.get(Subject, subject_id)
    
    # O'quvchilarni olish
    students_result = await session.execute(
        select(Student).where(
            Student.class_id == class_id,
            Student.is_active == True
        ).order_by(Student.full_name)
    )
    students = students_result.scalars().all()
    
    if not students:
        await update.callback_query.message.edit_text(
            "❌ Bu sinfda o'quvchilar topilmadi."
        )
        return
    
    # Bugungi mavjud davomatni olish
    today = date.today()
    attendances_result = await session.execute(
        select(Attendance).where(
            and_(
                Attendance.class_id == class_id,
                Attendance.subject_id == subject_id,
                Attendance.date == today
            )
        )
    )
    existing_attendances = {a.student_id: a.status for a in attendances_result.scalars().all()}
    
    # Davomat klaviaturasi
    keyboard = get_attendance_keyboard(students, existing_attendances)
    
    # User data ga saqlash
    context.user_data['attendance_students'] = [s.id for s in students]
    context.user_data['attendance_statuses'] = existing_attendances
    context.user_data['attendance_date'] = today
    
    text = f"""
{EMOJI_CALENDAR} DAVOMAT BELGILASH

📚 Sinf: {class_obj.name}
📖 Fan: {subject.name}
📅 Sana: {today.strftime("%d.%m.%Y")}
👥 O'quvchilar soni: {len(students)}

O'quvchini tanlang va holatini belgilang:
"""
    
    await update.callback_query.message.edit_text(text, reply_markup=keyboard)

async def attendance_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Davomat callback handleri"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    async for session in get_session():
        # Sinf tanlash
        if data.startswith("select_class_"):
            class_id = int(data.split("_")[2])
            context.user_data['selected_class_id'] = class_id
            await show_subject_selection(update, context, session)
        
        # Fan tanlash
        elif data.startswith("select_subject_"):
            subject_id = int(data.split("_")[2])
            context.user_data['selected_subject_id'] = subject_id
            await show_attendance_list(update, context, session)
        
        # O'quvchi tanlash
        elif data.startswith("student_"):
            student_id = int(data.split("_")[1])
            context.user_data['current_student_id'] = student_id
            
            # O'quvchi ma'lumotlarini olish
            student = await session.get(Student, student_id)
            current_status = context.user_data.get('attendance_statuses', {}).get(student_id)
            
            keyboard = get_status_keyboard(student_id, current_status)
            await query.message.edit_text(
                f"👤 {student.full_name}\n\nHolatni tanlang:",
                reply_markup=keyboard
            )
        
        # Holat tanlash
        elif data.startswith("status_"):
            parts = data.split("_")
            student_id = int(parts[1])
            status = parts[2]
            
            # Holatni saqlash
            if 'attendance_statuses' not in context.user_data:
                context.user_data['attendance_statuses'] = {}
            context.user_data['attendance_statuses'][student_id] = status
            
            # Agar kechikdi bo'lsa, sabab so'rash
            if status == "kechikdi":
                context.user_data['current_student_id'] = student_id
                keyboard = get_late_reason_keyboard()
                await query.message.edit_text(
                    "⏰ Kechikish sababini tanlang:",
                    reply_markup=keyboard
                )
            else:
                # Ro'yxatga qaytish
                await show_attendance_list(update, context, session)
        
        # Kechikish sababi
        elif data.startswith("late_reason_"):
            reason = data.split("_")[2]
            student_id = context.user_data.get('current_student_id')
            
            if not student_id:
                await query.answer("❌ Xatolik yuz berdi")
                return
            
            # Sabab va vaqtni so'rash
            context.user_data['late_reason'] = reason
            context.user_data['waiting_late_minutes'] = True
            
            await query.message.edit_text(
                "⏰ Necha daqiqa kechikdi?\n"
                "Raqam kiriting (masalan: 15)"
            )
        
        # Davomatni saqlash
        elif data == "save_attendance":
            await save_attendance(update, context, session)
        
        # Tasdiqlash
        elif data == "confirm_yes":
            await process_parent_notifications(update, context, session)
        
        elif data == "confirm_no":
            await query.message.edit_text(
                "✅ Davomat saqlandi.\n"
                "Ota-onalarga xabar yuborilmadi."
            )
            context.user_data.clear()

async def save_attendance(update: Update, context: ContextTypes.DEFAULT_TYPE, session):
    """Davomatni saqlash"""
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    # User ni olish
    user_result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = user_result.scalar_one_or_none()
    
    if not user:
        await query.answer("❌ Xatolik yuz berdi")
        return
    
    class_id = context.user_data.get('selected_class_id')
    subject_id = context.user_data.get('selected_subject_id')
    attendance_date = context.user_data.get('attendance_date')
    statuses = context.user_data.get('attendance_statuses', {})
    
    if not class_id or not subject_id or not attendance_date:
        await query.answer("❌ Xatolik yuz berdi")
        return
    
    # Davomatni saqlash
    saved_count = 0
    for student_id, status in statuses.items():
        # Mavjud yozuvni tekshirish
        existing_result = await session.execute(
            select(Attendance).where(
                and_(
                    Attendance.student_id == student_id,
                    Attendance.class_id == class_id,
                    Attendance.subject_id == subject_id,
                    Attendance.date == attendance_date
                )
            )
        )
        existing = existing_result.scalar_one_or_none()
        
        if existing:
            # Mavjud yozuvni yangilash
            existing.status = status
            existing.marked_by = user.id
            existing.marked_at = datetime.utcnow()
        else:
            # Yangi yozuv yaratish
            attendance = Attendance(
                student_id=student_id,
                class_id=class_id,
                subject_id=subject_id,
                date=attendance_date,
                status=status,
                marked_by=user.id
            )
            session.add(attendance)
        
        saved_count += 1
    
    await session.commit()
    
    # Ota-onalarga xabar yuborish tasdiqini so'rash
    absent_or_late = len([s for s, st in statuses.items() if st in ["kelmadi", "kechikdi"]])
    
    if absent_or_late > 0:
        keyboard = get_confirmation_keyboard()
        await query.message.edit_text(
            f"✅ Davomat saqlandi! ({saved_count} ta o'quvchi)\n\n"
            f"⚠️ {absent_or_late} ta o'quvchi kelmadi yoki kechikdi.\n\n"
            "Ota-onalarga xabar yuborilsinmi?",
            reply_markup=keyboard
        )
    else:
        await query.message.edit_text(
            f"✅ Davomat muvaffaqiyatli saqlandi!\n"
            f"Jami: {saved_count} ta o'quvchi"
        )
        context.user_data.clear()

async def process_parent_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE, session):
    """Ota-onalarga xabar yuborish"""
    query = update.callback_query
    
    class_id = context.user_data.get('selected_class_id')
    subject_id = context.user_data.get('selected_subject_id')
    attendance_date = context.user_data.get('attendance_date')
    statuses = context.user_data.get('attendance_statuses', {})
    
    # Xabar yuborish
    sent_count = 0
    failed_count = 0
    
    subject = await session.get(Subject, subject_id)
    
    for student_id, status in statuses.items():
        if status in ["kelmadi", "kechikdi"]:
            # O'quvchi va ota-onasini olish
            student = await session.get(Student, student_id)
            if not student or not student.parent_id:
                failed_count += 1
                continue
            
            parent = await session.get(User, student.parent_id)
            if not parent:
                failed_count += 1
                continue
            
            # Davomat yozuvini olish
            attendance_result = await session.execute(
                select(Attendance).where(
                    and_(
                        Attendance.student_id == student_id,
                        Attendance.class_id == class_id,
                        Attendance.subject_id == subject_id,
                        Attendance.date == attendance_date
                    )
                )
            )
            attendance = attendance_result.scalar_one_or_none()
            
            if attendance:
                # Xabar yuborish
                success = await send_parent_notification(
                    context.bot,
                    session,
                    attendance,
                    student,
                    parent,
                    subject.name
                )
                
                if success:
                    sent_count += 1
                else:
                    failed_count += 1
    
    result_text = f"✅ Davomat saqlandi va xabarlar yuborildi!\n\n"
    result_text += f"📤 Yuborildi: {sent_count}\n"
    if failed_count > 0:
        result_text += f"❌ Yuborilmadi: {failed_count}\n"
    
    await query.message.edit_text(result_text)
    context.user_data.clear()
