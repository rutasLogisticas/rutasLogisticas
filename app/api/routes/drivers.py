"""
Rutas simples para conductores
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_driver_service
from app.services.driver_service import DriverService
from app.schemas.driver_schemas import DriverCreate, DriverResponse, DriverSummary

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.get("/", response_model=List[DriverSummary])
async def get_drivers(
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Obtiene lista de conductores"""
    try:
        drivers = driver_service.get_all(db, skip=0, limit=100)
        return drivers
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/", response_model=DriverResponse)
async def create_driver(
    driver_data: DriverCreate,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Crea un nuevo conductor"""
    try:
        # Verificar si el email ya existe
        existing = driver_service.get_by_email(db, driver_data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Ya existe un conductor con este email")
        
        # Verificar si el documento ya existe
        existing_doc = driver_service.get_by_document(db, driver_data.document_number)
        if existing_doc:
            raise HTTPException(status_code=400, detail="Ya existe un conductor con este documento")
        
        driver = driver_service.create(db, **driver_data.model_dump())
        return driver
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Obtiene un conductor por ID"""
    try:
        driver = driver_service.get_by_id(db, driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Conductor no encontrado")
        return driver
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/available/", response_model=List[DriverSummary])
async def get_available_drivers(
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Obtiene conductores disponibles"""
    try:
        drivers = driver_service.get_available_drivers(db, skip=0, limit=100)
        return drivers
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")