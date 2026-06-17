"""Hisobot keyboardlari"""
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_report_keyboard() -> InlineKeyboardMarkup:
    """Hisobot turlarini tanlash keyboardi"""
    keyboard = [
        [InlineKeyboardButton("📅 Bugungi davomat", callback_data="report_today")],
        [InlineKeyboardButton("📊 Haftalik hisobot", callback_data="report_week")],
        [InlineKeyboardButton("📈 Oylik hisobot", callback_data="report_month")],
        [InlineKeyboardButton("👥 Sinf statistikasi", callback_data="report_class")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_class_selection_keyboard(classes: list) -> InlineKeyboardMarkup:
    """Sinf tanlash keyboardi"""
    keyboard = []
    
    for class_obj in classes:
        keyboard.append([
            InlineKeyboardButton(
                f"{class_obj.name} sinf",
                callback_data=f"select_class_{class_obj.id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(keyboard)

def get_subject_selection_keyboard(subjects: list) -> InlineKeyboardMarkup:
    """Fan tanlash keyboardi"""
    keyboard = []
    
    for subject in subjects:
        keyboard.append([
            InlineKeyboardButton(
                subject.name,
                callback_data=f"select_subject_{subject.id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(keyboard)
