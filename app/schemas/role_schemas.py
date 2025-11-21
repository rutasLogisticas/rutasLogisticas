"""
Schemas para Roles
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    """Schema base para permisos"""
    name: str = Field(..., description="Nombre del permiso")
    resource: str = Field(..., description="Recurso (users, vehicles, etc.)")
    action: str = Field(..., description="Acción (create, read, update, delete)")
    description: Optional[str] = Field(None, description="Descripción del permiso")


class PermissionCreate(PermissionBase):
    """Schema para crear permisos"""
    pass


class PermissionResponse(PermissionBase):
    """Schema de respuesta para permisos"""
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    """Schema base para roles"""
    name: str = Field(..., description="Nombre del rol")
    description: Optional[str] = Field(None, description="Descripción del rol")


class RoleCreate(RoleBase):
    """Schema para crear roles"""
    permission_ids: Optional[List[int]] = Field(default=[], description="IDs de permisos a asignar")


class RoleUpdate(BaseModel):
    """Schema para actualizar roles"""
    name: Optional[str] = Field(None, description="Nombre del rol")
    description: Optional[str] = Field(None, description="Descripción del rol")
    permission_ids: Optional[List[int]] = Field(None, description="IDs de permisos a asignar")
    is_active: Optional[bool] = Field(None, description="Estado del rol")


class RoleResponse(RoleBase):
    """Schema de respuesta para roles"""
    id: int
    is_active: bool
    permissions: List[PermissionResponse] = []
    
    class Config:
        from_attributes = True


class RoleSummary(BaseModel):
    """Schema resumido para roles"""
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    permissions_count: int = 0
    
    class Config:
        from_attributes = True


class UserPermissionsResponse(BaseModel):
    """Schema para respuesta de permisos de usuario"""
    user_id: int
    username: str
    role_id: Optional[int]
    role_name: Optional[str]
    permissions: List[PermissionResponse]
    total_permissions: int
