"""
Modelo de Rol para el sistema de rutas logísticas

Este módulo define el modelo de datos para los roles del sistema,
incluyendo la relación con permisos y usuarios.
"""
from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class Role(BaseModel):
    """
    Modelo de Rol
    
    Representa un rol en el sistema con sus permisos asociados.
    
    Atributos:
        name (str): Nombre del rol (único)
        description (str): Descripción del rol
        is_active (bool): Indica si el rol está activo
    """
    __tablename__ = "roles"
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Relaciones
    users = relationship("User", back_populates="role")
    role_permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"
