from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.users_service import UsersService
from app.schemas.users_schemas import UserCreate, UserResponse, UserLogin
from app.repositories import users_repository  # 👈 importar repo para la verificación

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
