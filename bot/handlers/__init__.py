"""Handler modullari"""
from .start import start_handler, help_handler
from .attendance import attendance_handler, attendance_callback_handler
from .reports import reports_handler, reports_callback_handler
from .admin import (
    admin_menu_handler, 
    students_list_handler, 
    settings_handler,
    admin_callback_handler,
    admin_gender_callback,
    admin_text_handler
)

__all__ = [
    'start_handler',
    'help_handler',
    'attendance_handler',
    'attendance_callback_handler',
    'reports_handler',
    'reports_callback_handler',
    'admin_menu_handler',
    'students_list_handler',
    'settings_handler',
    'admin_callback_handler',
    'admin_gender_callback',
    'admin_text_handler'
]
