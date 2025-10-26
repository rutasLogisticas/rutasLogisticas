"""
Repositorio de Pedidos para el sistema de rutas logísticas

Este módulo define el repositorio para manejar operaciones de base de datos
relacionadas con pedidos.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.repositories.base import BaseRepository
from app.models.order import Order


class OrderRepository(BaseRepository[Order]):
    """Repositorio para manejar operaciones de pedidos"""
    
    def __init__(self):
        super().__init__(Order)
    
    def get_by_client(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por cliente"""
        return db.query(Order).filter(
            and_(Order.client_id == client_id, Order.is_active == True)
        ).offset(skip).limit(limit).all()
    
    def get_by_driver(self, db: Session, driver_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por conductor"""
        return db.query(Order).filter(
            and_(Order.driver_id == driver_id, Order.is_active == True)
        ).offset(skip).limit(limit).all()
    
    def get_by_vehicle(self, db: Session, vehicle_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por vehículo"""
        return db.query(Order).filter(
            and_(Order.vehicle_id == vehicle_id, Order.is_active == True)
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por estado"""
        return db.query(Order).filter(
            and_(Order.status == status, Order.is_active == True)
        ).offset(skip).limit(limit).all()
    
    def get_by_tracking_code(self, db: Session, tracking_code: str) -> Optional[Order]:
        """Obtiene pedido por código de seguimiento"""
        return db.query(Order).filter(
            and_(Order.tracking_code == tracking_code, Order.is_active == True)
        ).first()
    
    def get_by_order_number(self, db: Session, order_number: str) -> Optional[Order]:
        """Obtiene pedido por número de pedido"""
        return db.query(Order).filter(
            and_(Order.order_number == order_number, Order.is_active == True)
        ).first()
    
    def get_unassigned(self, db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos sin asignar (sin conductor o vehículo)"""
        return db.query(Order).filter(
            and_(
                Order.is_active == True,
                or_(Order.driver_id.is_(None), Order.vehicle_id.is_(None))
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_date_range(self, db: Session, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por rango de fechas"""
        return db.query(Order).filter(
            and_(
                Order.is_active == True,
                Order.created_at >= start_date,
                Order.created_at <= end_date
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_city(self, db: Session, city: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por ciudad (origen o destino)"""
        return db.query(Order).filter(
            and_(
                Order.is_active == True,
                or_(Order.origin_city.ilike(f"%{city}%"), Order.destination_city.ilike(f"%{city}%"))
            )
        ).offset(skip).limit(limit).all()
    
    def assign_driver_and_vehicle(self, db: Session, order_id: int, driver_id: int, vehicle_id: int, tracking_code: Optional[str] = None) -> Optional[Order]:
        """Asigna conductor y vehículo a un pedido"""
        order = self.get_by_id(db, order_id)
        if order:
            order.driver_id = driver_id
            order.vehicle_id = vehicle_id
            order.status = "asignado"
            if tracking_code:
                order.tracking_code = tracking_code
            db.commit()
            db.refresh(order)
        return order
    
    def update_status(self, db: Session, order_id: int, status: str) -> Optional[Order]:
        """Actualiza el estado de un pedido"""
        order = self.get_by_id(db, order_id)
        if order:
            order.status = status
            if status == "entregado":
                order.delivered_date = datetime.utcnow()
            db.commit()
            db.refresh(order)
        return order
