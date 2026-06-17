"""Davomat keyboardlari"""
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config import EMOJI_PRESENT, EMOJI_ABSENT, EMOJI_LATE

def get_status_keyboard(student_id: int, current_status: str = None) -> InlineKeyboardMarkup:
    """O'quvchi uchun holat tanlash keyboardi"""
    keyboard = [
        [
            InlineKeyboardButton(
                f"{EMOJI_PRESENT} Keldi" if current_status != "keldi" else f"✓ {EMOJI_PRESENT} Keldi",
                callback_data=f"status_{student_id}_keldi"
            ),
            InlineKeyboardButton(
                f"{EMOJI_LATE} Kechikdi" if current_status != "kechikdi" else f"✓ {EMOJI_LATE} Kechikdi",
                callback_data=f"status_{student_id}_kechikdi"
            ),
            InlineKeyboardButton(
                f"{EMOJI_ABSENT} Kelmadi" if current_status != "kelmadi" else f"✓ {EMOJI_ABSENT} Kelmadi",
                callback_data=f"status_{student_id}_kelmadi"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_attendance_keyboard(students: list, attendances: dict = None) -> InlineKeyboardMarkup:
    """Barcha o'quvchilar uchun davomat keyboardi"""
    keyboard = []
    
    for student in students:
        status = attendances.get(student.id) if attendances else None
        status_emoji = ""
        
        if status == "keldi":
            status_emoji = EMOJI_PRESENT
        elif status == "kelmadi":
            status_emoji = EMOJI_ABSENT
        elif status == "kechikdi":
            status_emoji = EMOJI_LATE
        
        keyboard.append([
            InlineKeyboardButton(
                f"{status_emoji} {student.full_name}" if status_emoji else student.full_name,
                callback_data=f"student_{student.id}"
            )
        ])
    
    # Saqlash tugmasi
    keyboard.append([
        InlineKeyboardButton("💾 Saqlash va tugatish", callback_data="save_attendance")
    ])
    
    return InlineKeyboardMarkup(keyboard)

def get_late_reason_keyboard() -> InlineKeyboardMarkup:
    """Kechikish sababini tanlash keyboardi"""
    keyboard = [
        [InlineKeyboardButton("🚌 Transport muammosi", callback_data="late_reason_transport")],
        [InlineKeyboardButton("😴 Uxlab qolish", callback_data="late_reason_oversleep")],
        [InlineKeyboardButton("🤒 Kasallik", callback_data="late_reason_illness")],
        [InlineKeyboardButton("👨‍👩‍👧 Oilaviy sabab", callback_data="late_reason_family")],
        [InlineKeyboardButton("📝 Boshqa", callback_data="late_reason_other")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Tasdiqlash keyboardi"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Ha", callback_data="confirm_yes"),
            InlineKeyboardButton("❌ Yo'q", callback_data="confirm_no")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
