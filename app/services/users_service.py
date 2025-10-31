from sqlalchemy.orm import Session
from app.schemas.users_schemas import UserCreate, UserLogin
from app.repositories import users_repository
import logging

logger = logging.getLogger(__name__)

class UsersService:
    def __init__(self):
        self.repository = users_repository

    def create_user(self, db: Session, user: UserCreate):
        try:
            logger.info(f"Verificando si el usuario {user.username} ya existe")
            
            # Verificar si el usuario ya existe antes de intentar crearlo
            existing_user = self.repository.get_user_by_username(db, user.username)
            if existing_user:
                logger.warning(f"Usuario {user.username} ya existe en la base de datos")
                raise ValueError("El usuario ya existe")
            
            logger.info(f"Usuario {user.username} no existe, procediendo a crearlo")
            
            # Intentar crear el usuario
            result = self.repository.create_user(db, user)
            logger.info(f"Usuario {user.username} creado exitosamente")
            return result
        except ValueError as e:
            # Re-raise ValueError para que se maneje en el endpoint
            logger.warning(f"Error de validación en create_user: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado en create_user para {user.username}: {str(e)}", exc_info=True)
            raise ValueError(f"Error al crear usuario: {str(e)}")

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

    # NUEVO
    def get_security_questions(self, db: Session, username: str):
        return self.repository.get_security_questions(db, username)

    def verify_security_answers(self, db: Session, username: str, answers: list[str]) -> bool:
        return self.repository.verify_security_answers(db, username, answers)

    def update_password(self, db: Session, username: str, new_password: str):
        try:
            result = self.repository.update_password(db, username, new_password)
            if not result:
                raise ValueError("Usuario no encontrado")
            return result
        except ValueError as e:
            # Re-raise ValueError para que se maneje en el endpoint
            raise
        except Exception as e:
            logger.error(f"Error inesperado en update_password: {str(e)}")
            raise ValueError(f"Error al actualizar contraseña: {str(e)}")
