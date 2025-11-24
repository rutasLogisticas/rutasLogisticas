from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.models.users import User
from app.schemas.users_schemas import UserCreate, UserUpdate
from app.core.security import (
    get_password_hash,
    hash_answer,
    verify_answer,
    validate_password_policy,
)
import logging

logger = logging.getLogger(__name__)




def create_user(db: Session, user: UserCreate):
    try:
        logger.info(f"Iniciando creación de usuario: {user.username}")
        
        # Validar política de contraseña
        validate_password_policy(user.password)

        # Hash de contraseña
        try:
            password_hash = get_password_hash(user.password)
            logger.debug(f"Hash de contraseña generado para: {user.username}")
        except Exception as e:
            logger.error(f"Error al generar hash de contraseña: {str(e)}")
            raise ValueError(f"Error al procesar contraseña: {str(e)}")
        
        # Hash de respuestas de seguridad
        answer1_hash = None
        answer2_hash = None
        try:
            if user.security_answer1:
                answer1_hash = hash_answer(user.security_answer1)
            if user.security_answer2:
                answer2_hash = hash_answer(user.security_answer2)
            logger.debug(f"Hashes de respuestas generados para: {user.username}")
        except Exception as e:
            logger.error(f"Error al generar hash de respuestas: {str(e)}")
            raise ValueError(f"Error al procesar respuestas de seguridad: {str(e)}")
        
        # Crear objeto User
        try:
            db_user = User(
                username=user.username,
                password_hash=password_hash,
                security_question1=user.security_question1,
                security_answer1_hash=answer1_hash,
                security_question2=user.security_question2,
                security_answer2_hash=answer2_hash,
                role_id=user.role_id,
                is_active=user.is_active if user.is_active is not None else True
            )
            logger.debug(f"Objeto User creado para: {user.username} con role_id: {user.role_id}, is_active: {user.is_active}")
        except Exception as e:
            logger.error(f"Error al crear objeto User: {str(e)}")
            raise ValueError(f"Error al crear usuario: {str(e)}")
        
        # Agregar a la sesión
        try:
            db.add(db_user)
            logger.debug(f"Usuario agregado a sesión: {user.username}")
        except Exception as e:
            logger.error(f"Error al agregar usuario a sesión: {str(e)}")
            raise ValueError(f"Error al agregar usuario: {str(e)}")
        
        # Flush para validar sin commit
        try:
            db.flush()
            logger.debug(f"Flush exitoso para: {user.username}")
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error de integridad al hacer flush: {str(e)}")
            if "username" in str(e).lower() or "unique" in str(e).lower():
                raise ValueError("El usuario ya existe")
            raise ValueError(f"Error de integridad: {str(e)}")
        
        # Refresh para obtener el ID
        try:
            db.refresh(db_user)
            logger.info(f"Usuario creado exitosamente: {user.username} (ID: {db_user.id})")
        except Exception as e:
            logger.warning(f"Error al hacer refresh, pero el usuario puede haberse creado: {str(e)}")
            # No lanzar error aquí, el refresh no es crítico
        
        return db_user
    except ValueError:
        # Re-lanzar ValueError sin modificar
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad capturado: {str(e)}")
        if "username" in str(e).lower() or "unique" in str(e).lower():
            raise ValueError("El usuario ya existe")
        raise ValueError(f"Error de integridad: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al crear usuario {user.username}: {str(e)}", exc_info=True)
        raise ValueError(f"Error al crear usuario: {str(e)}")

def get_user_by_username(db: Session, username: str):
    return db.query(User).options(joinedload(User.role)).filter(User.username == username).first()


def get_users(db: Session):
    return db.query(User).options(joinedload(User.role)).all()

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
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None

        # Validar y generar el hash seguro de la nueva contraseña
        try:
            validate_password_policy(new_password)
        except ValueError as e:
            raise ValueError(str(e)) from e

        hashed = get_password_hash(new_password)
        user.password_hash = hashed

        # ✅ No uses db.add(user); el objeto ya está en la sesión
        # El context manager hará el commit automáticamente
        db.flush()  # Flush para aplicar cambios sin commit
        db.refresh(user)

        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar contraseña para usuario {username}: {str(e)}", exc_info=True)
        raise ValueError(f"Error al actualizar contraseña: {str(e)}")


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).options(joinedload(User.role)).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        # Actualizar campos proporcionados
        if user_update.username is not None:
            # Verificar que el nuevo username no exista
            existing_user = db.query(User).filter(
                User.username == user_update.username,
                User.id != user_id
            ).first()
            if existing_user:
                raise ValueError(f"Ya existe un usuario con el nombre '{user_update.username}'")
            user.username = user_update.username

        if user_update.role_id is not None:
            user.role_id = user_update.role_id

        if user_update.is_active is not None:
            user.is_active = user_update.is_active

        db.flush()
        db.refresh(user)
        return user
    except ValueError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario {user_id}: {str(e)}", exc_info=True)
        raise ValueError(f"Error al actualizar usuario: {str(e)}")


def delete_user(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        # Eliminación lógica
        user.is_active = False
        db.flush()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar usuario {user_id}: {str(e)}", exc_info=True)
        raise ValueError(f"Error al eliminar usuario: {str(e)}")

