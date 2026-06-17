"""Fan modeli"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Subject(Base):
    """Fan (matematika, fizika, ona tili va h.k.)"""
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(20))  # MAT, FIZ, ONA
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    attendances = relationship("Attendance", back_populates="subject")

    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name})>"
