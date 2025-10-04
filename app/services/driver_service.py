"""
Servicio para gestión de conductores
Implementa principio SRP y lógica de negocio específica
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import date, timedelta
import logging

from .base import BaseService
from app.repositories.driver_repository import DriverRepository
from app.models.driver import Driver, DriverStatus, LicenseType

logger = logging.getLogger(__name__)


class DriverService(BaseService[Driver, DriverRepository]):
    """
    Servicio para lógica de negocio de conductores
    Implementa principio SRP - responsabilidad única para conductores
    """
    
    def __init__(self):
        super().__init__(DriverRepository())
    
    def _validate_create(self, data: Dict[str, Any]) -> None:
        """Validaciones específicas para crear conductores"""
        # Validar email único
        if 'email' in data:
            # Esta validación se hará a nivel de repositorio
            pass
        
        # Validar documento único
        if 'document_number' in data:
            # Esta validación se hará a nivel de repositorio
            pass
        
        # Validar licencia única
        if 'license_number' in data:
            # Esta validación se hará a nivel de repositorio
            pass
        
        # Validar fecha de nacimiento
        if 'birth_date' in data and data['birth_date']:
            birth_date = data['birth_date']
            if isinstance(birth_date, str):
                birth_date = date.fromisoformat(birth_date)
            
            age = (date.today() - birth_date).days // 365
            if age < 18:
                raise ValueError("El conductor debe ser mayor de 18 años")
            if age > 70:
                raise ValueError("El conductor debe ser menor de 70 años")
        
        # Validar fecha de expiración de licencia
        if 'license_expiry' in data and data['license_expiry']:
            license_expiry = data['license_expiry']
            if isinstance(license_expiry, str):
                license_expiry = date.fromisoformat(license_expiry)
            
            if license_expiry < date.today():
                raise ValueError("La licencia no puede estar expirada")
    
    def _validate_update(self, db_obj: Driver, data: Dict[str, Any]) -> None:
        """Validaciones específicas para actualizar conductores"""
        # Aplicar las mismas validaciones que en create
        self._validate_create(data)
    
    def _validate_delete(self, db: Session, id: int) -> None:
        """Validaciones antes de eliminar conductor"""
        driver = self.get_by_id(db, id)
        if driver:
            # Verificar si el conductor está en ruta
            if driver.status == DriverStatus.EN_RUTA:
                raise ValueError("No se puede eliminar un conductor que está en ruta")
    
    def create_driver(self, db: Session, **kwargs) -> Driver:
        """Crea un nuevo conductor con validaciones de negocio"""
        return self.create(db, **kwargs)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Driver]:
        """Obtiene conductor por email"""
        return self.repository.get_by_email(db, email)
    
    def get_by_document_number(self, db: Session, document_number: str) -> Optional[Driver]:
        """Obtiene conductor por número de documento"""
        return self.repository.get_by_document_number(db, document_number)
    
    def get_by_license_number(self, db: Session, license_number: str) -> Optional[Driver]:
        """Obtiene conductor por número de licencia"""
        return self.repository.get_by_license_number(db, license_number)
    
    def get_available_drivers(self, db: Session, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores disponibles"""
        return self.repository.get_available_drivers(db, skip, limit)
    
    def get_drivers_by_status(self, db: Session, status: DriverStatus, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores por estado"""
        return self.repository.get_by_status(db, status, skip, limit)
    
    def get_drivers_by_license_type(self, db: Session, license_type: LicenseType, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores por tipo de licencia"""
        return self.repository.get_by_license_type(db, license_type, skip, limit)
    
    def get_drivers_with_expired_license(self, db: Session, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores con licencias expiradas"""
        return self.repository.get_drivers_with_expired_license(db, skip, limit)
    
    def get_drivers_with_expiring_license(self, db: Session, days_ahead: int = 30, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores con licencias próximas a expirar"""
        return self.repository.get_drivers_with_expiring_license(db, days_ahead, skip, limit)
    
    def update_driver_status(self, db: Session, driver_id: int, status: DriverStatus) -> Optional[Driver]:
        """Actualiza el estado de un conductor"""
        driver = self.get_by_id(db, driver_id)
        if not driver:
            return None
        
        # Validaciones de negocio para cambio de estado
        if driver.status == DriverStatus.EN_RUTA and status not in [DriverStatus.DISPONIBLE, DriverStatus.DESCANSANDO]:
            raise ValueError("Un conductor en ruta solo puede cambiar a disponible o descansando")
        
        return self.repository.update_driver_status(db, driver_id, status)
    
    def set_availability(self, db: Session, driver_id: int, is_available: bool) -> Optional[Driver]:
        """Establece disponibilidad del conductor"""
        driver = self.get_by_id(db, driver_id)
        if not driver:
            return None
        
        # Si se marca como no disponible, cambiar estado a fuera de servicio
        if not is_available and driver.status == DriverStatus.DISPONIBLE:
            driver.status = DriverStatus.FUERA_SERVICIO
        
        return self.repository.set_availability(db, driver_id, is_available)
    
    def assign_driver_to_route(self, db: Session, driver_id: int) -> Optional[Driver]:
        """Asigna conductor a una ruta"""
        driver = self.get_by_id(db, driver_id)
        if not driver:
            return None
        
        if not driver.is_operational():
            raise ValueError("El conductor no está operacional para asignar a ruta")
        
        driver.status = DriverStatus.EN_RUTA
        return self.repository.update(db, driver)
    
    def release_driver_from_route(self, db: Session, driver_id: int) -> Optional[Driver]:
        """Libera conductor de una ruta"""
        driver = self.get_by_id(db, driver_id)
        if not driver:
            return None
        
        if driver.status == DriverStatus.EN_RUTA:
            driver.status = DriverStatus.DISPONIBLE
        
        return self.repository.update(db, driver)
    
    def can_drive_vehicle_type(self, db: Session, driver_id: int, vehicle_type: str) -> bool:
        """Verifica si un conductor puede conducir un tipo específico de vehículo"""
        driver = self.get_by_id(db, driver_id)
        if not driver:
            return False
        
        return driver.can_drive_vehicle_type(vehicle_type)
    
    def get_driver_summary(self, db: Session, driver_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene resumen completo de un conductor"""
        driver = self.get_by_id(db, driver_id)
        if not driver:
            return None
        
        return {
            'basic_info': driver.to_summary_dict(),
            'personal_info': {
                'full_name': driver.full_name,
                'age': driver.age,
                'document_number': driver.document_number,
                'birth_date': driver.birth_date.isoformat() if driver.birth_date else None
            },
            'license_info': {
                'license_type': driver.license_type.value,
                'license_number': driver.license_number,
                'license_expiry': driver.license_expiry.isoformat() if driver.license_expiry else None,
                'is_license_valid': driver.is_license_valid()
            },
            'contact_info': driver.get_contact_info(),
            'operational_info': {
                'is_operational': driver.is_operational(),
                'employee_id': driver.employee_id,
                'hire_date': driver.hire_date.isoformat() if driver.hire_date else None
            },
            'created_at': driver.created_at.isoformat() if driver.created_at else None,
            'updated_at': driver.updated_at.isoformat() if driver.updated_at else None
        }
    
    def search_drivers(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Búsqueda avanzada de conductores"""
        return self.repository.search_drivers(db, search_term, skip, limit)
    
    def get_driver_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtiene estadísticas completas de conductores"""
        return self.repository.get_driver_statistics(db)
    
    def check_license_expiry_alerts(self, db: Session, days_ahead: int = 30) -> List[Driver]:
        """Obtiene conductores con licencias próximas a expirar para alertas"""
        return self.get_drivers_with_expiring_license(db, days_ahead)
