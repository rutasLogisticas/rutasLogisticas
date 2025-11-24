from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.users_service import UsersService
from app.schemas.users_schemas import (
    UserCreate, UserResponse, UserLogin, UserUpdate,
    RecoveryStartIn, SecurityQuestionsOut, VerifyAnswersIn, ResetPasswordIn
)
from app.schemas.role_schemas import UserPermissionsResponse, PermissionResponse
from app.services.role_service import RoleService
from app.core.security import create_reset_token, verify_reset_token, verify_password, create_access_token, hash_answer
from app.api.dependencies import get_current_user
from app.models.users import User
import logging
from app.services.audit_service import AuditService



logger = logging.getLogger(__name__)

router = APIRouter(prefix="/userses", tags=["Usuarios"])
service = UsersService()
audit_service = AuditService()

role_service = RoleService()


# -------------------------------------------------
# Crear usuario (requiere autenticación)
# -------------------------------------------------
@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Usuario {current_user.username} intentando crear usuario: {user.username}")
        return service.create_user(db, user)
    except ValueError as e:
        logger.warning(f"Error de validación al crear usuario {user.username}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error en base de datos al crear usuario {user.username}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# -------------------------------------------------
# Registro público de usuario
# -------------------------------------------------
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Registra un nuevo usuario (público, no requiere autenticación)"""
    try:
        logger.info(f"Intentando registrar usuario público: {user.username}")
        # Por defecto, los usuarios registrados públicamente no tienen rol asignado
        # hasta que un admin se los asigne
        if user.role_id is None:
            user.role_id = None  # Sin rol por defecto
        created_user = service.create_user(db, user)
        logger.info(f"Usuario público {user.username} registrado exitosamente (ID: {created_user.id})")
        return created_user
    except ValueError as e:
        logger.warning(f"Error de validación al registrar usuario {user.username}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error en base de datos al registrar usuario {user.username}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# -------------------------------------------------
# Listar usuarios
# -------------------------------------------------
@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene lista de usuarios (requiere autenticación)"""
    try:
        logger.info(f"Usuario {current_user.username} solicitando lista de usuarios")
        users = service.list_users(db)
        logger.info(f"Devolviendo {len(users)} usuarios")
        return users
    except Exception as e:
        logger.error(f"Error obteniendo usuarios: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


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
    # 3. Generar token JWT
    access_token = create_access_token(data={"sub": db_user.username})
    
    # 4. Ok - incluir información del rol
    role_info = None
    if db_user.role:
        role_info = {
            "id": db_user.role.id,
            "name": db_user.role.name
        }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login exitoso",
        "user_id": db_user.id,
        "username": db_user.username,
        "role": role_info
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

# -------------------------------------------------
# Cambiar contraseña (usuario autenticado)
# -------------------------------------------------
@router.post("/change-password")
def change_password(
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Permite al usuario cambiar su propia contraseña."""
    try:
        current_password = payload.get("current_password")
        new_password = payload.get("new_password")
        
        if not current_password or not new_password:
            raise HTTPException(status_code=400, detail="Contraseña actual y nueva son requeridas")
        
        # Verificar contraseña actual
        if not verify_password(current_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
        
        # Actualizar contraseña
        updated = service.update_password(db, current_user.username, new_password)
        if not updated:
            raise HTTPException(status_code=500, detail="Error al actualizar contraseña")
        
        logger.info(f"Contraseña cambiada exitosamente para usuario: {current_user.username}")
        return {"message": "Contraseña actualizada exitosamente"}
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Error de validación en cambio de contraseña: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado en cambio de contraseña: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# -------------------------------------------------
# Gestionar preguntas de seguridad
# -------------------------------------------------
@router.get("/me/security-questions")
def get_my_security_questions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene las preguntas de seguridad del usuario actual."""
    try:
        questions = []
        if current_user.security_question1:
            questions.append({"id": 1, "question": current_user.security_question1})
        if current_user.security_question2:
            questions.append({"id": 2, "question": current_user.security_question2})
        
        return {"questions": questions}
    except Exception as e:
        logger.error(f"Error al obtener preguntas de seguridad: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/me/security-questions")
def update_my_security_questions(
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza las preguntas de seguridad del usuario actual."""
    try:
        questions = payload.get("questions", [])
        
        # Limpiar preguntas existentes
        current_user.security_question1 = None
        current_user.security_answer1_hash = None
        current_user.security_question2 = None
        current_user.security_answer2_hash = None
        
        # Actualizar con nuevas preguntas
        for i, q in enumerate(questions[:2]):  # Máximo 2 preguntas
            question = q.get("question", "").strip()
            answer = q.get("answer", "").strip()
            
            if question and answer:
                if i == 0:
                    current_user.security_question1 = question
                    current_user.security_answer1_hash = hash_answer(answer)
                elif i == 1:
                    current_user.security_question2 = question
                    current_user.security_answer2_hash = hash_answer(answer)
        
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"Preguntas de seguridad actualizadas para usuario: {current_user.username}")
        return {"message": "Preguntas de seguridad actualizadas exitosamente"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar preguntas de seguridad: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# -------------------------------------------------
# Obtener permisos del usuario actual
# -------------------------------------------------
@router.get("/me/permissions", response_model=UserPermissionsResponse)
def get_my_permissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene los permisos del usuario actualmente autenticado."""
    try:
        permissions = role_service.get_user_permissions(db, current_user.id)
        role_name = None
        if current_user.role_id:
            role = role_service.get_role_by_id(db, current_user.role_id)
            if role:
                role_name = role.name

        formatted_permissions = [
            PermissionResponse(
                id=p.id,
                name=p.name,
                resource=p.resource,
                action=p.action,
                description=p.description,
                is_active=p.is_active
            ) for p in permissions
        ]
        
        logger.info(f"Devolviendo {len(formatted_permissions)} permisos para usuario {current_user.username} (rol: {role_name})")
        return UserPermissionsResponse(
            user_id=current_user.id,
            username=current_user.username,
            role_id=current_user.role_id,
            role_name=role_name,
            permissions=formatted_permissions,
            total_permissions=len(formatted_permissions)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener permisos para usuario {current_user.username}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor al obtener permisos")


# -------------------------------------------------
# Obtener usuario por ID
# -------------------------------------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene un usuario específico por ID"""
    try:
        user = service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo usuario {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# -------------------------------------------------
# Actualizar usuario
# -------------------------------------------------
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza un usuario"""
    try:
        logger.info(f"Usuario {current_user.username} actualizando usuario {user_id}")
        updated_user = service.update_user(db, user_id, user_update)
        logger.info(f"Usuario {user_id} actualizado exitosamente")
        return updated_user
    except ValueError as e:
        logger.warning(f"Error de validación al actualizar usuario {user_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error actualizando usuario {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# -------------------------------------------------
# Eliminar usuario
# -------------------------------------------------
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina un usuario (eliminación lógica)"""
    try:
        logger.info(f"Usuario {current_user.username} eliminando usuario {user_id}")
        result = service.delete_user(db, user_id)
        logger.info(f"Usuario {user_id} eliminado exitosamente")
        return {"message": "Usuario eliminado exitosamente"}
    except ValueError as e:
        logger.warning(f"Error al eliminar usuario {user_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error eliminando usuario {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
