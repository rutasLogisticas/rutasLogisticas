"""
Schemas simples para vehículos
"""
from typing import Optional
from pydantic import BaseModel


class VehicleCreate(BaseModel):
    """Schema para crear vehículos"""
    license_plate: str
    brand: str
    model: str
    year: int
    vehicle_type: str
    status: str = "disponible"


class VehicleResponse(BaseModel):
    """Schema para respuesta de vehículos"""
    id: int
    license_plate: str
    brand: str
    model: str
    year: int
    vehicle_type: str
    status: str
    is_available: bool
    
    model_config = {"from_attributes": True}


class VehicleSummary(BaseModel):
    """Schema para resumen de vehículos"""
    id: int
    license_plate: str
    brand: str
    model: str
    vehicle_type: str
    status: str
    
    model_config = {"from_attributes": True}