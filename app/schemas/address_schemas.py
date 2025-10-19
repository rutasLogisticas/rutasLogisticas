"""
Schemas simples para direcciones
"""
from typing import Optional
from pydantic import BaseModel


class AddressCreate(BaseModel):
    """Schema para crear direcciones"""
    client_id: int
    street: str
    city: str
    state: str
    postal_code: str
    country: str = "Colombia"
    address_type: str = "principal"
    is_primary: bool = False


class AddressUpdate(BaseModel):
    """Schema para actualizar direcciones"""
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    address_type: Optional[str] = None
    is_primary: Optional[bool] = None


class AddressResponse(BaseModel):
    """Schema para respuesta de direcciones"""
    id: int
    client_id: int
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    address_type: str
    is_primary: bool
    
    model_config = {"from_attributes": True}


class AddressSummary(BaseModel):
    """Schema para resumen de direcciones"""
    id: int
    client_id: int
    street: str
    city: str
    state: str
    address_type: str
    
    model_config = {"from_attributes": True}