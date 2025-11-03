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


class VehicleUpdate(BaseModel):
    """Schema para actualizar vehículos"""
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    vehicle_type: Optional[str] = None
    status: Optional[str] = None


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
    is_active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    model_config = {"from_attributes": True}


class VehicleSummary(BaseModel):
    """Schema para resumen de vehículos"""
    id: int
    license_plate: str
    brand: str
    model: str
    year: Optional[int] = None
    vehicle_type: str
    status: str
    is_available: bool
    
    model_config = {"from_attributes": True}