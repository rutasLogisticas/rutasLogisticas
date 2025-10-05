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
    client_type: str
    status: str
    
    model_config = {"from_attributes": True}