"""Xabarlar modeli"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Notification(Base):
    """Ota-onalarga yuborilgan xabarlar"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    attendance_id = Column(Integer, ForeignKey("attendances.id"))
    message_type = Column(String(50), nullable=False)  # absent, late
    message_text = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    is_delivered = Column(Boolean, default=False)
    error_message = Column(Text)

    # Relationships
    recipient = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.message_type}, delivered={self.is_delivered})>"
