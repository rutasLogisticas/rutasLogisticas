"""
Schemas simples para clientes
"""
from typing import Optional
from pydantic import BaseModel


class ClientCreate(BaseModel):
    """Schema para crear clientes"""
    name: str
    email: str
    phone: str
    company: Optional[str] = None
    client_type: str = "individual"
    status: str = "activo"
    is_active: bool = True


class ClientUpdate(BaseModel):
    """Schema para actualizar clientes"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    client_type: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class ClientResponse(BaseModel):
    """Schema para respuesta de clientes"""
    id: int
    name: str
    email: str
    phone: str
    company: Optional[str]
    client_type: str
    status: str
    is_active: bool
    
    model_config = {"from_attributes": True}


class ClientSummary(BaseModel):
    """Schema para resumen de clientes"""
    id: int
    name: str
    email: str
    phone: str
    company: Optional[str]
    client_type: str
    status: str
    is_active: bool
    
    model_config = {"from_attributes": True}