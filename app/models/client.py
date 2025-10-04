"""
Modelo de Cliente
Implementa principio SRP y encapsula lógica de negocio específica
"""
from sqlalchemy import Column, String, Integer, Boolean, Text, Enum, Float
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel


class ClientType(enum.Enum):
    """Tipos de cliente"""
    PERSONA_NATURAL = "persona_natural"
    EMPRESA = "empresa"
    ORGANIZACION = "organizacion"


class ClientStatus(enum.Enum):
    """Estados del cliente"""
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"
    POTENCIAL = "potencial"


class Client(BaseModel):
    """
    Modelo de Cliente para gestión de personas y empresas
    Implementa principio SRP - una sola responsabilidad
    """
    __tablename__ = "clients"
    
    # Información básica
    name = Column(String(255), nullable=False, index=True)
    client_type = Column(Enum(ClientType), nullable=False)
    status = Column(Enum(ClientStatus), default=ClientStatus.ACTIVO, nullable=False)
    
    # Información de contacto
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    secondary_phone = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Información fiscal (para empresas)
    tax_id = Column(String(50), nullable=True, index=True, comment="RUC, NIT, etc.")
    business_name = Column(String(255), nullable=True, comment="Razón social")
    
    # Información de ubicación principal
    main_address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True, default="Ecuador")
    postal_code = Column(String(20), nullable=True)
    
    # Información de contacto comercial
    contact_person = Column(String(255), nullable=True)
    contact_position = Column(String(100), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    
    # Información comercial
    credit_limit = Column(Float, nullable=True, default=0.0, comment="Límite de crédito en USD")
    payment_terms = Column(Integer, nullable=True, default=30, comment="Términos de pago en días")
    discount_percentage = Column(Float, nullable=True, default=0.0, comment="Descuento por defecto")
    
    # Información adicional
    notes = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True, comment="Notas internas no visibles para el cliente")
    tags = Column(String(500), nullable=True, comment="Tags separados por comas")
    
    # Configuraciones
    receives_notifications = Column(Boolean, default=True, nullable=False)
    is_priority = Column(Boolean, default=False, nullable=False)
    
    # Relaciones
    addresses = relationship("Address", back_populates="client", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Client(name='{self.name}', type='{self.client_type.value}')>"
    
    @property
    def primary_contact(self) -> str:
        """Retorna el contacto principal"""
        if self.contact_person:
            return self.contact_person
        return self.name
    
    @property
    def primary_email(self) -> str:
        """Retorna el email principal"""
        if self.contact_email:
            return self.contact_email
        return self.email
    
    @property
    def primary_phone(self) -> str:
        """Retorna el teléfono principal"""
        if self.contact_phone:
            return self.contact_phone
        return self.phone
    
    def is_active_client(self) -> bool:
        """Verifica si el cliente está activo"""
        return (
            self.status == ClientStatus.ACTIVO and 
            self.is_active
        )
    
    def get_main_address_info(self) -> dict:
        """Retorna información de la dirección principal"""
        return {
            'address': self.main_address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code
        }
    
    def get_contact_info(self) -> dict:
        """Retorna información completa de contacto"""
        return {
            'primary_contact': self.primary_contact,
            'email': self.primary_email,
            'phone': self.primary_phone,
            'secondary_phone': self.secondary_phone,
            'website': self.website,
            'contact_person': self.contact_person,
            'contact_position': self.contact_position,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone
        }
    
    def get_commercial_info(self) -> dict:
        """Retorna información comercial"""
        return {
            'credit_limit': self.credit_limit,
            'payment_terms': self.payment_terms,
            'discount_percentage': self.discount_percentage,
            'tax_id': self.tax_id,
            'business_name': self.business_name
        }
    
    def to_summary_dict(self) -> dict:
        """Retorna resumen del cliente para listados"""
        return {
            'id': self.id,
            'name': self.name,
            'client_type': self.client_type.value,
            'status': self.status.value,
            'email': self.primary_email,
            'phone': self.primary_phone,
            'city': self.city,
            'is_priority': self.is_priority,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
