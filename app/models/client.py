"""
Modelo de Cliente para el sistema de rutas logísticas

Este módulo define el modelo de datos para los clientes del sistema,
incluyendo información de contacto y clasificación por tipo.
"""
from sqlalchemy import Column, String, Boolean
from .base import BaseModel


class Client(BaseModel):
    """
    Modelo de Cliente
    
    Representa un cliente en el sistema logístico con información de contacto
    y clasificación necesaria para la gestión de entregas y servicios.
    
    Atributos:
        name (str): Nombre del cliente o empresa
        email (str): Email del cliente (único)
        phone (str): Teléfono del cliente
        company (str): Nombre de la empresa (opcional para clientes individuales)
        client_type (str): Tipo de cliente (individual, empresa)
        status (str): Estado del cliente (activo, inactivo, suspendido)
        is_active (bool): Indica si el cliente está activo en el sistema
    """
    __tablename__ = "clients"
    
    name = Column(String(200), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    company = Column(String(200), nullable=True)
    client_type = Column(String(20), default="individual", nullable=False)
    status = Column(String(20), default="activo", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)