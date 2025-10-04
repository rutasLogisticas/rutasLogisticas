"""
Esquemas para vehículos
Implementa validaciones específicas para vehículos
"""
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

from app.models.vehicle import VehicleType, VehicleStatus
from .base_schemas import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema


class VehicleCreate(BaseCreateSchema):
    """Esquema para crear vehículos"""
    license_plate: str = Field(..., min_length=1, max_length=20, description="Placa del vehículo")
    brand: str = Field(..., min_length=1, max_length=100, description="Marca del vehículo")
    model: str = Field(..., min_length=1, max_length=100, description="Modelo del vehículo")
    year: int = Field(..., ge=1900, le=2030, description="Año del vehículo")
    color: Optional[str] = Field(None, max_length=50, description="Color del vehículo")
    vehicle_type: VehicleType = Field(..., description="Tipo de vehículo")
    capacity_weight: Optional[float] = Field(None, gt=0, description="Capacidad de peso en kg")
    capacity_volume: Optional[float] = Field(None, gt=0, description="Capacidad de volumen en m³")
    fuel_type: Optional[str] = Field(None, max_length=50, description="Tipo de combustible")
    fuel_consumption: Optional[float] = Field(None, gt=0, description="Consumo en L/100km")
    last_maintenance: Optional[str] = Field(None, max_length=50, description="Último mantenimiento")
    next_maintenance: Optional[str] = Field(None, max_length=50, description="Próximo mantenimiento")
    insurance_expiry: Optional[str] = Field(None, max_length=50, description="Vencimiento del seguro")
    notes: Optional[str] = Field(None, description="Notas adicionales")
    
    @validator('license_plate')
    def validate_license_plate(cls, v):
        """Valida formato de placa"""
        if not v.replace('-', '').replace(' ', '').isalnum():
            raise ValueError('La placa debe contener solo letras, números, guiones y espacios')
        return v.upper().strip()


class VehicleUpdate(BaseUpdateSchema):
    """Esquema para actualizar vehículos"""
    license_plate: Optional[str] = Field(None, min_length=1, max_length=20)
    brand: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2030)
    color: Optional[str] = Field(None, max_length=50)
    vehicle_type: Optional[VehicleType] = None
    status: Optional[VehicleStatus] = None
    capacity_weight: Optional[float] = Field(None, gt=0)
    capacity_volume: Optional[float] = Field(None, gt=0)
    fuel_type: Optional[str] = Field(None, max_length=50)
    fuel_consumption: Optional[float] = Field(None, gt=0)
    last_maintenance: Optional[str] = Field(None, max_length=50)
    next_maintenance: Optional[str] = Field(None, max_length=50)
    insurance_expiry: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    is_available: Optional[bool] = None
    
    @validator('license_plate')
    def validate_license_plate(cls, v):
        """Valida formato de placa"""
        if v is not None:
            if not v.replace('-', '').replace(' ', '').isalnum():
                raise ValueError('La placa debe contener solo letras, números, guiones y espacios')
            return v.upper().strip()
        return v


class VehicleResponse(BaseResponseSchema):
    """Esquema para respuestas de vehículos"""
    license_plate: str
    brand: str
    model: str
    year: int
    color: Optional[str]
    vehicle_type: VehicleType
    status: VehicleStatus
    capacity_weight: Optional[float]
    capacity_volume: Optional[float]
    fuel_type: Optional[str]
    fuel_consumption: Optional[float]
    last_maintenance: Optional[str]
    next_maintenance: Optional[str]
    insurance_expiry: Optional[str]
    notes: Optional[str]
    is_available: bool


class VehicleSummary(BaseModel):
    """Esquema para resumen de vehículos"""
    id: int
    license_plate: str
    brand: str
    model: str
    year: int
    vehicle_type: VehicleType
    status: VehicleStatus
    is_available: bool
    created_at: datetime


class VehicleStatusUpdate(BaseModel):
    """Esquema para actualizar estado de vehículo"""
    status: VehicleStatus = Field(..., description="Nuevo estado del vehículo")


class VehicleAvailabilityUpdate(BaseModel):
    """Esquema para actualizar disponibilidad de vehículo"""
    is_available: bool = Field(..., description="Disponibilidad del vehículo")


class VehicleCapacityFilter(BaseModel):
    """Esquema para filtrar vehículos por capacidad"""
    min_weight: Optional[float] = Field(None, gt=0, description="Peso mínimo requerido en kg")
    min_volume: Optional[float] = Field(None, gt=0, description="Volumen mínimo requerido en m³")
    vehicle_type: Optional[VehicleType] = Field(None, description="Tipo de vehículo")
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)
