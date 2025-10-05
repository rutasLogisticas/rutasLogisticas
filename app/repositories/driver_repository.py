"""
Repositorio simple para conductores
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from app.models.driver import Driver


class DriverRepository(BaseRepository[Driver]):
    """Repositorio simple para conductores"""
    
    def __init__(self):
        super().__init__(Driver)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Driver]:
        """Obtiene conductor por email"""
        return db.query(Driver).filter(
            Driver.email == email,
            Driver.is_active == True
        ).first()
    
    def get_by_document(self, db: Session, document_number: str) -> Optional[Driver]:
        """Obtiene conductor por documento"""
        return db.query(Driver).filter(
            Driver.document_number == document_number,
            Driver.is_active == True
        ).first()
    
    def get_available_drivers(self, db: Session, skip: int = 0, limit: int = 100) -> List[Driver]:
        """Obtiene conductores disponibles"""
        return db.query(Driver).filter(
            Driver.is_available == True,
            Driver.is_active == True
        ).offset(skip).limit(limit).all()