"""
Repositorio simple para clientes
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from app.models.client import Client


class ClientRepository(BaseRepository[Client]):
    """Repositorio simple para clientes"""
    
    def __init__(self):
        super().__init__(Client)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Client]:
        """Obtiene cliente por email"""
        return db.query(Client).filter(
            Client.email == email,
            Client.is_active == True
        ).first()
    
    def get_by_company(self, db: Session, company: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por empresa"""
        return db.query(Client).filter(
            Client.company == company,
            Client.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_active_clients(self, db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes activos"""
        return db.query(Client).filter(
            Client.is_active == True
        ).offset(skip).limit(limit).all()