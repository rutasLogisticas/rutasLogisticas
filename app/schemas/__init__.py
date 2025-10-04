# Módulo de esquemas Pydantic para validación de datos
from .vehicle_schemas import *
from .driver_schemas import *
from .client_schemas import *
from .address_schemas import *
from .base_schemas import *

__all__ = [
    # Base schemas
    'BaseSchema',
    'BaseCreateSchema',
    'BaseUpdateSchema',
    'BaseResponseSchema',
    'PaginatedResponse',
    
    # Vehicle schemas
    'VehicleCreate',
    'VehicleUpdate',
    'VehicleResponse',
    'VehicleSummary',
    
    # Driver schemas
    'DriverCreate',
    'DriverUpdate',
    'DriverResponse',
    'DriverSummary',
    
    # Client schemas
    'ClientCreate',
    'ClientUpdate',
    'ClientResponse',
    'ClientSummary',
    
    # Address schemas
    'AddressCreate',
    'AddressUpdate',
    'AddressResponse',
    'AddressSummary',
]
