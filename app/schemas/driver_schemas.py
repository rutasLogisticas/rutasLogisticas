"""
Esquemas para conductores
Implementa validaciones específicas para conductores
"""
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime, date

from app.models.driver import DriverStatus, LicenseType
from .base_schemas import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema


class DriverCreate(BaseCreateSchema):
    """Esquema para crear conductores"""
    first_name: str = Field(..., min_length=1, max_length=100, description="Nombre")
    last_name: str = Field(..., min_length=1, max_length=100, description="Apellido")
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$', description="Email único")
    phone: str = Field(..., min_length=1, max_length=20, description="Teléfono")
    address: Optional[str] = Field(None, description="Dirección")
    document_type: str = Field(default="DNI", max_length=20, description="Tipo de documento")
    document_number: str = Field(..., min_length=1, max_length=20, description="Número de documento")
    birth_date: Optional[date] = Field(None, description="Fecha de nacimiento")
    employee_id: Optional[str] = Field(None, max_length=50, description="ID de empleado")
    hire_date: Optional[date] = Field(None, description="Fecha de contratación")
    salary: Optional[int] = Field(None, ge=0, description="Salario en centavos")
    license_type: LicenseType = Field(..., description="Tipo de licencia")
    license_number: str = Field(..., min_length=1, max_length=50, description="Número de licencia")
    license_expiry: date = Field(..., description="Fecha de vencimiento de licencia")
    emergency_contact_name: Optional[str] = Field(None, max_length=100, description="Contacto de emergencia")
    emergency_contact_phone: Optional[str] = Field(None, max_length=20, description="Teléfono de emergencia")
    notes: Optional[str] = Field(None, description="Notas adicionales")
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        """Valida fecha de nacimiento"""
        if v is not None:
            age = (date.today() - v).days // 365
            if age < 18:
                raise ValueError('El conductor debe ser mayor de 18 años')
            if age > 70:
                raise ValueError('El conductor debe ser menor de 70 años')
        return v
    
    @validator('license_expiry')
    def validate_license_expiry(cls, v):
        """Valida fecha de vencimiento de licencia"""
        if v < date.today():
            raise ValueError('La licencia no puede estar expirada')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        """Valida formato de email"""
        return v.lower().strip()


class DriverUpdate(BaseUpdateSchema):
    """Esquema para actualizar conductores"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    address: Optional[str] = None
    document_type: Optional[str] = Field(None, max_length=20)
    document_number: Optional[str] = Field(None, min_length=1, max_length=20)
    birth_date: Optional[date] = None
    employee_id: Optional[str] = Field(None, max_length=50)
    hire_date: Optional[date] = None
    salary: Optional[int] = Field(None, ge=0)
    status: Optional[DriverStatus] = None
    license_type: Optional[LicenseType] = None
    license_number: Optional[str] = Field(None, min_length=1, max_length=50)
    license_expiry: Optional[date] = None
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None
    is_available: Optional[bool] = None
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        """Valida fecha de nacimiento"""
        if v is not None:
            age = (date.today() - v).days // 365
            if age < 18:
                raise ValueError('El conductor debe ser mayor de 18 años')
            if age > 70:
                raise ValueError('El conductor debe ser menor de 70 años')
        return v
    
    @validator('license_expiry')
    def validate_license_expiry(cls, v):
        """Valida fecha de vencimiento de licencia"""
        if v is not None and v < date.today():
            raise ValueError('La licencia no puede estar expirada')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        """Valida formato de email"""
        if v is not None:
            return v.lower().strip()
        return v


class DriverResponse(BaseResponseSchema):
    """Esquema para respuestas de conductores"""
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Optional[str]
    document_type: str
    document_number: str
    birth_date: Optional[date]
    employee_id: Optional[str]
    hire_date: Optional[date]
    salary: Optional[int]
    status: DriverStatus
    license_type: LicenseType
    license_number: str
    license_expiry: date
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    notes: Optional[str]
    is_available: bool


class DriverSummary(BaseModel):
    """Esquema para resumen de conductores"""
    id: int
    full_name: str
    email: str
    phone: str
    document_number: str
    license_type: LicenseType
    license_number: str
    status: DriverStatus
    is_available: bool
    is_license_valid: bool
    created_at: datetime


class DriverStatusUpdate(BaseModel):
    """Esquema para actualizar estado de conductor"""
    status: DriverStatus = Field(..., description="Nuevo estado del conductor")


class DriverAvailabilityUpdate(BaseModel):
    """Esquema para actualizar disponibilidad de conductor"""
    is_available: bool = Field(..., description="Disponibilidad del conductor")


class DriverLicenseFilter(BaseModel):
    """Esquema para filtrar conductores por licencia"""
    license_type: Optional[LicenseType] = Field(None, description="Tipo de licencia")
    status: Optional[DriverStatus] = Field(None, description="Estado del conductor")
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)


class DriverAgeFilter(BaseModel):
    """Esquema para filtrar conductores por edad"""
    min_age: Optional[int] = Field(None, ge=18, le=70, description="Edad mínima")
    max_age: Optional[int] = Field(None, ge=18, le=70, description="Edad máxima")
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)
