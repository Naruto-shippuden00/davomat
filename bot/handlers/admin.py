"""Admin handlerlari - Sinf va o'quvchi boshqaruvi"""
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from sqlalchemy import select
from datetime import date
from bot.models import get_session, User, Class, Student, Subject
from bot.utils.auth import check_user_permission, get_role_name
from config import ROLE_ADMIN, ROLE_TEACHER, ROLE_CLASS_TEACHER, EMOJI_STUDENTS, EMOJI_SETTINGS

logger = logging.getLogger(__name__)


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
            [InlineKeyboardButton("➕ Sinf qo'shish", callback_data="admin_add_class")],
            [InlineKeyboardButton("➕ O'quvchi qo'shish", callback_data="admin_add_student")],
            [InlineKeyboardButton("➕ O'qituvchi qo'shish", callback_data="admin_add_teacher")],
            [InlineKeyboardButton("➕ Fan qo'shish", callback_data="admin_add_subject")],
            [InlineKeyboardButton("🏫 Sinflar ro'yxati", callback_data="admin_list_classes")],
            [InlineKeyboardButton("👥 O'quvchilar ro'yxati", callback_data="admin_list_students")],
            [InlineKeyboardButton("👨‍🏫 O'qituvchilar ro'yxati", callback_data="admin_list_teachers")],
            [InlineKeyboardButton("📚 Fanlar ro'yxati", callback_data="admin_list_subjects")],
        ]

        await update.message.reply_text(
            "👑 ADMINISTRATOR PANELI\n\n"
            "Quyidagi amallarni bajarishingiz mumkin:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin callback handleri"""
    query = update.callback_query
    await query.answer()

    telegram_id = update.effective_user.id

    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN]
        )

        if not has_permission:
            await query.message.edit_text(message)
            return

        data = query.data

        # ===== QO'SHISH =====
        if data == "admin_add_class":
            await query.message.edit_text(
                "➕ YANGI SINF QO'SHISH\n\n"
                "Sinf nomini kiriting (masalan: 9-A):"
            )
            context.user_data['admin_action'] = 'add_class'

        elif data == "admin_add_student":
            classes_result = await session.execute(select(Class))
            classes = classes_result.scalars().all()

            if not classes:
                await query.message.edit_text(
                    "❌ Avval sinf qo'shing!\n\n"
                    "/admin → Sinf qo'shish"
                )
                return

            keyboard = []
            for class_obj in classes:
                keyboard.append([
                    InlineKeyboardButton(
                        f"📚 {class_obj.name} sinf",
                        callback_data=f"admin_student_class_{class_obj.id}"
                    )
                ])

            await query.message.edit_text(
                "➕ YANGI O'QUVCHI QO'SHISH\n\n"
                "Qaysi sinfga qo'shmoqchisiz?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data == "admin_add_teacher":
            await query.message.edit_text(
                "➕ YANGI O'QITUVCHI QO'SHISH\n\n"
                "O'qituvchining Telegram ID sini kiriting:\n\n"
                "💡 O'qituvchi @userinfobot ga /start yuborib,\n"
                "o'z ID sini olishi kerak."
            )
            context.user_data['admin_action'] = 'add_teacher_id'

        elif data == "admin_add_subject":
            await query.message.edit_text(
                "➕ YANGI FAN QO'SHISH\n\n"
                "Fan nomini kiriting (masalan: Matematika):"
            )
            context.user_data['admin_action'] = 'add_subject'

        # ===== RO'YXATLAR =====
        elif data == "admin_list_classes":
            classes_result = await session.execute(select(Class))
            classes = classes_result.scalars().all()

            if not classes:
                await query.message.edit_text("❌ Hali sinflar qo'shilmagan.")
                return

            text = "🏫 SINFLAR RO'YXATI\n\n"
            for class_obj in classes:
                students_result = await session.execute(
                    select(Student).where(
                        Student.class_id == class_obj.id,
                        Student.is_active == True
                    )
                )
                students_count = len(students_result.scalars().all())
                text += f"📚 {class_obj.name} — {students_count} ta o'quvchi\n"

            await query.message.edit_text(text)

        elif data == "admin_list_students":
            classes_result = await session.execute(select(Class))
            classes = classes_result.scalars().all()

            if not classes:
                await query.message.edit_text("❌ Hali sinflar qo'shilmagan.")
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

                response += f"📚 {class_obj.name} sinf ({len(students)} ta)\n"
                response += "━━━━━━━━━━━━━━━━━━━━\n"
                for i, student in enumerate(students, 1):
                    emoji = "👦" if student.gender == "erkak" else "👧"
                    response += f"{i}. {emoji} {student.full_name}\n"
                response += "\n"

            if len(response) > 4000:
                parts = [response[i:i + 4000] for i in range(0, len(response), 4000)]
                await query.message.edit_text(parts[0])
                for part in parts[1:]:
                    await query.message.reply_text(part)
            else:
                await query.message.edit_text(response)

        elif data == "admin_list_teachers":
            teachers_result = await session.execute(
                select(User).where(
                    User.role.in_([ROLE_TEACHER, ROLE_CLASS_TEACHER]),
                    User.is_active == True
                )
            )
            teachers = teachers_result.scalars().all()

            if not teachers:
                await query.message.edit_text("❌ Hali o'qituvchilar qo'shilmagan.")
                return

            text = "👨‍🏫 O'QITUVCHILAR RO'YXATI\n\n"
            for i, teacher in enumerate(teachers, 1):
                role_name = "Sinf rahbari" if teacher.role == ROLE_CLASS_TEACHER else "O'qituvchi"
                text += f"{i}. {teacher.full_name}\n"
                text += f"   📝 Rol: {role_name}\n"
                text += f"   🆔 ID: {teacher.telegram_id}\n\n"

            await query.message.edit_text(text)

        elif data == "admin_list_subjects":
            subjects_result = await session.execute(select(Subject))
            subjects = subjects_result.scalars().all()

            if not subjects:
                await query.message.edit_text("❌ Hali fanlar qo'shilmagan.")
                return

            text = "📚 FANLAR RO'YXATI\n\n"
            for i, subject in enumerate(subjects, 1):
                text += f"{i}. {subject.name}\n"

            await query.message.edit_text(text)

        # ===== O'QUVCHI SINF TANLASH =====
        elif data.startswith("admin_student_class_"):
            class_id = int(data.split("_")[-1])
            context.user_data['student_class_id'] = class_id
            context.user_data['admin_action'] = 'add_student'

            class_obj = await session.get(Class, class_id)
            await query.message.edit_text(
                f"➕ {class_obj.name} SINFGA O'QUVCHI QO'SHISH\n\n"
                f"O'quvchining to'liq ismini kiriting:"
            )


async def admin_gender_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jins tanlagandan keyin o'quvchi yaratish"""
    query = update.callback_query
    await query.answer()

    telegram_id = update.effective_user.id

    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN]
        )

        if not has_permission:
            return

        gender = "erkak" if query.data == "gender_erkak" else "ayol"
        student_name = context.user_data.get('student_name')
        class_id = context.user_data.get('student_class_id')

        new_student = Student(
            full_name=student_name,
            class_id=class_id,
            gender=gender,
            date_of_birth=date(2009, 1, 1),
            is_active=True
        )
        session.add(new_student)
        await session.commit()

        class_obj = await session.get(Class, class_id)
        emoji = "👦" if gender == "erkak" else "👧"

        await query.message.edit_text(
            f"✅ O'quvchi muvaffaqiyatli qo'shildi!\n\n"
            f"👤 Ism: {student_name}\n"
            f"📚 Sinf: {class_obj.name}\n"
            f"{emoji} Jins: {gender.capitalize()}\n\n"
            f"Yana qo'shish uchun /admin buyrug'ini yuboring."
        )
        context.user_data.clear()


