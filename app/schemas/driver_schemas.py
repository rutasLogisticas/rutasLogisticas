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