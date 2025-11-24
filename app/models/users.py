from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    security_question1 = Column(String(255), nullable=True)
    security_answer1_hash = Column(String(255), nullable=True)
    security_question2 = Column(String(255), nullable=True)
    security_answer2_hash = Column(String(255), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    audit_logs = relationship("AuditLog", back_populates="actor")
    
    # Relaciones
    role = relationship("Role", back_populates="users")
