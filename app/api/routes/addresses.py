"""
Endpoints para gestión de direcciones
Implementa principio SRP y separación de responsabilidades
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_address_service
from app.services.address_service import AddressService
from app.schemas.address_schemas import (
    AddressCreate, AddressUpdate, AddressResponse, AddressSummary,
    AddressPrimaryUpdate, AddressDeliveryUpdate, AddressCoordinatesUpdate, AddressFilter
)
from app.schemas.base_schemas import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post("/", response_model=AddressResponse, status_code=201)
async def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Crea una nueva dirección"""
    try:
        # Validar datos de dirección
        validated_data = address_service.validate_address_data(address_data.dict())
        address = address_service.create_address(db, **validated_data)
        return address
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=PaginatedResponse[AddressSummary])
async def get_addresses(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    client_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    address_type: Optional[str] = Query(None, description="Filtrar por tipo"),
    city: Optional[str] = Query(None, description="Filtrar por ciudad"),
    delivery_available: Optional[bool] = Query(None, description="Filtrar por disponibilidad de entrega"),
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene lista paginada de direcciones"""
    try:
        skip = (page - 1) * size
        
        if client_id:
            if address_type:
                from app.models.address import AddressType
                addresses = address_service.get_by_type(db, client_id, AddressType(address_type), skip, size)
            elif delivery_available is not None:
                if delivery_available:
                    addresses = address_service.get_delivery_addresses(db, client_id, skip, size)
                else:
                    addresses = address_service.get_by_client_id(db, client_id, skip, size)
            else:
                addresses = address_service.get_by_client_id(db, client_id, skip, size)
            total = len(addresses)
        elif city:
            addresses = address_service.get_addresses_by_city(db, city, skip, size)
            total = len(addresses)
        else:
            addresses = address_service.get_all(db, skip, size)
            total = address_service.get_count(db)
        
        address_summaries = [AddressSummary.from_orm(address) for address in addresses]
        return PaginatedResponse.create(address_summaries, total, page, size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene una dirección por ID"""
    address = address_service.get_by_id(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return address


@router.put("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Actualiza una dirección"""
    try:
        address = address_service.update(db, address_id, **address_data.dict(exclude_unset=True))
        if not address:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        return address
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{address_id}", response_model=SuccessResponse)
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Elimina una dirección (eliminación lógica)"""
    try:
        success = address_service.delete(db, address_id)
        if not success:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        return SuccessResponse(message="Dirección eliminada exitosamente")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{address_id}/primary", response_model=SuccessResponse)
async def set_primary_address(
    address_id: int,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Establece una dirección como principal"""
    try:
        address = address_service.get_by_id(db, address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        
        success = address_service.set_primary_address(db, address.client_id, address_id)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo establecer como dirección principal")
        
        return SuccessResponse(message="Dirección establecida como principal")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{address_id}/delivery", response_model=AddressResponse)
async def update_delivery_availability(
    address_id: int,
    delivery_data: AddressDeliveryUpdate,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Actualiza la disponibilidad de entrega de una dirección"""
    try:
        address = address_service.set_delivery_availability(db, address_id, delivery_data.is_delivery_available)
        if not address:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        return address
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{address_id}/coordinates", response_model=AddressResponse)
async def update_coordinates(
    address_id: int,
    coordinates_data: AddressCoordinatesUpdate,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Actualiza las coordenadas de una dirección"""
    try:
        address = address_service.update_coordinates(
            db, address_id, coordinates_data.latitude, coordinates_data.longitude
        )
        if not address:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        return address
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/client/{client_id}/primary")
async def get_primary_address(
    client_id: int,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene la dirección principal de un cliente"""
    try:
        address = address_service.get_primary_address(db, client_id)
        if not address:
            raise HTTPException(status_code=404, detail="Cliente no tiene dirección principal")
        return address
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/client/{client_id}/delivery")
async def get_delivery_addresses(
    client_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene direcciones disponibles para entrega de un cliente"""
    try:
        skip = (page - 1) * size
        addresses = address_service.get_delivery_addresses(db, client_id, skip, size)
        
        address_summaries = [AddressSummary.from_orm(address) for address in addresses]
        return PaginatedResponse.create(address_summaries, len(addresses), page, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/search", response_model=PaginatedResponse[AddressSummary])
async def search_addresses(
    query: str = Query(..., min_length=2, description="Término de búsqueda"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Busca direcciones por múltiples campos"""
    try:
        skip = (page - 1) * size
        addresses = address_service.search_addresses(db, query, skip, size)
        
        address_summaries = [AddressSummary.from_orm(address) for address in addresses]
        return PaginatedResponse.create(address_summaries, len(addresses), page, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/filter", response_model=PaginatedResponse[AddressSummary])
async def filter_addresses(
    filter_data: AddressFilter,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Filtra direcciones por múltiples criterios"""
    try:
        skip = (filter_data.page - 1) * filter_data.size
        
        filters = {}
        if filter_data.client_id:
            filters['client_id'] = filter_data.client_id
        if filter_data.address_type:
            filters['address_type'] = filter_data.address_type
        if filter_data.city:
            filters['city'] = filter_data.city
        if filter_data.state:
            filters['state'] = filter_data.state
        if filter_data.is_primary is not None:
            filters['is_primary'] = filter_data.is_primary
        if filter_data.is_delivery_available is not None:
            filters['is_delivery_available'] = filter_data.is_delivery_available
        if filter_data.has_coordinates is not None:
            filters['has_coordinates'] = filter_data.has_coordinates
        if filter_data.parking_available is not None:
            filters['parking_available'] = filter_data.parking_available
        
        if filters:
            addresses = address_service.filter_by(db, filters, skip, filter_data.size)
        else:
            addresses = address_service.get_all(db, skip, filter_data.size)
        
        address_summaries = [AddressSummary.from_orm(address) for address in addresses]
        return PaginatedResponse.create(address_summaries, len(addresses), filter_data.page, filter_data.size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{address_id}/summary")
async def get_address_summary(
    address_id: int,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene resumen completo de una dirección"""
    try:
        summary = address_service.get_address_summary(db, address_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/statistics/overview")
async def get_address_statistics(
    client_id: Optional[int] = Query(None, description="ID del cliente para estadísticas específicas"),
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene estadísticas de direcciones"""
    try:
        stats = address_service.get_address_statistics(db, client_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
