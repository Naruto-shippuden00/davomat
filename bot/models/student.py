"""O'quvchi modeli"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Student(Base):
    """O'quvchi"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(200), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"))
    date_of_birth = Column(Date)
    gender = Column(String(10))  # erkak, ayol
    address = Column(String(500))
    parent_phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    class_obj = relationship("Class", back_populates="students")
    parent = relationship("User", back_populates="students", foreign_keys=[parent_id])
    attendances = relationship("Attendance", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.full_name})>"
