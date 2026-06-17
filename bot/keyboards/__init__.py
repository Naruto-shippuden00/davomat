"""Keyboard modullari"""
from .main_keyboard import get_main_keyboard
from .attendance_keyboard import get_attendance_keyboard, get_status_keyboard
from .report_keyboard import get_report_keyboard

__all__ = [
    'get_main_keyboard',
    'get_attendance_keyboard',
    'get_status_keyboard',
    'get_report_keyboard'
]
