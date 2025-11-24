"""
Modelos simples
"""
from .base import BaseModel
from .vehicle import Vehicle
from .driver import Driver
from .client import Client
from .order import Order
from .users import User
from .role import Role
from .permission import Permission
from .role_permission import RolePermission

# Importar todos los modelos para que SQLAlchemy los registre
__all__ = ["BaseModel", "Vehicle", "Driver", "Client", "Order", "User", "Role", "Permission", "RolePermission"]