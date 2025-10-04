"""
Repositorio específico para Vehículos
Implementa principio SRP y patrón Repository
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from .base import BaseRepository
from app.models.vehicle import Vehicle, VehicleType, VehicleStatus


class VehicleRepository(BaseRepository[Vehicle]):
    """
    Repositorio para gestión de vehículos
    Implementa principio SRP - responsabilidad única para vehículos
    """
    
    def __init__(self):
        super().__init__(Vehicle)
    
    def get_by_license_plate(self, db: Session, license_plate: str) -> Optional[Vehicle]:
        """Obtiene vehículo por placa"""
        return db.query(Vehicle).filter(
            and_(
                Vehicle.license_plate == license_plate,
                Vehicle.is_active == True
            )
        ).first()
    
    def get_by_type(self, db: Session, vehicle_type: VehicleType, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos por tipo"""
        return db.query(Vehicle).filter(
            and_(
                Vehicle.vehicle_type == vehicle_type,
                Vehicle.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, status: VehicleStatus, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos por estado"""
        return db.query(Vehicle).filter(
            and_(
                Vehicle.status == status,
                Vehicle.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_available_vehicles(self, db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos disponibles para uso"""
        return db.query(Vehicle).filter(
            and_(
                Vehicle.status == VehicleStatus.DISPONIBLE,
                Vehicle.is_available == True,
                Vehicle.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_vehicles_by_capacity(self, db: Session, min_weight: float = None, min_volume: float = None, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos que pueden transportar la capacidad requerida"""
        query = db.query(Vehicle).filter(Vehicle.is_active == True)
        
        if min_weight is not None:
            query = query.filter(Vehicle.capacity_weight >= min_weight)
        
        if min_volume is not None:
            query = query.filter(Vehicle.capacity_volume >= min_volume)
        
        return query.offset(skip).limit(limit).all()
    
    def search_vehicles(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Búsqueda de vehículos por múltiples campos"""
        search_fields = ['license_plate', 'brand', 'model', 'color']
        return self.search(db, search_term, search_fields, skip, limit)
    
    def get_vehicles_needing_maintenance(self, db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos que necesitan mantenimiento"""
        return db.query(Vehicle).filter(
            and_(
                Vehicle.is_active == True,
                Vehicle.status == VehicleStatus.MANTENIMIENTO
            )
        ).offset(skip).limit(limit).all()
    
    def get_vehicles_by_brand(self, db: Session, brand: str, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos por marca"""
        return db.query(Vehicle).filter(
            and_(
                Vehicle.brand.ilike(f"%{brand}%"),
                Vehicle.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def get_vehicles_by_year_range(self, db: Session, min_year: int = None, max_year: int = None, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos por rango de años"""
        query = db.query(Vehicle).filter(Vehicle.is_active == True)
        
        if min_year is not None:
            query = query.filter(Vehicle.year >= min_year)
        
        if max_year is not None:
            query = query.filter(Vehicle.year <= max_year)
        
        return query.offset(skip).limit(limit).all()
    
    def update_vehicle_status(self, db: Session, vehicle_id: int, status: VehicleStatus) -> Optional[Vehicle]:
        """Actualiza el estado de un vehículo"""
        vehicle = self.get_by_id(db, vehicle_id)
        if vehicle:
            vehicle.status = status
            return self.update(db, vehicle)
        return None
    
    def set_availability(self, db: Session, vehicle_id: int, is_available: bool) -> Optional[Vehicle]:
        """Establece disponibilidad del vehículo"""
        vehicle = self.get_by_id(db, vehicle_id)
        if vehicle:
            vehicle.is_available = is_available
            return self.update(db, vehicle)
        return None
    
    def get_vehicle_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtiene estadísticas de vehículos"""
        total = self.get_count(db)
        
        status_counts = {}
        for status in VehicleStatus:
            count = db.query(Vehicle).filter(
                and_(
                    Vehicle.status == status,
                    Vehicle.is_active == True
                )
            ).count()
            status_counts[status.value] = count
        
        type_counts = {}
        for vehicle_type in VehicleType:
            count = db.query(Vehicle).filter(
                and_(
                    Vehicle.vehicle_type == vehicle_type,
                    Vehicle.is_active == True
                )
            ).count()
            type_counts[vehicle_type.value] = count
        
        available_count = db.query(Vehicle).filter(
            and_(
                Vehicle.status == VehicleStatus.DISPONIBLE,
                Vehicle.is_available == True,
                Vehicle.is_active == True
            )
        ).count()
        
        return {
            'total_vehicles': total,
            'available_vehicles': available_count,
            'status_distribution': status_counts,
            'type_distribution': type_counts
        }
