"""
Endpoints para gestión de vehículos
Implementa principio SRP y separación de responsabilidades
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_vehicle_service
from app.services.vehicle_service import VehicleService
from app.schemas.vehicle_schemas import (
    VehicleCreate, VehicleUpdate, VehicleResponse, VehicleSummary,
    VehicleStatusUpdate, VehicleAvailabilityUpdate, VehicleCapacityFilter
)
from app.schemas.base_schemas import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("/", response_model=VehicleResponse, status_code=201)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Crea un nuevo vehículo"""
    try:
        # Verificar si la placa ya existe
        existing_vehicle = vehicle_service.get_by_license_plate(db, vehicle_data.license_plate)
        if existing_vehicle:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un vehículo con esta placa"
            )
        
        vehicle = vehicle_service.create_vehicle(db, **vehicle_data.dict())
        return vehicle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=PaginatedResponse[VehicleSummary])
async def get_vehicles(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    vehicle_type: Optional[str] = Query(None, description="Filtrar por tipo de vehículo"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    available_only: bool = Query(False, description="Solo vehículos disponibles"),
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Obtiene lista paginada de vehículos"""
    try:
        skip = (page - 1) * size
        
        if available_only:
            vehicles = vehicle_service.get_available_vehicles(db, skip, size)
            total = len(vehicles)  # Aproximación para vehículos disponibles
        elif vehicle_type:
            from app.models.vehicle import VehicleType
            vehicles = vehicle_service.get_vehicles_by_type(db, VehicleType(vehicle_type), skip, size)
            total = vehicle_service.get_count(db)  # Aproximación
        elif status:
            from app.models.vehicle import VehicleStatus
            vehicles = vehicle_service.get_vehicles_by_status(db, VehicleStatus(status), skip, size)
            total = vehicle_service.get_count(db)  # Aproximación
        else:
            vehicles = vehicle_service.get_all(db, skip, size)
            total = vehicle_service.get_count(db)
        
        vehicle_summaries = [VehicleSummary.from_orm(vehicle) for vehicle in vehicles]
        return PaginatedResponse.create(vehicle_summaries, total, page, size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Obtiene un vehículo por ID"""
    vehicle = vehicle_service.get_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehicle


@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Actualiza un vehículo"""
    try:
        # Verificar si la placa ya existe en otro vehículo
        if vehicle_data.license_plate:
            existing_vehicle = vehicle_service.get_by_license_plate(db, vehicle_data.license_plate)
            if existing_vehicle and existing_vehicle.id != vehicle_id:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un vehículo con esta placa"
                )
        
        vehicle = vehicle_service.update(db, vehicle_id, **vehicle_data.dict(exclude_unset=True))
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return vehicle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{vehicle_id}", response_model=SuccessResponse)
async def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Elimina un vehículo (eliminación lógica)"""
    try:
        success = vehicle_service.delete(db, vehicle_id)
        if not success:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return SuccessResponse(message="Vehículo eliminado exitosamente")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{vehicle_id}/status", response_model=VehicleResponse)
async def update_vehicle_status(
    vehicle_id: int,
    status_data: VehicleStatusUpdate,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Actualiza el estado de un vehículo"""
    try:
        vehicle = vehicle_service.update_vehicle_status(db, vehicle_id, status_data.status)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return vehicle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{vehicle_id}/availability", response_model=VehicleResponse)
async def update_vehicle_availability(
    vehicle_id: int,
    availability_data: VehicleAvailabilityUpdate,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Actualiza la disponibilidad de un vehículo"""
    try:
        vehicle = vehicle_service.set_availability(db, vehicle_id, availability_data.is_available)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return vehicle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/search", response_model=PaginatedResponse[VehicleSummary])
async def search_vehicles(
    query: str = Query(..., min_length=2, description="Término de búsqueda"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Busca vehículos por múltiples campos"""
    try:
        skip = (page - 1) * size
        vehicles = vehicle_service.search_vehicles(db, query, skip, size)
        total = len(vehicles)  # Aproximación para búsquedas
        
        vehicle_summaries = [VehicleSummary.from_orm(vehicle) for vehicle in vehicles]
        return PaginatedResponse.create(vehicle_summaries, total, page, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/filter/capacity", response_model=PaginatedResponse[VehicleSummary])
async def filter_vehicles_by_capacity(
    filter_data: VehicleCapacityFilter,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Filtra vehículos por capacidad"""
    try:
        skip = (filter_data.page - 1) * filter_data.size
        vehicles = vehicle_service.get_vehicles_by_capacity(
            db, 
            filter_data.min_weight, 
            filter_data.min_volume, 
            skip, 
            filter_data.size
        )
        
        vehicle_summaries = [VehicleSummary.from_orm(vehicle) for vehicle in vehicles]
        return PaginatedResponse.create(vehicle_summaries, len(vehicles), filter_data.page, filter_data.size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{vehicle_id}/summary")
async def get_vehicle_summary(
    vehicle_id: int,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Obtiene resumen completo de un vehículo"""
    try:
        summary = vehicle_service.get_vehicle_summary(db, vehicle_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/statistics/overview")
async def get_vehicle_statistics(
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Obtiene estadísticas de vehículos"""
    try:
        stats = vehicle_service.get_vehicle_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
