"""
Rutas simples para vehículos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_vehicle_service
from app.services.vehicle_service import VehicleService
from app.schemas.vehicle_schemas import VehicleCreate, VehicleUpdate, VehicleResponse, VehicleSummary

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=List[VehicleSummary])
async def get_vehicles(
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Obtiene lista de vehículos"""
    try:
        vehicles = vehicle_service.get_all(db, skip=0, limit=100)
        return vehicles
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/", response_model=VehicleResponse)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Crea un nuevo vehículo"""
    try:
        # Verificar si la placa ya existe
        existing = vehicle_service.get_by_license_plate(db, vehicle_data.license_plate)
        if existing:
            raise HTTPException(status_code=400, detail="Ya existe un vehículo con esta placa")
        
        vehicle = vehicle_service.create(db, **vehicle_data.model_dump())
        return vehicle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Obtiene un vehículo por ID"""
    try:
        vehicle = vehicle_service.get_by_id(db, vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return vehicle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Actualiza un vehículo"""
    try:
        # Verificar que el vehículo existe
        existing_vehicle = vehicle_service.get_by_id(db, vehicle_id)
        if not existing_vehicle:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        
        # Actualizar solo los campos proporcionados
        update_data = vehicle_data.model_dump(exclude_unset=True)
        updated_vehicle = vehicle_service.update(db, vehicle_id, **update_data)
        return updated_vehicle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    """Elimina un vehículo (soft delete)"""
    try:
        # Verificar que el vehículo existe
        existing_vehicle = vehicle_service.get_by_id(db, vehicle_id)
        if not existing_vehicle:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        
        # Realizar eliminación lógica
        success = vehicle_service.delete(db, vehicle_id)
        if success:
            return {"message": "Vehículo eliminado exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar el vehículo")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")