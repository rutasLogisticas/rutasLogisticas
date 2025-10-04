"""
Modelo de Conductor
Implementa principio SRP y encapsula lógica de negocio específica
"""
from sqlalchemy import Column, String, Integer, Date, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import date

from .base import BaseModel


class DriverStatus(enum.Enum):
    """Estados del conductor"""
    DISPONIBLE = "disponible"
    EN_RUTA = "en_ruta"
    DESCANSANDO = "descansando"
    VACACIONES = "vacaciones"
    FUERA_SERVICIO = "fuera_servicio"


class LicenseType(enum.Enum):
    """Tipos de licencia de conducir"""
    A = "A"  # Motocicletas
    B = "B"  # Vehículos livianos
    C = "C"  # Vehículos pesados
    D = "D"  # Transporte público
    E = "E"  # Remolques


class Driver(BaseModel):
    """
    Modelo de Conductor para la gestión de choferes
    Implementa principio SRP - una sola responsabilidad
    """
    __tablename__ = "drivers"
    
    # Información personal
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=True)
    
    # Información de identificación
    document_type = Column(String(20), nullable=False, default="DNI")
    document_number = Column(String(20), unique=True, nullable=False, index=True)
    birth_date = Column(Date, nullable=True)
    
    # Información laboral
    employee_id = Column(String(50), unique=True, nullable=True, index=True)
    hire_date = Column(Date, nullable=True)
    salary = Column(Integer, nullable=True, comment="Salario en centavos")
    status = Column(Enum(DriverStatus), default=DriverStatus.DISPONIBLE, nullable=False)
    
    # Información de licencia
    license_type = Column(Enum(LicenseType), nullable=False)
    license_number = Column(String(50), unique=True, nullable=False, index=True)
    license_expiry = Column(Date, nullable=False)
    
    # Información adicional
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    # routes = relationship("Route", back_populates="driver")  # TODO: Implementar cuando se cree el modelo Route
    
    def __repr__(self):
        return f"<Driver(name='{self.full_name}', license='{self.license_number}')>"
    
    @property
    def full_name(self) -> str:
        """Retorna el nombre completo del conductor"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        """Calcula la edad del conductor"""
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def is_license_valid(self) -> bool:
        """Verifica si la licencia está vigente"""
        if not self.license_expiry:
            return False
        return self.license_expiry >= date.today()
    
    def is_operational(self) -> bool:
        """Verifica si el conductor está operacional"""
        return (
            self.status == DriverStatus.DISPONIBLE and 
            self.is_active and 
            self.is_available and
            self.is_license_valid()
        )
    
    def can_drive_vehicle_type(self, vehicle_type) -> bool:
        """Verifica si puede conducir un tipo específico de vehículo"""
        license_mapping = {
            LicenseType.A: ['motocicleta', 'bicicleta'],
            LicenseType.B: ['camioneta', 'furgon'],
            LicenseType.C: ['camion'],
            LicenseType.D: ['camion', 'furgon', 'camioneta'],
            LicenseType.E: ['camion', 'furgon']
        }
        
        allowed_types = license_mapping.get(self.license_type, [])
        return vehicle_type in allowed_types
    
    def get_contact_info(self) -> dict:
        """Retorna información de contacto"""
        return {
            'email': self.email,
            'phone': self.phone,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone
        }
    
    def to_summary_dict(self) -> dict:
        """Retorna resumen del conductor para listados"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'document_number': self.document_number,
            'license_type': self.license_type.value,
            'license_number': self.license_number,
            'status': self.status.value,
            'is_available': self.is_available,
            'is_license_valid': self.is_license_valid(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
