"""
Dependencias simples para la API
"""
from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from app.core.database import db_manager
from app.services.vehicle_service import VehicleService
from app.services.driver_service import DriverService
from app.services.client_service import ClientService
from app.services.order_service import OrderService


def get_db() -> Generator[Session, None, None]:
    """Dependency para obtener sesión de base de datos"""
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


def get_order_service() -> OrderService:
    """Dependency para obtener servicio de pedidos"""
    return OrderService()