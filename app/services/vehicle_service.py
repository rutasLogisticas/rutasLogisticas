"""
Servicio simple para vehículos
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseService
from app.models.vehicle import Vehicle


class VehicleService(BaseService):
    """Servicio simple para vehículos"""
    
    def __init__(self):
        super().__init__()
        from app.repositories.vehicle_repository import VehicleRepository
        self.repository = VehicleRepository()
    
    def get_by_license_plate(self, db: Session, license_plate: str) -> Optional[Vehicle]:
        """Obtiene vehículo por placa"""
        return self.repository.get_by_license_plate(db, license_plate)
    
    def get_available_vehicles(self, db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Obtiene vehículos disponibles"""
        return self.repository.get_available_vehicles(db, skip, limit)