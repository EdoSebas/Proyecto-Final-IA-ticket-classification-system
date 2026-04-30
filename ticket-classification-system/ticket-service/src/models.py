from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from .database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="OPEN") # OPEN, IN_PROGRESS, CLOSED
    
    # Campos que llenará la IA asíncronamente
    ai_category = Column(String(100), nullable=True)
    ai_priority = Column(String(50), nullable=True) # HIGH, MEDIUM, LOW
    ai_confidence = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
