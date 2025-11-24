from pydantic import BaseModel, field_validator
from typing import Optional, List
from app.core.security import validate_password_policy


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    security_question1: Optional[str] = None
    security_answer1: Optional[str] = None
    security_question2: Optional[str] = None
    security_answer2: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = True

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        try:
            validate_password_policy(v)
        except ValueError as e:
            raise ValueError(str(e))
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None

class UserLogin(BaseModel):
    username: str
    password: str

class RoleInfo(BaseModel):
    """Información básica del rol"""
    id: int
    name: str
    
    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    role_id: Optional[int] = None
    is_active: bool
    role: Optional[RoleInfo] = None

    class Config:
        from_attributes = True

class RecoveryStartIn(BaseModel):
    username: str

class SecurityQuestionsOut(BaseModel):
    username: str
    questions: List[str]

class VerifyAnswersIn(BaseModel):
    username: str
    answers: List[str]  # en el mismo orden de questions

class ResetPasswordIn(BaseModel):
    token: str
    username: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        try:
            validate_password_policy(v)
        except ValueError as e:
            raise ValueError(str(e))
        return v

# Este es el que usarás como response_model
UserResponse = UserOut
