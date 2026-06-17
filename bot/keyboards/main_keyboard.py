"""Asosiy keyboard"""
from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import EMOJI_CALENDAR, EMOJI_CHART, EMOJI_STUDENTS, EMOJI_SETTINGS, EMOJI_HELP

def get_main_keyboard(role: str) -> ReplyKeyboardMarkup:
    """Rolga qarab asosiy keyboardni qaytarish"""
    
    if role in ["admin", "teacher", "class_teacher"]:
        keyboard = [
            [KeyboardButton(f"{EMOJI_CALENDAR} Davomat boshlash")],
            [KeyboardButton(f"{EMOJI_CHART} Hisobotlar"), KeyboardButton(f"{EMOJI_STUDENTS} O'quvchilar")],
            [KeyboardButton(f"{EMOJI_SETTINGS} Sozlamalar"), KeyboardButton(f"{EMOJI_HELP} Yordam")]
        ]
    elif role == "parent":
        keyboard = [
            [KeyboardButton(f"{EMOJI_CHART} Farzandim davomati")],
            [KeyboardButton(f"{EMOJI_HELP} Yordam")]
        ]
    else:
        keyboard = [
            [KeyboardButton(f"{EMOJI_HELP} Yordam")]
        ]
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
