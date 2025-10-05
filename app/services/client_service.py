"""
Servicio simple para clientes
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseService
from app.models.client import Client


class ClientService(BaseService):
    """Servicio simple para clientes"""
    
    def __init__(self):
        super().__init__()
        from app.repositories.client_repository import ClientRepository
        self.repository = ClientRepository()
    
    def get_by_email(self, db: Session, email: str) -> Optional[Client]:
        """Obtiene cliente por email"""
        return self.repository.get_by_email(db, email)
    
    def get_by_company(self, db: Session, company: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por empresa"""
        return self.repository.get_by_company(db, company, skip, limit)
    
    def get_active_clients(self, db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes activos"""
        return self.repository.get_active_clients(db, skip, limit)