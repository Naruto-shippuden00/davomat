"""Davomat modeli"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Attendance(Base):
    """Davomat yozuvi"""
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)  # keldi, kelmadi, kechikdi
    
    # Kechikish uchun
    late_minutes = Column(Integer)  # Necha daqiqa kechikdi
    late_reason = Column(String(50))  # transport, oversleep, illness, family, other
    late_reason_detail = Column(Text)  # Batafsil sabab
    arrival_time = Column(Time)  # Kelgan vaqt
    
    # Kim belgiladi
    marked_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    marked_at = Column(DateTime, default=datetime.utcnow)
    
    # Ota-onaga xabar yuborilganmi
    parent_notified = Column(Boolean, default=False)
    parent_notified_at = Column(DateTime)
    
    # Qo'shimcha ma'lumot
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="attendances")
    class_obj = relationship("Class", back_populates="attendances")
    subject = relationship("Subject", back_populates="attendances")
    marked_by_user = relationship("User", back_populates="attendances")

    def __repr__(self):
        return f"<Attendance(id={self.id}, student_id={self.student_id}, status={self.status}, date={self.date})>"
