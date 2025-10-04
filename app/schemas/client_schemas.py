"""
Esquemas para clientes
Implementa validaciones específicas para clientes
"""
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

from app.models.client import ClientType, ClientStatus
from .base_schemas import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema


class ClientCreate(BaseCreateSchema):
    """Esquema para crear clientes"""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre del cliente")
    client_type: ClientType = Field(..., description="Tipo de cliente")
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$', description="Email")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono")
    secondary_phone: Optional[str] = Field(None, max_length=20, description="Teléfono secundario")
    website: Optional[str] = Field(None, max_length=255, description="Sitio web")
    tax_id: Optional[str] = Field(None, max_length=50, description="ID fiscal (RUC, NIT, etc.)")
    business_name: Optional[str] = Field(None, max_length=255, description="Razón social")
    main_address: Optional[str] = Field(None, description="Dirección principal")
    city: Optional[str] = Field(None, max_length=100, description="Ciudad")
    state: Optional[str] = Field(None, max_length=100, description="Estado/Provincia")
    country: str = Field(default="Ecuador", max_length=100, description="País")
    postal_code: Optional[str] = Field(None, max_length=20, description="Código postal")
    contact_person: Optional[str] = Field(None, max_length=255, description="Persona de contacto")
    contact_position: Optional[str] = Field(None, max_length=100, description="Cargo del contacto")
    contact_email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$', description="Email del contacto")
    contact_phone: Optional[str] = Field(None, max_length=20, description="Teléfono del contacto")
    credit_limit: Optional[float] = Field(None, ge=0, description="Límite de crédito en USD")
    payment_terms: Optional[int] = Field(None, ge=0, description="Términos de pago en días")
    discount_percentage: Optional[float] = Field(None, ge=0, le=100, description="Descuento por defecto")
    notes: Optional[str] = Field(None, description="Notas")
    internal_notes: Optional[str] = Field(None, description="Notas internas")
    tags: Optional[str] = Field(None, max_length=500, description="Tags separados por comas")
    receives_notifications: bool = Field(default=True, description="Recibe notificaciones")
    is_priority: bool = Field(default=False, description="Cliente prioritario")
    
    @validator('email', 'contact_email')
    def validate_emails(cls, v):
        """Valida formato de emails"""
        if v is not None:
            return v.lower().strip()
        return v
    
    @validator('website')
    def validate_website(cls, v):
        """Valida formato de sitio web"""
        if v is not None and not v.startswith(('http://', 'https://')):
            v = f'https://{v}'
        return v


class ClientUpdate(BaseUpdateSchema):
    """Esquema para actualizar clientes"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    client_type: Optional[ClientType] = None
    status: Optional[ClientStatus] = None
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, max_length=20)
    secondary_phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=255)
    tax_id: Optional[str] = Field(None, max_length=50)
    business_name: Optional[str] = Field(None, max_length=255)
    main_address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    contact_person: Optional[str] = Field(None, max_length=255)
    contact_position: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    contact_phone: Optional[str] = Field(None, max_length=20)
    credit_limit: Optional[float] = Field(None, ge=0)
    payment_terms: Optional[int] = Field(None, ge=0)
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    notes: Optional[str] = None
    internal_notes: Optional[str] = None
    tags: Optional[str] = Field(None, max_length=500)
    receives_notifications: Optional[bool] = None
    is_priority: Optional[bool] = None
    
    @validator('email', 'contact_email')
    def validate_emails(cls, v):
        """Valida formato de emails"""
        if v is not None:
            return v.lower().strip()
        return v
    
    @validator('website')
    def validate_website(cls, v):
        """Valida formato de sitio web"""
        if v is not None and not v.startswith(('http://', 'https://')):
            v = f'https://{v}'
        return v


class ClientResponse(BaseResponseSchema):
    """Esquema para respuestas de clientes"""
    name: str
    client_type: ClientType
    status: ClientStatus
    email: Optional[str]
    phone: Optional[str]
    secondary_phone: Optional[str]
    website: Optional[str]
    tax_id: Optional[str]
    business_name: Optional[str]
    main_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: str
    postal_code: Optional[str]
    contact_person: Optional[str]
    contact_position: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    credit_limit: Optional[float]
    payment_terms: Optional[int]
    discount_percentage: Optional[float]
    notes: Optional[str]
    internal_notes: Optional[str]
    tags: Optional[str]
    receives_notifications: bool
    is_priority: bool


class ClientSummary(BaseModel):
    """Esquema para resumen de clientes"""
    id: int
    name: str
    client_type: ClientType
    status: ClientStatus
    email: Optional[str]
    phone: Optional[str]
    city: Optional[str]
    is_priority: bool
    created_at: datetime


class ClientStatusUpdate(BaseModel):
    """Esquema para actualizar estado de cliente"""
    status: ClientStatus = Field(..., description="Nuevo estado del cliente")


class ClientPriorityUpdate(BaseModel):
    """Esquema para actualizar prioridad de cliente"""
    is_priority: bool = Field(..., description="Prioridad del cliente")


class ClientNotificationUpdate(BaseModel):
    """Esquema para actualizar notificaciones de cliente"""
    receives_notifications: bool = Field(..., description="Recibe notificaciones")


class ClientCommercialUpdate(BaseModel):
    """Esquema para actualizar información comercial del cliente"""
    credit_limit: Optional[float] = Field(None, ge=0, description="Límite de crédito")
    payment_terms: Optional[int] = Field(None, ge=0, description="Términos de pago")
    discount_percentage: Optional[float] = Field(None, ge=0, le=100, description="Descuento")


class ClientFilter(BaseModel):
    """Esquema para filtrar clientes"""
    client_type: Optional[ClientType] = Field(None, description="Tipo de cliente")
    status: Optional[ClientStatus] = Field(None, description="Estado del cliente")
    city: Optional[str] = Field(None, description="Ciudad")
    state: Optional[str] = Field(None, description="Estado/Provincia")
    is_priority: Optional[bool] = Field(None, description="Cliente prioritario")
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)
