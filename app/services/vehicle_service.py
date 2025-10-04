"""
Servicio para gestión de vehículos
Implementa principio SRP y lógica de negocio específica
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from .base import BaseService
from app.repositories.vehicle_repository import VehicleRepository
from app.models.vehicle import Vehicle, VehicleType, VehicleStatus

logger = logging.getLogger(__name__)


class VehicleService(BaseService[Vehicle, VehicleRepository]):
    """
    Servicio para lógica de negocio de vehículos
    Implementa principio SRP - responsabilidad única para vehículos
    """
    
    def __init__(self):
        super().__init__(VehicleRepository())
    
    def _validate_create(self, data: Dict[str, Any]) -> None:
        """Validaciones específicas para crear vehículos"""
        # Validar que la placa sea única
        if 'license_plate' in data:
            # Esta validación se hará a nivel de repositorio
            pass
        
        # Validar año del vehículo
        if 'year' in data:
            current_year = 2024
            if data['year'] < 1900 or data['year'] > current_year + 1:
                raise ValueError("Año del vehículo inválido")
        
        # Validar capacidades
        if 'capacity_weight' in data and data['capacity_weight'] is not None:
            if data['capacity_weight'] <= 0:
                raise ValueError("La capacidad de peso debe ser mayor a 0")
        
        if 'capacity_volume' in data and data['capacity_volume'] is not None:
            if data['capacity_volume'] <= 0:
                raise ValueError("La capacidad de volumen debe ser mayor a 0")
    
    def _validate_update(self, db_obj: Vehicle, data: Dict[str, Any]) -> None:
        """Validaciones específicas para actualizar vehículos"""
        # Aplicar las mismas validaciones que en create
        self._validate_create(data)
    
    def _validate_delete(self, db: Session, id: int) -> None:
        """Validaciones antes de eliminar vehículo"""
        vehicle = self.get_by_id(db, id)
        if vehicle:
            # Verificar si el vehículo está en ruta
            if vehicle.status == VehicleStatus.EN_RUTA:
                raise ValueError("No se puede eliminar un vehículo que está en ruta")
    
    def create_vehicle(self, db: Session, **kwargs) -> Vehicle:
        """Crea un nuevo vehículo con validaciones de negocio"""
        return self.create(db, **kwargs)
    
    def get_by_license_plate(self, db: Session, license_plate: str) -> Optional[Vehicle]:
        """Obtiene vehículo por placa"""
        return self.repository.get_by_license_plate(db, license_plate)
    
    def get_available_vehicles(self, db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos disponibles para uso"""
        return self.repository.get_available_vehicles(db, skip, limit)
    
    def get_vehicles_by_type(self, db: Session, vehicle_type: VehicleType, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos por tipo"""
        return self.repository.get_by_type(db, vehicle_type, skip, limit)
    
    def get_vehicles_by_status(self, db: Session, status: VehicleStatus, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos por estado"""
        return self.repository.get_by_status(db, status, skip, limit)
    
    def get_vehicles_by_capacity(self, db: Session, min_weight: float = None, min_volume: float = None, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos que pueden transportar la capacidad requerida"""
        return self.repository.get_vehicles_by_capacity(db, min_weight, min_volume, skip, limit)
    
    def update_vehicle_status(self, db: Session, vehicle_id: int, status: VehicleStatus) -> Optional[Vehicle]:
        """Actualiza el estado de un vehículo"""
        vehicle = self.get_by_id(db, vehicle_id)
        if not vehicle:
            return None
        
        # Validaciones de negocio para cambio de estado
        if vehicle.status == VehicleStatus.EN_RUTA and status != VehicleStatus.DISPONIBLE:
            raise ValueError("Un vehículo en ruta solo puede cambiar a disponible")
        
        return self.repository.update_vehicle_status(db, vehicle_id, status)
    
    def set_availability(self, db: Session, vehicle_id: int, is_available: bool) -> Optional[Vehicle]:
        """Establece disponibilidad del vehículo"""
        vehicle = self.get_by_id(db, vehicle_id)
        if not vehicle:
            return None
        
        # Si se marca como no disponible, cambiar estado a fuera de servicio
        if not is_available and vehicle.status == VehicleStatus.DISPONIBLE:
            vehicle.status = VehicleStatus.FUERA_SERVICIO
        
        return self.repository.set_availability(db, vehicle_id, is_available)
    
    def get_vehicles_needing_maintenance(self, db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos que necesitan mantenimiento"""
        return self.repository.get_vehicles_needing_maintenance(db, skip, limit)
    
    def assign_vehicle_to_route(self, db: Session, vehicle_id: int) -> Optional[Vehicle]:
        """Asigna vehículo a una ruta"""
        vehicle = self.get_by_id(db, vehicle_id)
        if not vehicle:
            return None
        
        if not vehicle.is_operational():
            raise ValueError("El vehículo no está operacional para asignar a ruta")
        
        vehicle.status = VehicleStatus.EN_RUTA
        return self.repository.update(db, vehicle)
    
    def release_vehicle_from_route(self, db: Session, vehicle_id: int) -> Optional[Vehicle]:
        """Libera vehículo de una ruta"""
        vehicle = self.get_by_id(db, vehicle_id)
        if not vehicle:
            return None
        
        if vehicle.status == VehicleStatus.EN_RUTA:
            vehicle.status = VehicleStatus.DISPONIBLE
        
        return self.repository.update(db, vehicle)
    
    def get_vehicle_summary(self, db: Session, vehicle_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene resumen completo de un vehículo"""
        vehicle = self.get_by_id(db, vehicle_id)
        if not vehicle:
            return None
        
        return {
            'basic_info': vehicle.to_summary_dict(),
            'operational_info': {
                'is_operational': vehicle.is_operational(),
                'can_carry_weight': vehicle.capacity_weight,
                'can_carry_volume': vehicle.capacity_volume,
                'fuel_type': vehicle.fuel_type,
                'fuel_consumption': vehicle.fuel_consumption
            },
            'maintenance_info': vehicle.get_maintenance_info(),
            'created_at': vehicle.created_at.isoformat() if vehicle.created_at else None,
            'updated_at': vehicle.updated_at.isoformat() if vehicle.updated_at else None
        }
    
    def search_vehicles(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Búsqueda avanzada de vehículos"""
        return self.repository.search_vehicles(db, search_term, skip, limit)
    
    def get_vehicle_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtiene estadísticas completas de vehículos"""
        return self.repository.get_vehicle_statistics(db)
