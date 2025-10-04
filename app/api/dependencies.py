"""
Dependencias para la API REST
Implementa principio DIP (Dependency Inversion Principle)
"""
from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from app.core.database import db_manager
from app.services.vehicle_service import VehicleService
from app.services.driver_service import DriverService
from app.services.client_service import ClientService
from app.services.address_service import AddressService


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener sesión de base de datos
    Implementa principio DIP
    """
    with db_manager.get_session() as session:
        yield session


def get_vehicle_service() -> VehicleService:
    """Dependency para obtener servicio de vehículos"""
    return VehicleService()


def get_driver_service() -> DriverService:
    """Dependency para obtener servicio de conductores"""
    return DriverService()


def get_client_service() -> ClientService:
    """Dependency para obtener servicio de clientes"""
    return ClientService()


def get_address_service() -> AddressService:
    """Dependency para obtener servicio de direcciones"""
    return AddressService()


# Dependencias combinadas para endpoints que requieren múltiples servicios
def get_services(
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    driver_service: DriverService = Depends(get_driver_service),
    client_service: ClientService = Depends(get_client_service),
    address_service: AddressService = Depends(get_address_service)
):
    """Retorna todos los servicios para endpoints que los requieren"""
    return {
        'vehicle_service': vehicle_service,
        'driver_service': driver_service,
        'client_service': client_service,
        'address_service': address_service
    }
