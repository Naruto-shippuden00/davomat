"""Bot sozlamalari va konfiguratsiya"""
import os
from dotenv import load_dotenv
from datetime import timezone, timedelta

load_dotenv()

# Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/davomat.db")

# Timezone (Tashkent UTC+5)
TIMEZONE = timezone(timedelta(hours=5))

# Admin
ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID", 0))

# Rollar
ROLE_ADMIN = "admin"
ROLE_TEACHER = "teacher"
ROLE_CLASS_TEACHER = "class_teacher"
ROLE_PARENT = "parent"

# Davomat holatlari
STATUS_PRESENT = "keldi"
STATUS_ABSENT = "kelmadi"
STATUS_LATE = "kechikdi"

# Kechikish sabablari
LATE_REASONS = {
    "transport": "Transport muammosi",
    "oversleep": "Uxlab qolish",
    "illness": "Kasallik",
    "family": "Oilaviy sabab",
    "other": "Boshqa"
}

# Emoji
EMOJI_PRESENT = "✅"
EMOJI_ABSENT = "❌"
EMOJI_LATE = "⏰"
EMOJI_TROPHY = "🏆"
EMOJI_WARNING = "⚠️"
EMOJI_CALENDAR = "📅"
EMOJI_CHART = "📊"
EMOJI_STUDENTS = "👥"
EMOJI_SETTINGS = "⚙️"
EMOJI_HELP = "❓"
EMOJI_BELL = "🔔"

# Xabar shablonlari
PARENT_NOTIFICATION_ABSENT = """
{emoji} Hurmatli {parent_name},

Farzandingiz {student_name} bugun {date} darsga kelmadi.

📚 Fan: {subject}
⏰ Vaqt: {time}

Qo'shimcha ma'lumot uchun sinf rahbariga murojaat qiling.
"""

PARENT_NOTIFICATION_LATE = """
{emoji} Hurmatli {parent_name},

Farzandingiz {student_name} bugun {date} darsga {minutes} daqiqa kechikdi.

📚 Fan: {subject}
⏰ Kelgan vaqt: {arrival_time}
💬 Sabab: {reason}

Qo'shimcha ma'lumot uchun sinf rahbariga murojaat qiling.
"""
