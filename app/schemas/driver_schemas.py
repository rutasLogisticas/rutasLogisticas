"""
Schemas simples para conductores
"""
from typing import Optional
from pydantic import BaseModel


class DriverCreate(BaseModel):
    """Schema para crear conductores"""
    first_name: str
    last_name: str
    email: str
    phone: str
    document_number: str
    license_type: str
    status: str = "disponible"


class DriverUpdate(BaseModel):
    """Schema para actualizar conductores"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    license_type: Optional[str] = None
    status: Optional[str] = None


class DriverResponse(BaseModel):
    """Schema para respuesta de conductores"""
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    document_number: str
    license_type: str
    status: str
    is_available: bool
    
    model_config = {"from_attributes": True}


class DriverSummary(BaseModel):
    """Schema para resumen de conductores"""
    id: int
    first_name: str
    last_name: str
    email: str
    license_type: str
    status: str
    
    model_config = {"from_attributes": True}