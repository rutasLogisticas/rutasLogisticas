"""
Repositorio simple para vehículos
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from app.models.vehicle import Vehicle


class VehicleRepository(BaseRepository[Vehicle]):
    """Repositorio simple para vehículos"""
    
    def __init__(self):
        super().__init__(Vehicle)
    
    def get_by_license_plate(self, db: Session, license_plate: str) -> Optional[Vehicle]:
        """Obtiene vehículo por placa"""
        return db.query(Vehicle).filter(
            Vehicle.license_plate == license_plate,
            Vehicle.is_active == True
        ).first()
    
    def get_available_vehicles(self, db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos disponibles"""
        return db.query(Vehicle).filter(
            Vehicle.is_available == True,
            Vehicle.is_active == True
        ).offset(skip).limit(limit).all()