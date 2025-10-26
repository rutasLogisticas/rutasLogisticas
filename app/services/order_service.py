"""
Servicio de Pedidos para el sistema de rutas logísticas

Este módulo define la lógica de negocio para manejar pedidos.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.base import BaseService
from app.models.order import Order
from app.repositories.order_repository import OrderRepository
from app.schemas.order_schemas import OrderCreate, OrderUpdate, OrderAssignment


class OrderService(BaseService):
    """Servicio para manejar la lógica de negocio de pedidos"""
    
    def __init__(self):
        super().__init__()
        self.repository = OrderRepository()
    
    def create_order(self, db: Session, order_data: OrderCreate) -> Order:
        """Crea un nuevo pedido con número automático"""
        try:
            # Validar que el cliente existe
            from app.repositories.client_repository import ClientRepository
            client_repo = ClientRepository()
            client = client_repo.get_by_id(db, order_data.client_id)
            if not client:
                raise ValueError(f"Cliente con ID {order_data.client_id} no encontrado")

            # Validar conductor si se proporciona
            if order_data.driver_id:
                from app.repositories.driver_repository import DriverRepository
                driver_repo = DriverRepository()
                driver = driver_repo.get_by_id(db, order_data.driver_id)
                if not driver:
                    raise ValueError(f"Conductor con ID {order_data.driver_id} no encontrado")

            # Validar vehículo si se proporciona
            if order_data.vehicle_id:
                from app.repositories.vehicle_repository import VehicleRepository
                vehicle_repo = VehicleRepository()
                vehicle = vehicle_repo.get_by_id(db, order_data.vehicle_id)
                if not vehicle:
                    raise ValueError(f"Vehículo con ID {order_data.vehicle_id} no encontrado")

            # Generar número de pedido único
            order_number = self._generate_order_number(db)
            
            # Crear el pedido
            order_dict = order_data.model_dump()
            order_dict["order_number"] = order_number
            
            return self.repository.create(db, **order_dict)
            
        except Exception as e:
            raise ValueError(f"Error al crear pedido: {str(e)}")
    
    def get_by_client(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por cliente"""
        return self.repository.get_by_client(db, client_id, skip, limit)
    
    def get_by_driver(self, db: Session, driver_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por conductor"""
        return self.repository.get_by_driver(db, driver_id, skip, limit)
    
    def get_by_vehicle(self, db: Session, vehicle_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por vehículo"""
        return self.repository.get_by_vehicle(db, vehicle_id, skip, limit)
    
    def get_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por estado"""
        return self.repository.get_by_status(db, status, skip, limit)
    
    def get_by_tracking_code(self, db: Session, tracking_code: str) -> Optional[Order]:
        """Obtiene pedido por código de seguimiento"""
        return self.repository.get_by_tracking_code(db, tracking_code)
    
    def get_by_order_number(self, db: Session, order_number: str) -> Optional[Order]:
        """Obtiene pedido por número de pedido"""
        return self.repository.get_by_order_number(db, order_number)
    
    def get_unassigned(self, db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos sin asignar"""
        return self.repository.get_unassigned(db, skip, limit)
    
    def get_by_date_range(self, db: Session, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por rango de fechas"""
        return self.repository.get_by_date_range(db, start_date, end_date, skip, limit)
    
    def get_by_city(self, db: Session, city: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene pedidos por ciudad"""
        return self.repository.get_by_city(db, city, skip, limit)
    
    def assign_driver_and_vehicle(self, db: Session, order_id: int, assignment: OrderAssignment) -> Optional[Order]:
        """Asigna conductor y vehículo a un pedido"""
        return self.repository.assign_driver_and_vehicle(
            db, order_id, assignment.driver_id, assignment.vehicle_id, assignment.tracking_code
        )
    
    def update_status(self, db: Session, order_id: int, status: str) -> Optional[Order]:
        """Actualiza el estado de un pedido"""
        return self.repository.update_status(db, order_id, status)
    
    def get_order_with_details(self, db: Session, order_id: int) -> Optional[dict]:
        """Obtiene un pedido con detalles completos"""
        order = self.repository.get_by_id(db, order_id)
        if not order:
            return None
        
        # Obtener detalles del cliente
        client_info = {}
        if order.client:
            client_info = {
                "client_name": f"{order.client.name}",
                "client_email": order.client.email,
                "client_phone": order.client.phone
            }
        
        # Obtener detalles del conductor
        driver_info = {}
        if order.driver:
            driver_info = {
                "driver_name": f"{order.driver.first_name} {order.driver.last_name}",
                "driver_phone": order.driver.phone
            }
        
        # Obtener detalles del vehículo
        vehicle_info = {}
        if order.vehicle:
            vehicle_info = {
                "vehicle_license_plate": order.vehicle.license_plate,
                "vehicle_brand": order.vehicle.brand,
                "vehicle_model": order.vehicle.model
            }
        
        # Combinar toda la información
        order_dict = {
            "id": order.id,
            "order_number": order.order_number,
            "client_id": order.client_id,
            "driver_id": order.driver_id,
            "vehicle_id": order.vehicle_id,
            "origin_address": order.origin_address,
            "destination_address": order.destination_address,
            "origin_city": order.origin_city,
            "destination_city": order.destination_city,
            "description": order.description,
            "weight": order.weight,
            "volume": order.volume,
            "value": order.value,
            "status": order.status,
            "priority": order.priority,
            "delivery_date": order.delivery_date,
            "delivered_date": order.delivered_date,
            "notes": order.notes,
            "tracking_code": order.tracking_code,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "is_active": order.is_active,
            **client_info,
            **driver_info,
            **vehicle_info
        }
        
        return order_dict
    
    def _generate_order_number(self, db: Session) -> str:
        """Genera un número de pedido único"""
        import random
        import string
        
        while True:
            # Generar número con formato: ORD-YYYYMMDD-XXXX
            today = datetime.now().strftime("%Y%m%d")
            random_suffix = ''.join(random.choices(string.digits, k=4))
            order_number = f"ORD-{today}-{random_suffix}"
            
            # Verificar que no exista
            if not self.repository.get_by_order_number(db, order_number):
                return order_number
    
    def _generate_tracking_code(self, db: Session) -> str:
        """Genera un código de seguimiento único"""
        import random
        import string
        
        while True:
            # Generar código con formato: TRK-XXXXXXXXXXXX
            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            tracking_code = f"TRK-{random_code}"
            
            # Verificar que no exista
            if not self.repository.get_by_tracking_code(db, tracking_code):
                return tracking_code
