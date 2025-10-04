"""
Servicio para gestión de clientes
Implementa principio SRP y lógica de negocio específica
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from .base import BaseService
from app.repositories.client_repository import ClientRepository
from app.models.client import Client, ClientType, ClientStatus

logger = logging.getLogger(__name__)


class ClientService(BaseService[Client, ClientRepository]):
    """
    Servicio para lógica de negocio de clientes
    Implementa principio SRP - responsabilidad única para clientes
    """
    
    def __init__(self):
        super().__init__(ClientRepository())
    
    def _validate_create(self, data: Dict[str, Any]) -> None:
        """Validaciones específicas para crear clientes"""
        # Validar email único si se proporciona
        if 'email' in data and data['email']:
            # Esta validación se hará a nivel de repositorio
            pass
        
        # Validar ID fiscal único si se proporciona
        if 'tax_id' in data and data['tax_id']:
            # Esta validación se hará a nivel de repositorio
            pass
        
        # Validar límite de crédito
        if 'credit_limit' in data and data['credit_limit'] is not None:
            if data['credit_limit'] < 0:
                raise ValueError("El límite de crédito no puede ser negativo")
        
        # Validar términos de pago
        if 'payment_terms' in data and data['payment_terms'] is not None:
            if data['payment_terms'] < 0:
                raise ValueError("Los términos de pago no pueden ser negativos")
        
        # Validar porcentaje de descuento
        if 'discount_percentage' in data and data['discount_percentage'] is not None:
            if data['discount_percentage'] < 0 or data['discount_percentage'] > 100:
                raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")
    
    def _validate_update(self, db_obj: Client, data: Dict[str, Any]) -> None:
        """Validaciones específicas para actualizar clientes"""
        # Aplicar las mismas validaciones que en create
        self._validate_create(data)
    
    def _validate_delete(self, db: Session, id: int) -> None:
        """Validaciones antes de eliminar cliente"""
        client = self.get_by_id(db, id)
        if client:
            # Verificar si el cliente tiene direcciones asociadas
            if client.addresses:
                # Solo permitir eliminación si no hay direcciones activas
                active_addresses = [addr for addr in client.addresses if addr.is_active]
                if active_addresses:
                    raise ValueError("No se puede eliminar un cliente que tiene direcciones activas")
    
    def create_client(self, db: Session, **kwargs) -> Client:
        """Crea un nuevo cliente con validaciones de negocio"""
        return self.create(db, **kwargs)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Client]:
        """Obtiene cliente por email"""
        return self.repository.get_by_email(db, email)
    
    def get_by_tax_id(self, db: Session, tax_id: str) -> Optional[Client]:
        """Obtiene cliente por ID fiscal"""
        return self.repository.get_by_tax_id(db, tax_id)
    
    def get_priority_clients(self, db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes prioritarios"""
        return self.repository.get_priority_clients(db, skip, limit)
    
    def get_active_clients(self, db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes activos"""
        return self.repository.get_active_clients(db, skip, limit)
    
    def get_clients_by_type(self, db: Session, client_type: ClientType, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por tipo"""
        return self.repository.get_by_client_type(db, client_type, skip, limit)
    
    def get_clients_by_status(self, db: Session, status: ClientStatus, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por estado"""
        return self.repository.get_by_status(db, status, skip, limit)
    
    def get_clients_by_city(self, db: Session, city: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por ciudad"""
        return self.repository.get_clients_by_city(db, city, skip, limit)
    
    def get_clients_by_state(self, db: Session, state: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por estado/provincia"""
        return self.repository.get_clients_by_state(db, state, skip, limit)
    
    def update_client_status(self, db: Session, client_id: int, status: ClientStatus) -> Optional[Client]:
        """Actualiza el estado de un cliente"""
        client = self.get_by_id(db, client_id)
        if not client:
            return None
        
        # Validaciones de negocio para cambio de estado
        if status == ClientStatus.INACTIVO and client.is_priority:
            # Permitir pero advertir sobre cliente prioritario
            logger.warning(f"Cliente prioritario {client.name} marcado como inactivo")
        
        return self.repository.update_client_status(db, client_id, status)
    
    def set_priority(self, db: Session, client_id: int, is_priority: bool) -> Optional[Client]:
        """Establece si un cliente es prioritario"""
        client = self.get_by_id(db, client_id)
        if not client:
            return None
        
        # Si se establece como prioritario, asegurar que esté activo
        if is_priority and client.status != ClientStatus.ACTIVO:
            client.status = ClientStatus.ACTIVO
        
        return self.repository.set_priority(db, client_id, is_priority)
    
    def set_notifications(self, db: Session, client_id: int, receives_notifications: bool) -> Optional[Client]:
        """Establece si un cliente recibe notificaciones"""
        return self.repository.set_notifications(db, client_id, receives_notifications)
    
    def update_credit_limit(self, db: Session, client_id: int, credit_limit: float) -> Optional[Client]:
        """Actualiza el límite de crédito de un cliente"""
        if credit_limit < 0:
            raise ValueError("El límite de crédito no puede ser negativo")
        
        return self.update(db, client_id, credit_limit=credit_limit)
    
    def update_payment_terms(self, db: Session, client_id: int, payment_terms: int) -> Optional[Client]:
        """Actualiza los términos de pago de un cliente"""
        if payment_terms < 0:
            raise ValueError("Los términos de pago no pueden ser negativos")
        
        return self.update(db, client_id, payment_terms=payment_terms)
    
    def update_discount_percentage(self, db: Session, client_id: int, discount_percentage: float) -> Optional[Client]:
        """Actualiza el porcentaje de descuento de un cliente"""
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")
        
        return self.update(db, client_id, discount_percentage=discount_percentage)
    
    def get_client_summary(self, db: Session, client_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene resumen completo de un cliente"""
        client = self.get_by_id(db, client_id)
        if not client:
            return None
        
        # Contar direcciones activas
        active_addresses_count = len([addr for addr in client.addresses if addr.is_active])
        
        return {
            'basic_info': client.to_summary_dict(),
            'contact_info': client.get_contact_info(),
            'location_info': client.get_main_address_info(),
            'commercial_info': client.get_commercial_info(),
            'addresses': {
                'total': len(client.addresses),
                'active': active_addresses_count,
                'primary': client.addresses[0].is_primary if client.addresses else False
            },
            'created_at': client.created_at.isoformat() if client.created_at else None,
            'updated_at': client.updated_at.isoformat() if client.updated_at else None
        }
    
    def search_clients(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Búsqueda avanzada de clientes"""
        return self.repository.search_clients(db, search_term, skip, limit)
    
    def get_clients_by_tags(self, db: Session, tag: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes por tags"""
        return self.repository.get_clients_by_tags(db, tag, skip, limit)
    
    def get_client_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtiene estadísticas completas de clientes"""
        return self.repository.get_client_statistics(db)
    
    def get_clients_with_notifications(self, db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        """Obtiene clientes que reciben notificaciones"""
        return self.repository.get_clients_with_notifications(db, skip, limit)
