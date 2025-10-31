from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users_schemas import UserCreate
from passlib.context import CryptContext
from app.core.security import get_password_hash, hash_answer, verify_answer
from passlib.context import CryptContext
from app.core.security import pwd_context




def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        password_hash=get_password_hash(user.password),
        security_question1=user.security_question1,
        security_answer1_hash=hash_answer(user.security_answer1) if user.security_answer1 else None,
        security_question2=user.security_question2,
        security_answer2_hash=hash_answer(user.security_answer2) if user.security_answer2 else None,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session):
    return db.query(User).all()

# NUEVO
def get_security_questions(db: Session, username: str):
    u = get_user_by_username(db, username)
    if not u:
        return None
    questions = [q for q in [u.security_question1, u.security_question2] if q]
    return {"username": username, "questions": questions}

def verify_security_answers(db: Session, username: str, answers: list[str]) -> bool:
    u = get_user_by_username(db, username)
    if not u:
        return False
    stored = [h for h in [u.security_answer1_hash, u.security_answer2_hash] if h]
    if len(stored) != len(answers):
        return False
    for plain, hashed in zip(answers, stored):
        if not verify_answer(plain, hashed):
            return False
    return True

def update_password(db: Session, username: str, new_password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    # Genera el hash seguro de la nueva contraseña
    hashed = get_password_hash(new_password)
    user.password_hash = hashed

    # ✅ No uses db.add(user); el objeto ya está en la sesión
    db.commit()
    db.refresh(user)

    return user

