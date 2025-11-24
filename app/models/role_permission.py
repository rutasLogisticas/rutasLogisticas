"""
Modelo de relación Rol-Permiso para el sistema de rutas logísticas

Este módulo define la tabla de relación many-to-many entre roles y permisos.
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class RolePermission(BaseModel):
    """
    Modelo de relación Rol-Permiso
    
    Tabla intermedia para la relación many-to-many entre roles y permisos.
    
    Atributos:
        role_id (int): ID del rol
        permission_id (int): ID del permiso
    """
    __tablename__ = "role_permissions"
    
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False, index=True)
    
    # Relaciones
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")
    
    def __repr__(self):
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"
