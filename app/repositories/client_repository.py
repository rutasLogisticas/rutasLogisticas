"""
Repositorio específico para Clientes
Implementa principio SRP y patrón Repository
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from .base import BaseRepository
from app.models.client import Client, ClientType, ClientStatus


class ClientRepository(BaseRepository[Client]):
    """
    Repositorio para gestión de clientes
    Implementa principio SRP - responsabilidad única para clientes
    """
    
    def __init__(self):
        super().__init__(Client)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Client]:
        """Obtiene cliente por email"""
        return db.query(Client).filter(
            and_(
                or_(
                    Client.email == email,
                    Client.contact_email == email
                ),
                Client.is_active == True
            )
        ).first()
    
    def get_by_tax_id(self, db: Session, tax_id: str) -> Optional[Client]:
        """Obtiene cliente por ID fiscal (RUC, NIT, etc.)"""
        return db.query(Client).filter(
            and_(
                Client.tax_id == tax_id,
                Client.is_active == True
            )
        ).first()
    
    def get_by_client_type(self, db: Session, client_type: ClientType, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por tipo"""
        return db.query(Client).filter(
            and_(
                Client.client_type == client_type,
                Client.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, status: ClientStatus, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por estado"""
        return db.query(Client).filter(
            and_(
                Client.status == status,
                Client.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_priority_clients(self, db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes prioritarios"""
        return db.query(Client).filter(
            and_(
                Client.is_priority == True,
                Client.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_active_clients(self, db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes activos"""
        return db.query(Client).filter(
            and_(
                Client.status == ClientStatus.ACTIVO,
                Client.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def search_clients(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Búsqueda de clientes por múltiples campos"""
        search_fields = ['name', 'email', 'tax_id', 'business_name', 'contact_person', 'phone']
        return self.search(db, search_term, search_fields, skip, limit)
    
    def get_clients_by_city(self, db: Session, city: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por ciudad"""
        return db.query(Client).filter(
            and_(
                Client.city.ilike(f"%{city}%"),
                Client.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_clients_by_state(self, db: Session, state: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por estado/provincia"""
        return db.query(Client).filter(
            and_(
                Client.state.ilike(f"%{state}%"),
                Client.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_clients_by_credit_limit_range(self, db: Session, min_limit: float = None, max_limit: float = None, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por rango de límite de crédito"""
        query = db.query(Client).filter(Client.is_active == True)
        
        if min_limit is not None:
            query = query.filter(Client.credit_limit >= min_limit)
        
        if max_limit is not None:
            query = query.filter(Client.credit_limit <= max_limit)
        
        return query.offset(skip).limit(limit).all()
    
    def get_clients_with_notifications(self, db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes que reciben notificaciones"""
        return db.query(Client).filter(
            and_(
                Client.receives_notifications == True,
                Client.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_clients_by_tags(self, db: Session, tag: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes que tienen un tag específico"""
        return db.query(Client).filter(
            and_(
                Client.tags.ilike(f"%{tag}%"),
                Client.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def update_client_status(self, db: Session, client_id: int, status: ClientStatus) -> Optional[Client]:
        """Actualiza el estado de un cliente"""
        client = self.get_by_id(db, client_id)
        if client:
            client.status = status
            return self.update(db, client)
        return None
    
    def set_priority(self, db: Session, client_id: int, is_priority: bool) -> Optional[Client]:
        """Establece si un cliente es prioritario"""
        client = self.get_by_id(db, client_id)
        if client:
            client.is_priority = is_priority
            return self.update(db, client)
        return None
    
    def set_notifications(self, db: Session, client_id: int, receives_notifications: bool) -> Optional[Client]:
        """Establece si un cliente recibe notificaciones"""
        client = self.get_by_id(db, client_id)
        if client:
            client.receives_notifications = receives_notifications
            return self.update(db, client)
        return None
    
    def get_client_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtiene estadísticas de clientes"""
        total = self.get_count(db)
        
        status_counts = {}
        for status in ClientStatus:
            count = db.query(Client).filter(
                and_(
                    Client.status == status,
                    Client.is_active == True
                )
            ).count()
            status_counts[status.value] = count
        
        type_counts = {}
        for client_type in ClientType:
            count = db.query(Client).filter(
                and_(
                    Client.client_type == client_type,
                    Client.is_active == True
                )
            ).count()
            type_counts[client_type.value] = count
        
        priority_count = db.query(Client).filter(
            and_(
                Client.is_priority == True,
                Client.is_active == True
            )
        ).count()
        
        active_count = db.query(Client).filter(
            and_(
                Client.status == ClientStatus.ACTIVO,
                Client.is_active == True
            )
        ).count()
        
        notifications_count = db.query(Client).filter(
            and_(
                Client.receives_notifications == True,
                Client.is_active == True
            )
        ).count()
        
        return {
            'total_clients': total,
            'active_clients': active_count,
            'priority_clients': priority_count,
            'clients_with_notifications': notifications_count,
            'status_distribution': status_counts,
            'type_distribution': type_counts
        }
