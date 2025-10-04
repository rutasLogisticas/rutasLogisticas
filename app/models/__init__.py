# Módulo de modelos de datos
from .base import BaseModel
from .vehicle import Vehicle
from .driver import Driver
from .client import Client
from .address import Address

__all__ = [
    'BaseModel',
    'Vehicle', 
    'Driver',
    'Client',
    'Address'
]
