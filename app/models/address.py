"""
Modelo de Dirección
Implementa principio SRP y encapsula lógica de negocio específica
"""
from sqlalchemy import Column, String, Integer, Boolean, Text, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel


class AddressType(enum.Enum):
    """Tipos de dirección"""
    DOMICILIO = "domicilio"
    OFICINA = "oficina"
    ALMACEN = "almacen"
    ENTREGA = "entrega"
    RECOGIDA = "recogida"
    FACTURACION = "facturacion"
    OTRO = "otro"


class Address(BaseModel):
    """
    Modelo de Dirección asociada a clientes
    Implementa principio SRP - una sola responsabilidad
    """
    __tablename__ = "addresses"
    
    # Relación con cliente
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    
    # Información de la dirección
    address_type = Column(Enum(AddressType), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    neighborhood = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False, default="Ecuador")
    postal_code = Column(String(20), nullable=True)
    
    # Coordenadas geográficas
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Información adicional
    reference_points = Column(Text, nullable=True, comment="Puntos de referencia")
    delivery_instructions = Column(Text, nullable=True, comment="Instrucciones de entrega")
    contact_name = Column(String(255), nullable=True, comment="Persona de contacto en esta dirección")
    contact_phone = Column(String(20), nullable=True, comment="Teléfono de contacto en esta dirección")
    
    # Configuraciones
    is_primary = Column(Boolean, default=False, nullable=False, comment="Dirección principal")
    is_active = Column(Boolean, default=True, nullable=False)
    is_delivery_available = Column(Boolean, default=True, nullable=False, comment="Disponible para entregas")
    
    # Información de acceso
    access_notes = Column(Text, nullable=True, comment="Notas sobre acceso al lugar")
    parking_available = Column(Boolean, default=True, nullable=False)
    delivery_time_preference = Column(String(100), nullable=True, comment="Horario preferido de entrega")
    
    # Relaciones
    client = relationship("Client", back_populates="addresses")
    
    def __repr__(self):
        return f"<Address(client_id={self.client_id}, type='{self.address_type.value}', city='{self.city}')>"
    
    @property
    def full_address(self) -> str:
        """Retorna la dirección completa formateada"""
        parts = [
            self.address_line1,
            self.address_line2,
            self.neighborhood,
            self.city,
            self.state,
            self.country
        ]
        return ", ".join([part for part in parts if part])
    
    @property
    def short_address(self) -> str:
        """Retorna dirección abreviada"""
        parts = [self.address_line1, self.city, self.state]
        return ", ".join([part for part in parts if part])
    
    def has_coordinates(self) -> bool:
        """Verifica si tiene coordenadas geográficas"""
        return self.latitude is not None and self.longitude is not None
    
    def get_coordinates(self) -> tuple:
        """Retorna coordenadas como tupla (lat, lng)"""
        return (self.latitude, self.longitude)
    
    def is_accessible_for_delivery(self) -> bool:
        """Verifica si es accesible para entregas"""
        return (
            self.is_active and 
            self.is_delivery_available and 
            self.is_active
        )
    
    def get_contact_info(self) -> dict:
        """Retorna información de contacto específica de la dirección"""
        return {
            'contact_name': self.contact_name,
            'contact_phone': self.contact_phone,
            'delivery_instructions': self.delivery_instructions,
            'delivery_time_preference': self.delivery_time_preference,
            'access_notes': self.access_notes,
            'parking_available': self.parking_available
        }
    
    def get_location_info(self) -> dict:
        """Retorna información de ubicación"""
        return {
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'neighborhood': self.neighborhood,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'reference_points': self.reference_points,
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            } if self.has_coordinates() else None
        }
    
    def to_summary_dict(self) -> dict:
        """Retorna resumen de la dirección para listados"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'address_type': self.address_type.value,
            'short_address': self.short_address,
            'city': self.city,
            'is_primary': self.is_primary,
            'is_delivery_available': self.is_delivery_available,
            'contact_phone': self.contact_phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
