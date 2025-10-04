# Módulo de repositorios - Patrón Repository
from .base import BaseRepository
from .vehicle_repository import VehicleRepository
from .driver_repository import DriverRepository
from .client_repository import ClientRepository
from .address_repository import AddressRepository

__all__ = [
    'BaseRepository',
    'VehicleRepository',
    'DriverRepository', 
    'ClientRepository',
    'AddressRepository'
]
