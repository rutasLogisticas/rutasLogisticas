"""
Modelos simples
"""
from .base import BaseModel
from .vehicle import Vehicle
from .driver import Driver
from .client import Client
from .address import Address

# Importar todos los modelos para que SQLAlchemy los registre
__all__ = ["BaseModel", "Vehicle", "Driver", "Client", "Address"]