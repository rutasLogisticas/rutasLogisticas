"""
Modelo de Conductor para el sistema de rutas logísticas

Este módulo define el modelo de datos para los conductores de la flota,
incluyendo información personal y profesional necesaria para la gestión.
"""
from sqlalchemy import Column, String, Boolean
from .base import BaseModel


class Driver(BaseModel):
    """
    Modelo de Conductor
    
    Representa un conductor en el sistema logístico con información personal
    y profesional necesaria para la asignación de vehículos y rutas.
    
    Atributos:
        first_name (str): Nombre del conductor
        last_name (str): Apellido del conductor
        email (str): Email del conductor (único)
        phone (str): Teléfono del conductor
        document_number (str): Número de documento (único)
        license_type (str): Tipo de licencia (A, B, C, etc.)
        status (str): Estado actual (disponible, en_ruta, etc.)
        is_available (bool): Indica si el conductor está disponible
    """
    __tablename__ = "drivers"
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    document_number = Column(String(20), unique=True, nullable=False, index=True)
    license_type = Column(String(10), nullable=False)
    status = Column(String(20), default="disponible", nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)