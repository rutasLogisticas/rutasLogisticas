"""
Servicio simple para conductores
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseService
from app.models.driver import Driver


class DriverService(BaseService):
    """Servicio simple para conductores"""
    
    def __init__(self):
        super().__init__()
        from app.repositories.driver_repository import DriverRepository
        self.repository = DriverRepository()
    
    def get_by_email(self, db: Session, email: str) -> Optional[Driver]:
        """Obtiene conductor por email"""
        return self.repository.get_by_email(db, email)
    
    def get_by_document(self, db: Session, document_number: str) -> Optional[Driver]:
        """Obtiene conductor por documento"""
        return self.repository.get_by_document(db, document_number)
    
    def get_available_drivers(self, db: Session, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores disponibles"""
        return self.repository.get_available_drivers(db, skip, limit)