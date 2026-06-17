"""Xabarlar yuborish"""
from telegram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from bot.models import Notification, Attendance, Student, User
from config import (
    PARENT_NOTIFICATION_ABSENT, 
    PARENT_NOTIFICATION_LATE,
    EMOJI_WARNING,
    EMOJI_LATE,
    LATE_REASONS
)

async def send_parent_notification(
    bot: Bot,
    session: AsyncSession,
    attendance: Attendance,
    student: Student,
    parent: User,
    subject_name: str
) -> bool:
    """
    Ota-onaga xabar yuborish
    
    Returns:
        bool: Xabar yuborilgan bo'lsa True
    """
    try:
        # Xabar shablonini tanlash
        if attendance.status == "kelmadi":
            message_text = PARENT_NOTIFICATION_ABSENT.format(
                emoji=EMOJI_WARNING,
                parent_name=parent.full_name,
                student_name=student.full_name,
                date=attendance.date.strftime("%d.%m.%Y"),
                subject=subject_name,
                time=datetime.now().strftime("%H:%M")
            )
            message_type = "absent"
        elif attendance.status == "kechikdi":
            reason = LATE_REASONS.get(attendance.late_reason, "Noma'lum")
            message_text = PARENT_NOTIFICATION_LATE.format(
                emoji=EMOJI_LATE,
                parent_name=parent.full_name,
                student_name=student.full_name,
                date=attendance.date.strftime("%d.%m.%Y"),
                minutes=attendance.late_minutes or 0,
                subject=subject_name,
                arrival_time=attendance.arrival_time.strftime("%H:%M") if attendance.arrival_time else "Noma'lum",
                reason=reason
            )
            message_type = "late"
        else:
            return False
        
        # Xabar yuborish
        await bot.send_message(
            chat_id=parent.telegram_id,
            text=message_text
        )
        
        # Notification yozuvini yaratish
        notification = Notification(
            recipient_id=parent.id,
            attendance_id=attendance.id,
            message_type=message_type,
            message_text=message_text,
            is_delivered=True
        )
        session.add(notification)
        
        # Attendance ni yangilash
        attendance.parent_notified = True
        attendance.parent_notified_at = datetime.utcnow()
        
        await session.commit()
        return True
        
    except Exception as e:
        # Xatolik yuz bersa, log qilish
        notification = Notification(
            recipient_id=parent.id,
            attendance_id=attendance.id,
            message_type=message_type if 'message_type' in locals() else "unknown",
            message_text=message_text if 'message_text' in locals() else "",
            is_delivered=False,
            error_message=str(e)
        )
        session.add(notification)
        await session.commit()
        return False
