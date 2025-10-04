"""
Repositorio específico para Direcciones
Implementa principio SRP y patrón Repository
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from .base import BaseRepository
from app.models.address import Address, AddressType


class AddressRepository(BaseRepository[Address]):
    """
    Repositorio para gestión de direcciones
    Implementa principio SRP - responsabilidad única para direcciones
    """
    
    def __init__(self):
        super().__init__(Address)
    
    def get_by_client_id(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por ID de cliente"""
        return db.query(Address).filter(
            and_(
                Address.client_id == client_id,
                Address.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_primary_address(self, db: Session, client_id: int) -> Optional[Address]:
        """Obtiene la dirección principal de un cliente"""
        return db.query(Address).filter(
            and_(
                Address.client_id == client_id,
                Address.is_primary == True,
                Address.is_active == True
            )
        ).first()
    
    def get_by_type(self, db: Session, client_id: int, address_type: AddressType, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por tipo"""
        return db.query(Address).filter(
            and_(
                Address.client_id == client_id,
                Address.address_type == address_type,
                Address.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_delivery_addresses(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones disponibles para entrega"""
        return db.query(Address).filter(
            and_(
                Address.client_id == client_id,
                Address.is_delivery_available == True,
                Address.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_addresses_by_city(self, db: Session, city: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por ciudad"""
        return db.query(Address).filter(
            and_(
                Address.city.ilike(f"%{city}%"),
                Address.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_addresses_by_state(self, db: Session, state: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por estado/provincia"""
        return db.query(Address).filter(
            and_(
                Address.state.ilike(f"%{state}%"),
                Address.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_addresses_with_coordinates(self, db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones que tienen coordenadas geográficas"""
        return db.query(Address).filter(
            and_(
                Address.latitude.isnot(None),
                Address.longitude.isnot(None),
                Address.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def search_addresses(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Búsqueda de direcciones por múltiples campos"""
        search_fields = ['address_line1', 'address_line2', 'neighborhood', 'city', 'state', 'postal_code']
        return self.search(db, search_term, search_fields, skip, limit)
    
    def get_addresses_in_radius(self, db: Session, latitude: float, longitude: float, radius_km: float, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones dentro de un radio específico (requiere extensión PostGIS)"""
        # Nota: Esta implementación requeriría la extensión PostGIS para cálculos geográficos precisos
        # Por ahora retornamos direcciones con coordenadas
        return db.query(Address).filter(
            and_(
                Address.latitude.isnot(None),
                Address.longitude.isnot(None),
                Address.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_addresses_with_parking(self, db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones con estacionamiento disponible"""
        return db.query(Address).filter(
            and_(
                Address.parking_available == True,
                Address.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def set_primary_address(self, db: Session, client_id: int, address_id: int) -> bool:
        """Establece una dirección como principal (desactiva otras principales del cliente)"""
        # Primero desactivar todas las direcciones principales del cliente
        db.query(Address).filter(
            and_(
                Address.client_id == client_id,
                Address.is_primary == True,
                Address.is_active == True
            )
        ).update({"is_primary": False})
        
        # Establecer la nueva dirección como principal
        address = self.get_by_id(db, address_id)
        if address and address.client_id == client_id:
            address.is_primary = True
            db.add(address)
            db.flush()
            return True
        
        return False
    
    def set_delivery_availability(self, db: Session, address_id: int, is_delivery_available: bool) -> Optional[Address]:
        """Establece disponibilidad de entrega para una dirección"""
        address = self.get_by_id(db, address_id)
        if address:
            address.is_delivery_available = is_delivery_available
            return self.update(db, address)
        return None
    
    def update_coordinates(self, db: Session, address_id: int, latitude: float, longitude: float) -> Optional[Address]:
        """Actualiza las coordenadas geográficas de una dirección"""
        address = self.get_by_id(db, address_id)
        if address:
            address.latitude = latitude
            address.longitude = longitude
            return self.update(db, address)
        return None
    
    def get_address_statistics(self, db: Session, client_id: int = None) -> Dict[str, Any]:
        """Obtiene estadísticas de direcciones"""
        query = db.query(Address).filter(Address.is_active == True)
        
        if client_id:
            query = query.filter(Address.client_id == client_id)
        
        total = query.count()
        
        type_counts = {}
        for address_type in AddressType:
            count = query.filter(Address.address_type == address_type).count()
            type_counts[address_type.value] = count
        
        primary_count = query.filter(Address.is_primary == True).count()
        delivery_available_count = query.filter(Address.is_delivery_available == True).count()
        with_coordinates_count = query.filter(
            and_(
                Address.latitude.isnot(None),
                Address.longitude.isnot(None)
            )
        ).count()
        parking_available_count = query.filter(Address.parking_available == True).count()
        
        return {
            'total_addresses': total,
            'primary_addresses': primary_count,
            'delivery_available': delivery_available_count,
            'with_coordinates': with_coordinates_count,
            'parking_available': parking_available_count,
            'type_distribution': type_counts
        }
