"""
Modelo de Pedido simplificado para el sistema de rutas logísticas

Este módulo define el modelo de datos para los pedidos del sistema,
relacionando directamente cliente, conductor, vehículo con información de origen y destino.
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from .base import BaseModel


class Order(BaseModel):
    """
    Modelo de Pedido Simplificado
    
    Representa un pedido en el sistema logístico con información de origen,
    destino, cliente, conductor y vehículo asignado.
    
    Atributos:
        order_number (str): Número único del pedido
        client_id (int): ID del cliente que realiza el pedido
        driver_id (int): ID del conductor asignado (opcional inicialmente)
        vehicle_id (int): ID del vehículo asignado (opcional inicialmente)
        origin_address (str): Dirección de origen
        destination_address (str): Dirección de destino
        origin_city (str): Ciudad de origen
        destination_city (str): Ciudad de destino
        description (str): Descripción del pedido
        weight (float): Peso del pedido en kg
        volume (float): Volumen del pedido en m³
        value (float): Valor del pedido
        status (str): Estado del pedido (pendiente, asignado, en_transito, entregado, cancelado)
        priority (str): Prioridad del pedido (baja, media, alta, urgente)
        delivery_date (DateTime): Fecha programada de entrega
        delivered_date (DateTime): Fecha real de entrega
        notes (str): Notas adicionales sobre el pedido
        tracking_code (str): Código de seguimiento único
        
    Relaciones:
        client: Relación con el modelo Client
        driver: Relación con el modelo Driver
        vehicle: Relación con el modelo Vehicle
    """
    __tablename__ = "orders"
    
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True, index=True)
    origin_address = Column(String(300), nullable=False)
    destination_address = Column(String(300), nullable=False)
    origin_city = Column(String(100), nullable=False, index=True)
    destination_city = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    weight = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    value = Column(Numeric(10, 2), nullable=True)
    status = Column(String(20), default="pendiente", nullable=False)
    priority = Column(String(20), default="media", nullable=False)
    delivery_date = Column(DateTime, nullable=True)
    delivered_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    tracking_code = Column(String(50), unique=True, nullable=True, index=True)
    
    # Relaciones
    client = relationship("Client", backref="orders")
    driver = relationship("Driver", backref="orders")
    vehicle = relationship("Vehicle", backref="orders")