async def admin_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin text xabarlarini qayta ishlash"""
    telegram_id = update.effective_user.id
    text = update.message.text

    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN]
        )

        if not has_permission:
            return

        action = context.user_data.get('admin_action')
        logger.info(f"Admin action: {action}, Text: {text}")

        if not action:
            return

        # ===== SINF QO'SHISH =====
        if action == 'add_class':
            class_name = text.strip().upper()

            if '-' not in class_name:
                await update.message.reply_text(
                    "❌ Noto'g'ri format!\n"
                    "To'g'ri format: 9-A, 10-B, 11-V\n\n"
                    "Yana urinib ko'ring:"
                )
                return

            try:
                parts = class_name.split('-')
                grade = int(parts[0])
                section = parts[1]
            except (ValueError, IndexError):
                await update.message.reply_text(
                    "❌ Noto'g'ri format!\n\n"
                    "Misol: 9-A, 10-B\n"
                    "Yana urinib ko'ring:"
                )
                return

            new_class = Class(
                name=class_name,
                grade=grade,
                section=section,
                academic_year="2024-2025"
            )
            session.add(new_class)
            await session.commit()

            await update.message.reply_text(
                f"✅ {class_name} sinf muvaffaqiyatli qo'shildi!\n\n"
                f"Yana qo'shish uchun /admin buyrug'ini yuboring."
            )
            context.user_data.clear()

        # ===== O'QUVCHI QO'SHISH =====
        elif action == 'add_student':
            context.user_data['student_name'] = text.strip()
            context.user_data['admin_action'] = 'add_student_gender'

            keyboard = [
                [InlineKeyboardButton("👦 Erkak", callback_data="gender_erkak")],
                [InlineKeyboardButton("👧 Ayol", callback_data="gender_ayol")]
            ]

            await update.message.reply_text(
                "Jinsini tanlang:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        # ===== O'QITUVCHI QO'SHISH (ID) =====
        elif action == 'add_teacher_id':
            try:
                teacher_telegram_id = int(text.strip())
            except ValueError:
                await update.message.reply_text(
                    "❌ Noto'g'ri format!\n"
                    "Telegram ID raqam bo'lishi kerak.\n\n"
                    "Misol: 123456789\n"
                    "Yana urinib ko'ring:"
                )
                return

            existing_result = await session.execute(
                select(User).where(User.telegram_id == teacher_telegram_id)
            )
            existing = existing_result.scalar_one_or_none()

            if existing:
                await update.message.reply_text(
                    f"❌ Bu Telegram ID allaqachon mavjud!\n"
                    f"Foydalanuvchi: {existing.full_name}\n"
                    f"Rol: {get_role_name(existing.role)}"
                )
                context.user_data.clear()
                return

            context.user_data['teacher_telegram_id'] = teacher_telegram_id
            context.user_data['admin_action'] = 'add_teacher_name'

            await update.message.reply_text(
                "O'qituvchining to'liq ismini kiriting:"
            )

        # ===== O'QITUVCHI QO'SHISH (ISM) =====
        elif action == 'add_teacher_name':
            teacher_name = text.strip()
            teacher_telegram_id = context.user_data.get('teacher_telegram_id')

            new_teacher = User(
                telegram_id=teacher_telegram_id,
                full_name=teacher_name,
                role=ROLE_TEACHER,
                is_active=True
            )
            session.add(new_teacher)
            await session.commit()

            await update.message.reply_text(
                f"✅ O'qituvchi muvaffaqiyatli qo'shildi!\n\n"
                f"👨‍🏫 Ism: {teacher_name}\n"
                f"🆔 Telegram ID: {teacher_telegram_id}\n"
                f"📝 Rol: O'qituvchi\n\n"
                f"O'qituvchi endi botga /start yuborib,\n"
                f"davomat belgilashi mumkin!\n\n"
                f"Yana qo'shish uchun /admin buyrug'ini yuboring."
            )
            context.user_data.clear()

        # ===== FAN QO'SHISH =====
        elif action == 'add_subject':
            subject_name = text.strip()
            code = ''.join([w[0].upper() for w in subject_name.split()[:3]])

            new_subject = Subject(
                name=subject_name,
                code=code
            )
            session.add(new_subject)
            await session.commit()

            await update.message.reply_text(
                f"✅ \"{subject_name}\" fani muvaffaqiyatli qo'shildi!\n\n"
                f"Yana qo'shish uchun /admin buyrug'ini yuboring."
            )
            context.user_data.clear()


async def students_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchilar ro'yxati (buyruq orqali)"""
    telegram_id = update.effective_user.id

    async for session in get_session():
        has_permission, user, message = await check_user_permission(
            session, telegram_id, [ROLE_ADMIN]
        )

        if not has_permission:
            await update.message.reply_text(message)
            return

        classes_result = await session.execute(select(Class))
        classes = classes_result.scalars().all()

        if not classes:
            await update.message.reply_text("❌ Hali sinflar qo'shilmagan.")
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

            response += f"📚 {class_obj.name} sinf ({len(students)} ta)\n"
            response += "━━━━━━━━━━━━━━━━━━━━\n"
            for i, student in enumerate(students, 1):
                emoji = "👦" if student.gender == "erkak" else "👧"
                response += f"{i}. {emoji} {student.full_name}\n"
            response += "\n"

        if len(response) > 4000:
            parts = [response[i:i + 4000] for i in range(0, len(response), 4000)]
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

        settings_text = (
            f"{EMOJI_SETTINGS} SOZLAMALAR\n\n"
            f"👤 Profil ma'lumotlari:\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Ism: {user.full_name}\n"
            f"Rol: {role_name}\n"
            f"Telegram: @{user.username or 'N/A'}\n"
        )

        await update.message.reply_text(settings_text)
