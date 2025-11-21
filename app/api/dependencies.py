"""
Dependencias para la API
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import get_db
from app.core.security import verify_access_token
from app.models.users import User
from app.repositories.users_repository import get_user_by_username

# Servicios
from app.services.client_service import ClientService
from app.services.driver_service import DriverService
from app.services.vehicle_service import VehicleService
from app.services.order_service import OrderService

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtiene el usuario actual basado en el token JWT
    """
    import logging
    logger = logging.getLogger(__name__)
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        logger.info(f"Verificando token: {credentials.credentials[:20]}...")
        # Verificar el token
        payload = verify_access_token(credentials.credentials)
        username: str = payload.get("sub")
        logger.info(f"Token válido para usuario: {username}")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        logger.error(f"Error JWT: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Error inesperado en autenticación: {str(e)}")
        raise credentials_exception
    
    # Obtener el usuario de la base de datos
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    return user


# Dependencias para servicios
def get_client_service() -> ClientService:
    return ClientService()

def get_driver_service() -> DriverService:
    return DriverService()

def get_vehicle_service() -> VehicleService:
    return VehicleService()

def get_order_service() -> OrderService:
    return OrderService()