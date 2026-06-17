"""Sinf modeli"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Class(Base):
    """Sinf (masalan: 9-A, 10-B)"""
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # 9-A, 10-B
    grade = Column(Integer, nullable=False)  # 9, 10, 11
    section = Column(String(10), nullable=False)  # A, B, C
    class_teacher_id = Column(Integer, ForeignKey("users.id"))
    academic_year = Column(String(20))  # 2023-2024
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    class_teacher = relationship("User", back_populates="classes")
    students = relationship("Student", back_populates="class_obj")
    attendances = relationship("Attendance", back_populates="class_obj")

    def __repr__(self):
        return f"<Class(id={self.id}, name={self.name})>"
