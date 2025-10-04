"""
Repositorio específico para Conductores
Implementa principio SRP y patrón Repository
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date

from .base import BaseRepository
from app.models.driver import Driver, DriverStatus, LicenseType


class DriverRepository(BaseRepository[Driver]):
    """
    Repositorio para gestión de conductores
    Implementa principio SRP - responsabilidad única para conductores
    """
    
    def __init__(self):
        super().__init__(Driver)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Driver]:
        """Obtiene conductor por email"""
        return db.query(Driver).filter(
            and_(
                Driver.email == email,
                Driver.is_active == True
            )
        ).first()
    
    def get_by_document_number(self, db: Session, document_number: str) -> Optional[Driver]:
        """Obtiene conductor por número de documento"""
        return db.query(Driver).filter(
            and_(
                Driver.document_number == document_number,
                Driver.is_active == True
            )
        ).first()
    
    def get_by_license_number(self, db: Session, license_number: str) -> Optional[Driver]:
        """Obtiene conductor por número de licencia"""
        return db.query(Driver).filter(
            and_(
                Driver.license_number == license_number,
                Driver.is_active == True
            )
        ).first()
    
    def get_by_employee_id(self, db: Session, employee_id: str) -> Optional[Driver]:
        """Obtiene conductor por ID de empleado"""
        return db.query(Driver).filter(
            and_(
                Driver.employee_id == employee_id,
                Driver.is_active == True
            )
        ).first()
    
    def get_by_status(self, db: Session, status: DriverStatus, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores por estado"""
        return db.query(Driver).filter(
            and_(
                Driver.status == status,
                Driver.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_available_drivers(self, db: Session, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores disponibles"""
        return db.query(Driver).filter(
            and_(
                Driver.status == DriverStatus.DISPONIBLE,
                Driver.is_available == True,
                Driver.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_license_type(self, db: Session, license_type: LicenseType, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores por tipo de licencia"""
        return db.query(Driver).filter(
            and_(
                Driver.license_type == license_type,
                Driver.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_drivers_with_expired_license(self, db: Session, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores con licencias expiradas"""
        today = date.today()
        return db.query(Driver).filter(
            and_(
                Driver.license_expiry < today,
                Driver.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_drivers_with_expiring_license(self, db: Session, days_ahead: int = 30, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores con licencias próximas a expirar"""
        from datetime import timedelta
        future_date = date.today() + timedelta(days=days_ahead)
        
        return db.query(Driver).filter(
            and_(
                Driver.license_expiry <= future_date,
                Driver.license_expiry >= date.today(),
                Driver.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def search_drivers(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Búsqueda de conductores por múltiples campos"""
        search_fields = ['first_name', 'last_name', 'email', 'document_number', 'license_number', 'employee_id']
        return self.search(db, search_term, search_fields, skip, limit)
    
    def get_drivers_by_age_range(self, db: Session, min_age: int = None, max_age: int = None, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores por rango de edad"""
        from datetime import date
        
        query = db.query(Driver).filter(Driver.is_active == True)
        
        if min_age is not None:
            min_birth_date = date(date.today().year - max_age, date.today().month, date.today().day) if max_age else None
            if min_birth_date:
                query = query.filter(Driver.birth_date <= min_birth_date)
        
        if max_age is not None:
            max_birth_date = date(date.today().year - min_age, date.today().month, date.today().day) if min_age else None
            if max_birth_date:
                query = query.filter(Driver.birth_date >= max_birth_date)
        
        return query.offset(skip).limit(limit).all()
    
    def get_drivers_by_hire_date_range(self, db: Session, start_date: date = None, end_date: date = None, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores por rango de fecha de contratación"""
        query = db.query(Driver).filter(Driver.is_active == True)
        
        if start_date is not None:
            query = query.filter(Driver.hire_date >= start_date)
        
        if end_date is not None:
            query = query.filter(Driver.hire_date <= end_date)
        
        return query.offset(skip).limit(limit).all()
    
    def update_driver_status(self, db: Session, driver_id: int, status: DriverStatus) -> Optional[Driver]:
        """Actualiza el estado de un conductor"""
        driver = self.get_by_id(db, driver_id)
        if driver:
            driver.status = status
            return self.update(db, driver)
        return None
    
    def set_availability(self, db: Session, driver_id: int, is_available: bool) -> Optional[Driver]:
        """Establece disponibilidad del conductor"""
        driver = self.get_by_id(db, driver_id)
        if driver:
            driver.is_available = is_available
            return self.update(db, driver)
        return None
    
    def get_driver_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtiene estadísticas de conductores"""
        total = self.get_count(db)
        
        status_counts = {}
        for status in DriverStatus:
            count = db.query(Driver).filter(
                and_(
                    Driver.status == status,
                    Driver.is_active == True
                )
            ).count()
            status_counts[status.value] = count
        
        license_counts = {}
        for license_type in LicenseType:
            count = db.query(Driver).filter(
                and_(
                    Driver.license_type == license_type,
                    Driver.is_active == True
                )
            ).count()
            license_counts[license_type.value] = count
        
        available_count = db.query(Driver).filter(
            and_(
                Driver.status == DriverStatus.DISPONIBLE,
                Driver.is_available == True,
                Driver.is_active == True
            )
        ).count()
        
        expired_licenses = len(self.get_drivers_with_expired_license(db))
        expiring_licenses = len(self.get_drivers_with_expiring_license(db))
        
        return {
            'total_drivers': total,
            'available_drivers': available_count,
            'status_distribution': status_counts,
            'license_type_distribution': license_counts,
            'expired_licenses': expired_licenses,
            'expiring_licenses': expiring_licenses
        }
