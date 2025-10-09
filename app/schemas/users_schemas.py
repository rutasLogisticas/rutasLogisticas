from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool   

    class Config:
        from_attributes = True 

# Este es el que usarás como response_model
UserResponse = UserOut
