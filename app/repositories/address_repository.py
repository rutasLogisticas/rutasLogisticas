"""
Repositorio simple para direcciones
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from app.models.address import Address


class AddressRepository(BaseRepository[Address]):
    """Repositorio simple para direcciones"""
    
    def __init__(self):
        super().__init__(Address)
    
    def get_by_client_id(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por cliente"""
        return db.query(Address).filter(
            Address.client_id == client_id,
            Address.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_primary_address(self, db: Session, client_id: int) -> Optional[Address]:
        """Obtiene dirección principal del cliente"""
        return db.query(Address).filter(
            Address.client_id == client_id,
            Address.is_primary == True,
            Address.is_active == True
        ).first()
    
    def get_by_city(self, db: Session, city: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por ciudad"""
        return db.query(Address).filter(
            Address.city == city,
            Address.is_active == True
        ).offset(skip).limit(limit).all()