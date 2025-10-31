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
from app.services.directions_service import DirectionsService
from app.services.geocoding_service import GeocodingService


class OrderService(BaseService):
    """Servicio para manejar la lógica de negocio de pedidos"""
    
    def __init__(self):
        super().__init__()
        self.repository = OrderRepository()
        self.directions_service = DirectionsService()
        self.geocoding_service = GeocodingService()
    
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
    
    def get_order_route(self, db: Session, order_id: int, mode: str = "driving") -> Optional[dict]:
        """
        Obtiene la ruta calculada para un pedido específico
        
        Args:
            db: Sesión de base de datos
            order_id: ID del pedido
            mode: Modo de transporte (driving, walking, bicycling, transit)
            
        Returns:
            Dict con información del pedido y su ruta calculada
        """
        try:
            # Obtener el pedido con detalles
            order_details = self.get_order_with_details(db, order_id)
            if not order_details:
                return None
            
            # Obtener las direcciones del pedido
            origin_address = order_details["origin_address"]
            destination_address = order_details["destination_address"]
            
            # Mejorar direcciones agregando ciudad si falta
            origin_city = order_details.get("origin_city", "")
            destination_city = order_details.get("destination_city", "")
            
            # Si la dirección no incluye la ciudad, agregarla
            if origin_city and origin_city.lower() not in origin_address.lower():
                origin_address = f"{origin_address}, {origin_city}, Colombia"
            
            if destination_city and destination_city.lower() not in destination_address.lower():
                destination_address = f"{destination_address}, {destination_city}, Colombia"
            
            # Calcular la ruta usando DirectionsService
            try:
                route_response = self.directions_service.get_directions(
                    origin_address, 
                    destination_address, 
                    mode
                )
            except ValueError as e:
                error_msg = str(e)
                # Mensajes más claros para el usuario
                if "NOT_FOUND" in error_msg:
                    raise ValueError(f"No se pudo encontrar una ruta entre las direcciones proporcionadas. Verifica que las direcciones de origen ({order_details['origin_address']}) y destino ({order_details['destination_address']}) sean válidas.")
                elif "ZERO_RESULTS" in error_msg:
                    raise ValueError(f"No se encontró una ruta entre las direcciones. Puede que no exista una ruta {mode} entre estos puntos.")
                else:
                    raise ValueError(f"Error calculando ruta: {error_msg}")
            except Exception as e:
                raise ValueError(f"Error calculando ruta: {str(e)}")
            
            # Calcular tiempo estimado de entrega
            estimated_delivery_time = None
            if order_details.get("delivery_date"):
                # Si ya hay una fecha programada, usarla
                estimated_delivery_time = order_details["delivery_date"]
            else:
                # Calcular basado en la duración de la ruta
                from datetime import datetime, timedelta
                duration_text = route_response.duration_text
                # Extraer horas y minutos de la duración (formato: "2 horas 30 minutos")
                import re
                hours_match = re.search(r'(\d+)\s*hora', duration_text)
                minutes_match = re.search(r'(\d+)\s*minuto', duration_text)
                
                hours = int(hours_match.group(1)) if hours_match else 0
                minutes = int(minutes_match.group(1)) if minutes_match else 0
                
                estimated_delivery_time = datetime.now() + timedelta(hours=hours, minutes=minutes)
            
            # Combinar información del pedido con la ruta
            order_route = {
                "order": order_details,
                "route": {
                    "origin": route_response.origin,
                    "destination": route_response.destination,
                    "distance_text": route_response.distance_text,
                    "duration_text": route_response.duration_text,
                    "steps": [step.model_dump() for step in route_response.steps]
                },
                "estimated_delivery_time": estimated_delivery_time,
                "route_distance": route_response.distance_text,
                "route_duration": route_response.duration_text,
                "polyline": route_response.polyline
            }
            
            return order_route
            
        except Exception as e:
            raise ValueError(f"Error al calcular ruta del pedido: {str(e)}")
    
    def get_multiple_order_routes(self, db: Session, order_ids: List[int], mode: str = "driving") -> List[dict]:
        """
        Obtiene rutas para múltiples pedidos
        
        Args:
            db: Sesión de base de datos
            order_ids: Lista de IDs de pedidos
            mode: Modo de transporte
            
        Returns:
            Lista de diccionarios con información de pedidos y sus rutas
        """
        routes = []
        for order_id in order_ids:
            try:
                route = self.get_order_route(db, order_id, mode)
                if route:
                    routes.append(route)
            except Exception as e:
                # Log error pero continuar con otros pedidos
                print(f"Error calculando ruta para pedido {order_id}: {str(e)}")
                continue
        
        return routes
