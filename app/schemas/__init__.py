"""
Módulo de esquemas Pydantic para validación de datos
"""
from .vehicle_schemas import *
from .driver_schemas import *
from .client_schemas import *
from .address_schemas import *

__all__ = [
    # Vehicle schemas
    'VehicleCreate',
    'VehicleResponse',
    'VehicleSummary',
    
    # Driver schemas
    'DriverCreate',
    'DriverResponse',
    'DriverSummary',
    
    # Client schemas
    'ClientCreate',
    'ClientResponse',
    'ClientSummary',
    
    # Address schemas
    'AddressCreate',
    'AddressResponse',
    'AddressSummary',
]