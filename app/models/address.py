"""
Modelo de Dirección para el sistema de rutas logísticas

Este módulo define el modelo de datos para las direcciones de clientes,
estableciendo la relación con clientes para la gestión de entregas.
"""
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class Address(BaseModel):
    """
    Modelo de Dirección
    
    Representa una dirección asociada a un cliente en el sistema logístico,
    necesaria para la planificación de rutas y entregas.
    
    Atributos:
        client_id (int): ID del cliente propietario de la dirección
        street (str): Dirección de la calle
        city (str): Ciudad
        state (str): Estado o departamento
        postal_code (str): Código postal
        country (str): País (por defecto: Colombia)
        address_type (str): Tipo de dirección (principal, entrega, oficina, etc.)
        is_primary (bool): Indica si es la dirección principal del cliente
        
    Relaciones:
        client: Relación con el modelo Client
    """
    __tablename__ = "addresses"
    
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    street = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default="Colombia", nullable=False)
    address_type = Column(String(20), default="principal", nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    
    # Relación
    client = relationship("Client", backref="addresses")