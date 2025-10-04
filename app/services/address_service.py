"""
Servicio para gestión de direcciones
Implementa principio SRP y lógica de negocio específica
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from .base import BaseService
from app.repositories.address_repository import AddressRepository
from app.models.address import Address, AddressType

logger = logging.getLogger(__name__)


class AddressService(BaseService[Address, AddressRepository]):
    """
    Servicio para lógica de negocio de direcciones
    Implementa principio SRP - responsabilidad única para direcciones
    """
    
    def __init__(self):
        super().__init__(AddressRepository())
    
    def _validate_create(self, data: Dict[str, Any]) -> None:
        """Validaciones específicas para crear direcciones"""
        # Validar que se proporcione client_id
        if 'client_id' not in data:
            raise ValueError("El ID del cliente es requerido")
        
        # Validar que se proporcione al menos address_line1
        if 'address_line1' not in data or not data['address_line1']:
            raise ValueError("La dirección principal es requerida")
        
        # Validar que se proporcione ciudad
        if 'city' not in data or not data['city']:
            raise ValueError("La ciudad es requerida")
        
        # Validar que se proporcione estado
        if 'state' not in data or not data['state']:
            raise ValueError("El estado/provincia es requerido")
        
        # Validar coordenadas si se proporcionan
        if 'latitude' in data and data['latitude'] is not None:
            if not (-90 <= data['latitude'] <= 90):
                raise ValueError("La latitud debe estar entre -90 y 90")
        
        if 'longitude' in data and data['longitude'] is not None:
            if not (-180 <= data['longitude'] <= 180):
                raise ValueError("La longitud debe estar entre -180 y 180")
    
    def _validate_update(self, db_obj: Address, data: Dict[str, Any]) -> None:
        """Validaciones específicas para actualizar direcciones"""
        # Aplicar las mismas validaciones que en create
        self._validate_create(data)
    
    def _validate_delete(self, db: Session, id: int) -> None:
        """Validaciones antes de eliminar dirección"""
        address = self.get_by_id(db, id)
        if address:
            # Verificar si es la dirección principal
            if address.is_primary:
                raise ValueError("No se puede eliminar la dirección principal. Primero establezca otra como principal.")
    
    def create_address(self, db: Session, **kwargs) -> Address:
        """Crea una nueva dirección con validaciones de negocio"""
        # Si es la primera dirección del cliente, establecerla como principal
        if 'is_primary' not in kwargs:
            client_addresses = self.repository.get_by_client_id(db, kwargs['client_id'])
            if not client_addresses:
                kwargs['is_primary'] = True
        
        return self.create(db, **kwargs)
    
    def get_by_client_id(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por ID de cliente"""
        return self.repository.get_by_client_id(db, client_id, skip, limit)
    
    def get_primary_address(self, db: Session, client_id: int) -> Optional[Address]:
        """Obtiene la dirección principal de un cliente"""
        return self.repository.get_primary_address(db, client_id)
    
    def get_by_type(self, db: Session, client_id: int, address_type: AddressType, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por tipo"""
        return self.repository.get_by_type(db, client_id, address_type, skip, limit)
    
    def get_delivery_addresses(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones disponibles para entrega"""
        return self.repository.get_delivery_addresses(db, client_id, skip, limit)
    
    def set_primary_address(self, db: Session, client_id: int, address_id: int) -> bool:
        """Establece una dirección como principal"""
        return self.repository.set_primary_address(db, client_id, address_id)
    
    def set_delivery_availability(self, db: Session, address_id: int, is_delivery_available: bool) -> Optional[Address]:
        """Establece disponibilidad de entrega para una dirección"""
        address = self.get_by_id(db, address_id)
        if not address:
            return None
        
        # Si se desactiva la disponibilidad de entrega y es la dirección principal,
        # verificar que haya otras direcciones disponibles para entrega
        if not is_delivery_available and address.is_primary:
            delivery_addresses = self.get_delivery_addresses(db, address.client_id)
            other_delivery_addresses = [addr for addr in delivery_addresses if addr.id != address_id]
            if not other_delivery_addresses:
                raise ValueError("No se puede desactivar la entrega en la única dirección disponible")
        
        return self.repository.set_delivery_availability(db, address_id, is_delivery_available)
    
    def update_coordinates(self, db: Session, address_id: int, latitude: float, longitude: float) -> Optional[Address]:
        """Actualiza las coordenadas geográficas de una dirección"""
        # Validar coordenadas
        if not (-90 <= latitude <= 90):
            raise ValueError("La latitud debe estar entre -90 y 90")
        
        if not (-180 <= longitude <= 180):
            raise ValueError("La longitud debe estar entre -180 y 180")
        
        return self.repository.update_coordinates(db, address_id, latitude, longitude)
    
    def get_addresses_by_city(self, db: Session, city: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por ciudad"""
        return self.repository.get_addresses_by_city(db, city, skip, limit)
    
    def get_addresses_by_state(self, db: Session, state: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones por estado/provincia"""
        return self.repository.get_addresses_by_state(db, state, skip, limit)
    
    def get_addresses_with_coordinates(self, db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones que tienen coordenadas geográficas"""
        return self.repository.get_addresses_with_coordinates(db, skip, limit)
    
    def get_addresses_with_parking(self, db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
        """Obtiene direcciones con estacionamiento disponible"""
        return self.repository.get_addresses_with_parking(db, skip, limit)
    
    def get_address_summary(self, db: Session, address_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene resumen completo de una dirección"""
        address = self.get_by_id(db, address_id)
        if not address:
            return None
        
        return {
            'basic_info': address.to_summary_dict(),
            'location_info': address.get_location_info(),
            'contact_info': address.get_contact_info(),
            'operational_info': {
                'is_accessible_for_delivery': address.is_accessible_for_delivery(),
                'has_coordinates': address.has_coordinates(),
                'coordinates': address.get_coordinates() if address.has_coordinates() else None
            },
            'created_at': address.created_at.isoformat() if address.created_at else None,
            'updated_at': address.updated_at.isoformat() if address.updated_at else None
        }
    
    def search_addresses(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Búsqueda avanzada de direcciones"""
        return self.repository.search_addresses(db, search_term, skip, limit)
    
    def get_address_statistics(self, db: Session, client_id: int = None) -> Dict[str, Any]:
        """Obtiene estadísticas de direcciones"""
        return self.repository.get_address_statistics(db, client_id)
    
    def validate_address_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida y limpia datos de dirección"""
        validated_data = {}
        
        # Campos requeridos
        required_fields = ['client_id', 'address_line1', 'city', 'state']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"El campo {field} es requerido")
            validated_data[field] = data[field]
        
        # Campos opcionales
        optional_fields = [
            'address_line2', 'neighborhood', 'country', 'postal_code',
            'address_type', 'reference_points', 'delivery_instructions',
            'contact_name', 'contact_phone', 'access_notes',
            'delivery_time_preference', 'latitude', 'longitude'
        ]
        
        for field in optional_fields:
            if field in data:
                validated_data[field] = data[field]
        
        # Valores por defecto
        validated_data.setdefault('country', 'Ecuador')
        validated_data.setdefault('address_type', AddressType.DOMICILIO)
        validated_data.setdefault('is_active', True)
        validated_data.setdefault('is_delivery_available', True)
        validated_data.setdefault('parking_available', True)
        
        return validated_data
