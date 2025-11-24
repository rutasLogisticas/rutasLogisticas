"""
Modelo de Permiso para el sistema de rutas logísticas

Este módulo define el modelo de datos para los permisos del sistema.
"""
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class Permission(BaseModel):
    """
    Modelo de Permiso
    
    Representa un permiso específico en el sistema.
    
    Atributos:
        name (str): Nombre del permiso (único)
        resource (str): Recurso al que aplica (users, vehicles, etc.)
        action (str): Acción permitida (create, read, update, delete)
        description (str): Descripción del permiso
    """
    __tablename__ = "permissions"
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    resource = Column(String(50), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Relaciones
    role_permissions = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}', resource='{self.resource}', action='{self.action}')>"
