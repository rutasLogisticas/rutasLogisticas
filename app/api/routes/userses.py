from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.users_service import UsersService
from app.schemas.users_schemas import (
    UserCreate, UserResponse, UserLogin,
    RecoveryStartIn, SecurityQuestionsOut, VerifyAnswersIn, ResetPasswordIn
)
from app.core.security import create_reset_token, verify_reset_token, verify_password
import logging
from app.services.audit_service import AuditService



logger = logging.getLogger(__name__)

router = APIRouter(prefix="/userses", tags=["Usuarios"])
service = UsersService()
audit_service = AuditService()



# -------------------------------------------------
# Crear usuario
# -------------------------------------------------
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Intentando crear usuario: {user.username}")
        return service.create_user(db, user)
    except ValueError as e:
        logger.warning(f"Error de validación al crear usuario {user.username}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error en base de datos al crear usuario {user.username}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# -------------------------------------------------
# Login
# -------------------------------------------------
@router.post("/login")
def login(user: UserLogin, request: Request, db: Session = Depends(get_db)):
    # 1. Buscar usuario
    db_user = service.get_user_by_username(db, user.username)
    if not db_user:
        audit_service.registrar_evento(
        db=db,
        actor=None,
        event_type="login_fail",
        description="Usuario no existe",
        ip_address=request.client.host,
        details={"username": user.username}
    )
        # IMPORTANTE: devolvemos 404 si el usuario no existe
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Validar contraseña usando verify_password del core.security
    if not verify_password(user.password, db_user.password_hash):
        # Si el hash NO coincide con lo que el usuario escribió
        audit_service.registrar_evento(
        db=db,
        actor=db_user.username,
        event_type="login_fail",
        description="Contraseña incorrecta",
        ip_address=request.client.host,
        details=None
    )
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # 3. Ok
    audit_service.registrar_evento(
        db=db,
        actor=db_user.id,
        event_type="login_success",
        description="Inicio de sesión exitoso",
        ip_address=request.client.host,
        details={}
    )
    
    return {
        "message": "Login exitoso",
        "user_id": db_user.id,
        "username": db_user.username,
    }


# -------------------------------------------------
# Paso 1: obtener preguntas de seguridad
# -------------------------------------------------
@router.post("/recovery/start", response_model=SecurityQuestionsOut)
def recovery_start(payload: RecoveryStartIn, db: Session = Depends(get_db)):
    data = service.get_security_questions(db, payload.username)
    if not data:
        # si no hay usuario devolvemos 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # devolvemos las preguntas
    return {
        "username": payload.username,
        "questions": data["questions"],
    }


# -------------------------------------------------
# Paso 2: validar respuestas
# -------------------------------------------------
@router.post("/recovery/verify")
def recovery_verify(payload: VerifyAnswersIn, db: Session = Depends(get_db)):
    ok = service.verify_security_answers(db, payload.username, payload.answers)
    if not ok:
        raise HTTPException(status_code=401, detail="Respuestas incorrectas")

    # si pasó, generamos token temporal para reset
    token = create_reset_token(payload.username)

    return {
        "reset_token": token,
        "message": "Verificación exitosa",
    }


# -------------------------------------------------
# Paso 3: reset password
# -------------------------------------------------
@router.post("/recovery/reset")
def recovery_reset(payload: ResetPasswordIn, request: Request, db: Session = Depends(get_db)):
    try:
        # modo prueba:
        if payload.token == "token-fijo":
            username = payload.username  # <-- usa el username que mande el front
        else:
            try:
                username = verify_reset_token(payload.token)
            except Exception as e:
                logger.warning(f"Token inválido para reset: {str(e)}")
                raise HTTPException(status_code=401, detail="Token inválido o vencido")

        logger.info(f"Intentando resetear contraseña para usuario: {username}")
        updated = service.update_password(db, username, payload.new_password)

        db_user = service.get_user_by_username(db, username)
        if not updated:
            logger.warning(f"Usuario no encontrado para reset: {username}")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        service.update_password(db, username, payload.new_password)

        audit_service.registrar_evento(
            db=db,
            actor=db_user.id,
            event_type="PASSWORD_RESET",
            description="Usuario cambió su contraseña",
            ip_address=request.client.host,
            details={}
        )


        logger.info(f"Contraseña actualizada exitosamente para usuario: {username}")
        return {"message": "Contraseña actualizada"}
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Error de validación en reset: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado en recovery/reset: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# -------------------------------------------------
# Logout (cierre de sesión)
# -------------------------------------------------
@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    actor_id = data.get("actor_id")

    ip = request.client.host

    audit_service.registrar_evento(
        db=db,
        actor=actor_id,
        event_type="logout",
        description="Cierre de sesión",
        ip_address=ip,
        details={}
    )

    return {"message": "Logout registrado"}
