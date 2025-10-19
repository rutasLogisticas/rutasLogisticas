from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users_schemas import UserCreate
from passlib.context import CryptContext

# Configurar bcrypt con límite de rounds más bajo para evitar problemas
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)

def get_password_hash(password: str):
    # Truncar password si es muy largo (límite de bcrypt es 72 bytes)
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        password_hash=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session):
    return db.query(User).all()

