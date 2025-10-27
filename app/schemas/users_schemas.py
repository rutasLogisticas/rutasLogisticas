from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    security_question1: Optional[str] = None
    security_answer1: Optional[str] = None
    security_question2: Optional[str] = None
    security_answer2: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool   

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
    new_password: str

# Este es el que usarás como response_model
UserResponse = UserOut
