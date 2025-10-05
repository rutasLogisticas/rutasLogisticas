"""
Modelo de Vehículo para el sistema de rutas logísticas

Este módulo define el modelo de datos para los vehículos de la flota,
incluyendo información básica como placa, marca, modelo y estado.
"""
from sqlalchemy import Column, String, Integer, Boolean
from .base import BaseModel


class Vehicle(BaseModel):
    """
    Modelo de Vehículo
    
    Representa un vehículo en la flota logística con información básica
    necesaria para la gestión de rutas y asignaciones.
    
    Atributos:
        license_plate (str): Placa del vehículo (única)
        brand (str): Marca del vehículo
        model (str): Modelo del vehículo
        year (int): Año del vehículo
        vehicle_type (str): Tipo de vehículo (camioneta, furgon, etc.)
        status (str): Estado actual (disponible, en_ruta, mantenimiento, etc.)
        is_available (bool): Indica si el vehículo está disponible para uso
    """
    __tablename__ = "vehicles"
    
    license_plate = Column(String(20), unique=True, nullable=False, index=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    vehicle_type = Column(String(20), nullable=False)
    status = Column(String(20), default="disponible", nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
