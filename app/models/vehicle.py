"""
Modelo de Vehículo
Implementa principio SRP y encapsula lógica de negocio específica
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, Enum
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel


class VehicleType(enum.Enum):
    """Tipos de vehículos disponibles"""
    CAMION = "camion"
    FURGON = "furgon"
    MOTOCICLETA = "motocicleta"
    BICICLETA = "bicicleta"
    CAMIONETA = "camioneta"


class VehicleStatus(enum.Enum):
    """Estados del vehículo"""
    DISPONIBLE = "disponible"
    EN_RUTA = "en_ruta"
    MANTENIMIENTO = "mantenimiento"
    FUERA_SERVICIO = "fuera_servicio"


class Vehicle(BaseModel):
    """
    Modelo de Vehículo para la flota logística
    Implementa principio SRP - una sola responsabilidad
    """
    __tablename__ = "vehicles"
    
    # Información básica
    license_plate = Column(String(20), unique=True, nullable=False, index=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String(50), nullable=True)
    
    # Clasificación
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.DISPONIBLE, nullable=False)
    
    # Especificaciones técnicas
    capacity_weight = Column(Float, nullable=True, comment="Capacidad en kilogramos")
    capacity_volume = Column(Float, nullable=True, comment="Capacidad en metros cúbicos")
    fuel_type = Column(String(50), nullable=True)
    fuel_consumption = Column(Float, nullable=True, comment="Consumo en L/100km")
    
    # Información de mantenimiento
    last_maintenance = Column(String(50), nullable=True)
    next_maintenance = Column(String(50), nullable=True)
    insurance_expiry = Column(String(50), nullable=True)
    
    # Información adicional
    notes = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    # routes = relationship("Route", back_populates="vehicle")  # TODO: Implementar cuando se cree el modelo Route
    
    def __repr__(self):
        return f"<Vehicle(license_plate='{self.license_plate}', type='{self.vehicle_type.value}')>"
    
    def is_operational(self) -> bool:
        """Verifica si el vehículo está operacional"""
        return (
            self.status == VehicleStatus.DISPONIBLE and 
            self.is_active and 
            self.is_available
        )
    
    def can_carry_weight(self, required_weight: float) -> bool:
        """Verifica si puede transportar el peso requerido"""
        if not self.capacity_weight:
            return False
        return required_weight <= self.capacity_weight
    
    def can_carry_volume(self, required_volume: float) -> bool:
        """Verifica si puede transportar el volumen requerido"""
        if not self.capacity_volume:
            return False
        return required_volume <= self.capacity_volume
    
    def get_maintenance_info(self) -> dict:
        """Retorna información de mantenimiento"""
        return {
            'last_maintenance': self.last_maintenance,
            'next_maintenance': self.next_maintenance,
            'insurance_expiry': self.insurance_expiry
        }
    
    def to_summary_dict(self) -> dict:
        """Retorna resumen del vehículo para listados"""
        return {
            'id': self.id,
            'license_plate': self.license_plate,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'vehicle_type': self.vehicle_type.value,
            'status': self.status.value,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
