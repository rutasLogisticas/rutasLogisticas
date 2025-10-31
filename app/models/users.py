from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.core.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    security_question1 = Column(String(255), nullable=True)
    security_answer1_hash = Column(String(255), nullable=True)
    security_question2 = Column(String(255), nullable=True)
    security_answer2_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
