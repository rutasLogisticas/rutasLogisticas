"""
Esquemas de Pedidos para el sistema de rutas logísticas

Este módulo define los esquemas Pydantic para validación y serialización
de datos relacionados con pedidos.
"""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, model_validator


class OrderBase(BaseModel):
    """Esquema base para pedidos"""
    origin_address: str = Field(..., min_length=5, max_length=300, description="Dirección de origen")
    destination_address: str = Field(..., min_length=5, max_length=300, description="Dirección de destino")
    origin_city: str = Field(..., min_length=2, max_length=100, description="Ciudad de origen")
    destination_city: str = Field(..., min_length=2, max_length=100, description="Ciudad de destino")
    description: str = Field(..., min_length=10, max_length=1000, description="Descripción del pedido")
    weight: Optional[float] = Field(None, ge=0, le=10000, description="Peso en kg (0-10,000)")
    volume: Optional[float] = Field(None, ge=0, le=1000, description="Volumen en m³ (0-1,000)")
    value: Optional[Decimal] = Field(None, ge=0, le=10000000, description="Valor del pedido (0-10,000,000)")
    priority: str = Field("media", description="Prioridad del pedido")
    delivery_date: Optional[datetime] = Field(None, description="Fecha programada de entrega")
    notes: Optional[str] = Field(None, max_length=500, description="Notas adicionales")


class OrderCreate(OrderBase):
    """Esquema para crear un pedido"""
    client_id: int = Field(..., gt=0, description="ID del cliente")
    driver_id: Optional[int] = Field(None, gt=0, description="ID del conductor")
    vehicle_id: Optional[int] = Field(None, gt=0, description="ID del vehículo")

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        valid_priorities = ['baja', 'media', 'alta', 'urgente']
        if v not in valid_priorities:
            raise ValueError(f'La prioridad debe ser una de: {", ".join(valid_priorities)}')
        return v

    @field_validator('origin_address', 'destination_address')
    @classmethod
    def validate_addresses(cls, v):
        if v.strip() != v:
            raise ValueError('Las direcciones no pueden tener espacios al inicio o final')
        return v.strip()

    @model_validator(mode='after')
    def validate_different_addresses(self):
        if self.origin_address.lower() == self.destination_address.lower():
            raise ValueError('La dirección de origen y destino deben ser diferentes')
        return self


class OrderUpdate(BaseModel):
    """Esquema para actualizar un pedido"""
    driver_id: Optional[int] = Field(None, description="ID del conductor")
    vehicle_id: Optional[int] = Field(None, description="ID del vehículo")
    origin_address: Optional[str] = Field(None, min_length=1, max_length=300, description="Dirección de origen")
    destination_address: Optional[str] = Field(None, min_length=1, max_length=300, description="Dirección de destino")
    origin_city: Optional[str] = Field(None, min_length=1, max_length=100, description="Ciudad de origen")
    destination_city: Optional[str] = Field(None, min_length=1, max_length=100, description="Ciudad de destino")
    description: Optional[str] = Field(None, min_length=1, description="Descripción del pedido")
    weight: Optional[float] = Field(None, ge=0, description="Peso en kg")
    volume: Optional[float] = Field(None, ge=0, description="Volumen en m³")
    value: Optional[Decimal] = Field(None, ge=0, description="Valor del pedido")
    priority: Optional[str] = Field(None, description="Prioridad del pedido")
    delivery_date: Optional[datetime] = Field(None, description="Fecha programada de entrega")
    notes: Optional[str] = Field(None, description="Notas adicionales")


class OrderResponse(OrderBase):
    """Esquema de respuesta para pedidos"""
    id: int
    order_number: str
    client_id: int
    driver_id: Optional[int]
    vehicle_id: Optional[int]
    status: str
    tracking_code: Optional[str]
    delivered_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class OrderSummary(BaseModel):
    """Esquema resumido para pedidos"""
    id: int
    order_number: str
    client_id: int
    driver_id: Optional[int]
    vehicle_id: Optional[int]
    origin_city: str
    destination_city: str
    status: str
    priority: str
    delivery_date: Optional[datetime]
    delivered_date: Optional[datetime]
    tracking_code: Optional[str]

    class Config:
        from_attributes = True


class OrderWithDetails(OrderResponse):
    """Esquema de pedido con detalles completos"""
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    vehicle_license_plate: Optional[str] = None
    vehicle_brand: Optional[str] = None
    vehicle_model: Optional[str] = None


class OrderAssignment(BaseModel):
    """Esquema para asignar conductor y vehículo a un pedido"""
    driver_id: int = Field(..., description="ID del conductor")
    vehicle_id: int = Field(..., description="ID del vehículo")
    tracking_code: Optional[str] = Field(None, description="Código de seguimiento personalizado")


class OrderRouteResponse(BaseModel):
    """Esquema que combina información del pedido con la ruta calculada"""
    order: OrderWithDetails
    route: dict = Field(..., description="Información de la ruta calculada")
    estimated_delivery_time: Optional[datetime] = Field(None, description="Tiempo estimado de entrega")
    route_distance: Optional[str] = Field(None, description="Distancia total de la ruta")
    route_duration: Optional[str] = Field(None, description="Duración estimada de la ruta")
    polyline: Optional[str] = Field(None, description="Polyline para mostrar en el mapa")


class MultipleOrderRoutesRequest(BaseModel):
    """Esquema para solicitar rutas de múltiples pedidos"""
    order_ids: List[int] = Field(..., min_items=1, max_items=10, description="Lista de IDs de pedidos")
    mode: Optional[str] = Field("driving", description="Modo de transporte: driving, walking, bicycling, transit")