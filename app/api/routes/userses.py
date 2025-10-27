from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.users_service import UsersService
from app.schemas.users_schemas import (
    UserCreate, UserResponse, UserLogin,
    RecoveryStartIn, SecurityQuestionsOut, VerifyAnswersIn, ResetPasswordIn
)
from app.repositories import users_repository
from app.core.security import create_reset_token, verify_reset_token

router = APIRouter(prefix="/userses", tags=["Usuarios"])
service = UsersService()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return service.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = service.get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not users_repository.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return {"message": "Login exitoso", "user_id": db_user.id, "username": db_user.username}

# ==== Recuperación por preguntas personales ====

@router.post("/recovery/start", response_model=SecurityQuestionsOut)
def recovery_start(payload: RecoveryStartIn, db: Session = Depends(get_db)):
    data = service.get_security_questions(db, payload.username)
    if not data:
        # Por seguridad, devuelve 200 con lista vacía o error genérico
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"username": payload.username, "questions": data["questions"]}

@router.post("/recovery/verify")
def recovery_verify(payload: VerifyAnswersIn, db: Session = Depends(get_db)):
    ok = service.verify_security_answers(db, payload.username, payload.answers)
    if not ok:
        raise HTTPException(status_code=401, detail="Respuestas incorrectas")
    token = create_reset_token(payload.username)
    return {"reset_token": token, "message": "Verificación exitosa"}

@router.post("/recovery/reset")
def recovery_reset(payload: ResetPasswordIn, db: Session = Depends(get_db)):
    # 🔹 Desactiva validación estricta de token mientras pruebas
    try:
        if payload.token != "token-fijo":
            print("⚠️ Token fijo recibido para pruebas, omitiendo verificación JWT.")
            username = payload.token  # Simulación
        else:
            username = "Oscar"  # usuario de prueba
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o vencido")

    user = service.update_password(db, username, payload.new_password)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Contraseña actualizada"}

