"""Foydalanuvchi modeli"""
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    """Foydalanuvchi (O'qituvchi, Ma'mur, Ota-ona)"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100))
    full_name = Column(String(200), nullable=False)
    phone = Column(String(20))
    role = Column(String(50), nullable=False)  # admin, teacher, class_teacher, parent
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    students = relationship("Student", back_populates="parent", foreign_keys="Student.parent_id")
    classes = relationship("Class", back_populates="class_teacher")
    attendances = relationship("Attendance", back_populates="marked_by_user")
    notifications = relationship("Notification", back_populates="recipient")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.full_name}, role={self.role})>"
