from sqlalchemy import Column, Integer, String, DateTime, JSON, func, ForeignKey, Text
from datetime import datetime
from app.models.base import BaseModel
from sqlalchemy.orm import relationship



class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"))
    actor = relationship("User", back_populates="audit_logs")
    event_type = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    ip_address = Column(String(50), nullable=False)
    extra_data = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
