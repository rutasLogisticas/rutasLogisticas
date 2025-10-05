"""
Servicio simple para direcciones
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseService
from app.models.address import Address


class AddressService(BaseService):
    """Servicio simple para direcciones"""
    
    def __init__(self):
        super().__init__()
        from app.repositories.address_repository import AddressRepository
        self.repository = AddressRepository()
    
    def get_by_client_id(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por cliente"""
        return self.repository.get_by_client_id(db, client_id, skip, limit)
    
    def get_primary_address(self, db: Session, client_id: int) -> Optional[Address]:
        """Obtiene dirección principal del cliente"""
        return self.repository.get_primary_address(db, client_id)
    
    def get_by_city(self, db: Session, city: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por ciudad"""
        return self.repository.get_by_city(db, city, skip, limit)