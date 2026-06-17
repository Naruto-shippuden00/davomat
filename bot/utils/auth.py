"""Autentifikatsiya va ruxsat tekshirish"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models import User
from config import ROLE_ADMIN, ROLE_TEACHER, ROLE_CLASS_TEACHER, ROLE_PARENT

async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User:
    """Telegram ID orqali foydalanuvchini topish"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id, User.is_active == True)
    )
    return result.scalar_one_or_none()

async def check_user_permission(session: AsyncSession, telegram_id: int, required_roles: list) -> tuple:
    """
    Foydalanuvchi ruxsatini tekshirish
    
    Returns:
        (has_permission: bool, user: User or None, message: str)
    """
    user = await get_user_by_telegram_id(session, telegram_id)
    
    if not user:
        return (False, None, "❌ Kechirasiz, siz ro'yxatdan o'tmagansiz. Iltimos, administrator bilan bog'laning.")
    
    if user.role not in required_roles:
        return (False, user, "❌ Kechirasiz, bu funksiyadan foydalanish uchun ruxsatingiz yo'q.")
    
    return (True, user, "")

def get_role_name(role: str) -> str:
    """Rol nomini o'zbek tilida qaytarish"""
    role_names = {
        ROLE_ADMIN: "Ma'mur",
        ROLE_TEACHER: "O'qituvchi",
        ROLE_CLASS_TEACHER: "Sinf rahbari",
        ROLE_PARENT: "Ota-ona"
    }
    return role_names.get(role, "Noma'lum")
