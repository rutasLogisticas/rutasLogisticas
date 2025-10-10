from sqlalchemy.orm import Session
from app.schemas.users_schemas import UserCreate, UserLogin
from app.repositories import users_repository

class UsersService:
    def __init__(self):
        self.repository = users_repository

    def create_user(self, db: Session, user: UserCreate):
        existing_user = self.repository.get_user_by_username(db, user.username)
        if existing_user:
            raise ValueError("El usuario ya existe")
        
        return self.repository.create_user(db, user)

    def list_users(self, db: Session):
        return self.repository.get_users(db)
    
    def get_user_by_username(self, db: Session, username: str):
        return self.repository.get_user_by_username(db, username)

    def login_user(self, db: Session, user: UserLogin):
        db_user = self.repository.get_user_by_username(db, user.username)
        if not db_user:
            raise ValueError("Usuario no encontrado")
        if not self.repository.verify_password(user.password, db_user.password_hash):
            raise ValueError("Contraseña incorrecta")
        return db_user
