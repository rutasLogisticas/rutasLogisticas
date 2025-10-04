"""
Esquemas para direcciones
Implementa validaciones específicas para direcciones
"""
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

from app.models.address import AddressType
from .base_schemas import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema


class AddressCreate(BaseCreateSchema):
    """Esquema para crear direcciones"""
    client_id: int = Field(..., description="ID del cliente")
    address_type: AddressType = Field(default=AddressType.DOMICILIO, description="Tipo de dirección")
    address_line1: str = Field(..., min_length=1, max_length=255, description="Dirección principal")
    address_line2: Optional[str] = Field(None, max_length=255, description="Dirección secundaria")
    neighborhood: Optional[str] = Field(None, max_length=100, description="Barrio")
    city: str = Field(..., min_length=1, max_length=100, description="Ciudad")
    state: str = Field(..., min_length=1, max_length=100, description="Estado/Provincia")
    country: str = Field(default="Ecuador", max_length=100, description="País")
    postal_code: Optional[str] = Field(None, max_length=20, description="Código postal")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitud")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitud")
    reference_points: Optional[str] = Field(None, description="Puntos de referencia")
    delivery_instructions: Optional[str] = Field(None, description="Instrucciones de entrega")
    contact_name: Optional[str] = Field(None, max_length=255, description="Persona de contacto")
    contact_phone: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    access_notes: Optional[str] = Field(None, description="Notas sobre acceso")
    parking_available: bool = Field(default=True, description="Estacionamiento disponible")
    delivery_time_preference: Optional[str] = Field(None, max_length=100, description="Horario preferido")
    is_primary: bool = Field(default=False, description="Dirección principal")
    is_delivery_available: bool = Field(default=True, description="Disponible para entregas")
    
    @validator('latitude', 'longitude')
    def validate_coordinates(cls, v, values):
        """Valida coordenadas geográficas"""
        if v is not None:
            if 'latitude' in values and 'longitude' in values:
                lat = values.get('latitude')
                lng = values.get('longitude')
                if lat is not None and lng is not None:
                    # Validación adicional de coordenadas para Ecuador
                    if lat < -5 or lat > 2 or lng < -92 or lng > -75:
                        raise ValueError('Las coordenadas no están dentro del rango de Ecuador')
        return v


class AddressUpdate(BaseUpdateSchema):
    """Esquema para actualizar direcciones"""
    address_type: Optional[AddressType] = None
    address_line1: Optional[str] = Field(None, min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    neighborhood: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    reference_points: Optional[str] = None
    delivery_instructions: Optional[str] = None
    contact_name: Optional[str] = Field(None, max_length=255)
    contact_phone: Optional[str] = Field(None, max_length=20)
    access_notes: Optional[str] = None
    parking_available: Optional[bool] = None
    delivery_time_preference: Optional[str] = Field(None, max_length=100)
    is_primary: Optional[bool] = None
    is_delivery_available: Optional[bool] = None
    
    @validator('latitude', 'longitude')
    def validate_coordinates(cls, v, values):
        """Valida coordenadas geográficas"""
        if v is not None:
            # Validación adicional de coordenadas para Ecuador
            if 'latitude' in values and 'longitude' in values:
                lat = values.get('latitude')
                lng = values.get('longitude')
                if lat is not None and lng is not None:
                    if lat < -5 or lat > 2 or lng < -92 or lng > -75:
                        raise ValueError('Las coordenadas no están dentro del rango de Ecuador')
        return v


class AddressResponse(BaseResponseSchema):
    """Esquema para respuestas de direcciones"""
    client_id: int
    address_type: AddressType
    address_line1: str
    address_line2: Optional[str]
    neighborhood: Optional[str]
    city: str
    state: str
    country: str
    postal_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    reference_points: Optional[str]
    delivery_instructions: Optional[str]
    contact_name: Optional[str]
    contact_phone: Optional[str]
    access_notes: Optional[str]
    parking_available: bool
    delivery_time_preference: Optional[str]
    is_primary: bool
    is_delivery_available: bool


class AddressSummary(BaseModel):
    """Esquema para resumen de direcciones"""
    id: int
    client_id: int
    address_type: AddressType
    short_address: str
    city: str
    is_primary: bool
    is_delivery_available: bool
    contact_phone: Optional[str]
    created_at: datetime


class AddressPrimaryUpdate(BaseModel):
    """Esquema para establecer dirección como principal"""
    address_id: int = Field(..., description="ID de la dirección a establecer como principal")


class AddressDeliveryUpdate(BaseModel):
    """Esquema para actualizar disponibilidad de entrega"""
    is_delivery_available: bool = Field(..., description="Disponibilidad para entregas")


class AddressCoordinatesUpdate(BaseModel):
    """Esquema para actualizar coordenadas"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitud")
    longitude: float = Field(..., ge=-180, le=180, description="Longitud")


class AddressFilter(BaseModel):
    """Esquema para filtrar direcciones"""
    client_id: Optional[int] = Field(None, description="ID del cliente")
    address_type: Optional[AddressType] = Field(None, description="Tipo de dirección")
    city: Optional[str] = Field(None, description="Ciudad")
    state: Optional[str] = Field(None, description="Estado/Provincia")
    is_primary: Optional[bool] = Field(None, description="Dirección principal")
    is_delivery_available: Optional[bool] = Field(None, description="Disponible para entregas")
    has_coordinates: Optional[bool] = Field(None, description="Tiene coordenadas")
    parking_available: Optional[bool] = Field(None, description="Tiene estacionamiento")
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)
