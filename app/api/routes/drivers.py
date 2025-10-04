"""
Endpoints para gestión de conductores
Implementa principio SRP y separación de responsabilidades
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_driver_service
from app.services.driver_service import DriverService
from app.schemas.driver_schemas import (
    DriverCreate, DriverUpdate, DriverResponse, DriverSummary,
    DriverStatusUpdate, DriverAvailabilityUpdate, DriverLicenseFilter, DriverAgeFilter
)
from app.schemas.base_schemas import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/", response_model=DriverResponse, status_code=201)
async def create_driver(
    driver_data: DriverCreate,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Crea un nuevo conductor"""
    try:
        # Verificar si el email ya existe
        existing_driver = driver_service.get_by_email(db, driver_data.email)
        if existing_driver:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un conductor con este email"
            )
        
        # Verificar si el documento ya existe
        existing_driver = driver_service.get_by_document_number(db, driver_data.document_number)
        if existing_driver:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un conductor con este número de documento"
            )
        
        # Verificar si la licencia ya existe
        existing_driver = driver_service.get_by_license_number(db, driver_data.license_number)
        if existing_driver:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un conductor con este número de licencia"
            )
        
        driver = driver_service.create_driver(db, **driver_data.dict())
        return driver
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=PaginatedResponse[DriverSummary])
async def get_drivers(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    license_type: Optional[str] = Query(None, description="Filtrar por tipo de licencia"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    available_only: bool = Query(False, description="Solo conductores disponibles"),
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Obtiene lista paginada de conductores"""
    try:
        skip = (page - 1) * size
        
        if available_only:
            drivers = driver_service.get_available_drivers(db, skip, size)
            total = len(drivers)  # Aproximación
        elif license_type:
            from app.models.driver import LicenseType
            drivers = driver_service.get_drivers_by_license_type(db, LicenseType(license_type), skip, size)
            total = driver_service.get_count(db)
        elif status:
            from app.models.driver import DriverStatus
            drivers = driver_service.get_drivers_by_status(db, DriverStatus(status), skip, size)
            total = driver_service.get_count(db)
        else:
            drivers = driver_service.get_all(db, skip, size)
            total = driver_service.get_count(db)
        
        driver_summaries = [DriverSummary.from_orm(driver) for driver in drivers]
        return PaginatedResponse.create(driver_summaries, total, page, size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Obtiene un conductor por ID"""
    driver = driver_service.get_by_id(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return driver


@router.put("/{driver_id}", response_model=DriverResponse)
async def update_driver(
    driver_id: int,
    driver_data: DriverUpdate,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Actualiza un conductor"""
    try:
        # Verificar email único si se proporciona
        if driver_data.email:
            existing_driver = driver_service.get_by_email(db, driver_data.email)
            if existing_driver and existing_driver.id != driver_id:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un conductor con este email"
                )
        
        # Verificar documento único si se proporciona
        if driver_data.document_number:
            existing_driver = driver_service.get_by_document_number(db, driver_data.document_number)
            if existing_driver and existing_driver.id != driver_id:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un conductor con este número de documento"
                )
        
        # Verificar licencia única si se proporciona
        if driver_data.license_number:
            existing_driver = driver_service.get_by_license_number(db, driver_data.license_number)
            if existing_driver and existing_driver.id != driver_id:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un conductor con este número de licencia"
                )
        
        driver = driver_service.update(db, driver_id, **driver_data.dict(exclude_unset=True))
        if not driver:
            raise HTTPException(status_code=404, detail="Conductor no encontrado")
        return driver
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{driver_id}", response_model=SuccessResponse)
async def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Elimina un conductor (eliminación lógica)"""
    try:
        success = driver_service.delete(db, driver_id)
        if not success:
            raise HTTPException(status_code=404, detail="Conductor no encontrado")
        return SuccessResponse(message="Conductor eliminado exitosamente")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{driver_id}/status", response_model=DriverResponse)
async def update_driver_status(
    driver_id: int,
    status_data: DriverStatusUpdate,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Actualiza el estado de un conductor"""
    try:
        driver = driver_service.update_driver_status(db, driver_id, status_data.status)
        if not driver:
            raise HTTPException(status_code=404, detail="Conductor no encontrado")
        return driver
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{driver_id}/availability", response_model=DriverResponse)
async def update_driver_availability(
    driver_id: int,
    availability_data: DriverAvailabilityUpdate,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Actualiza la disponibilidad de un conductor"""
    try:
        driver = driver_service.set_availability(db, driver_id, availability_data.is_available)
        if not driver:
            raise HTTPException(status_code=404, detail="Conductor no encontrado")
        return driver
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/search", response_model=PaginatedResponse[DriverSummary])
async def search_drivers(
    query: str = Query(..., min_length=2, description="Término de búsqueda"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Busca conductores por múltiples campos"""
    try:
        skip = (page - 1) * size
        drivers = driver_service.search_drivers(db, query, skip, size)
        
        driver_summaries = [DriverSummary.from_orm(driver) for driver in drivers]
        return PaginatedResponse.create(driver_summaries, len(drivers), page, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/filter/license", response_model=PaginatedResponse[DriverSummary])
async def filter_drivers_by_license(
    filter_data: DriverLicenseFilter,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Filtra conductores por licencia"""
    try:
        skip = (filter_data.page - 1) * filter_data.size
        
        if filter_data.license_type and filter_data.status:
            from app.models.driver import LicenseType, DriverStatus
            drivers = driver_service.filter_by(db, {
                'license_type': filter_data.license_type,
                'status': filter_data.status
            }, skip, filter_data.size)
        elif filter_data.license_type:
            from app.models.driver import LicenseType
            drivers = driver_service.get_drivers_by_license_type(db, filter_data.license_type, skip, filter_data.size)
        elif filter_data.status:
            from app.models.driver import DriverStatus
            drivers = driver_service.get_drivers_by_status(db, filter_data.status, skip, filter_data.size)
        else:
            drivers = driver_service.get_all(db, skip, filter_data.size)
        
        driver_summaries = [DriverSummary.from_orm(driver) for driver in drivers]
        return PaginatedResponse.create(driver_summaries, len(drivers), filter_data.page, filter_data.size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/filter/age", response_model=PaginatedResponse[DriverSummary])
async def filter_drivers_by_age(
    filter_data: DriverAgeFilter,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Filtra conductores por rango de edad"""
    try:
        skip = (filter_data.page - 1) * filter_data.size
        drivers = driver_service.get_drivers_by_age_range(
            db, filter_data.min_age, filter_data.max_age, skip, filter_data.size
        )
        
        driver_summaries = [DriverSummary.from_orm(driver) for driver in drivers]
        return PaginatedResponse.create(driver_summaries, len(drivers), filter_data.page, filter_data.size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{driver_id}/summary")
async def get_driver_summary(
    driver_id: int,
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Obtiene resumen completo de un conductor"""
    try:
        summary = driver_service.get_driver_summary(db, driver_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Conductor no encontrado")
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/alerts/license-expiry")
async def get_license_expiry_alerts(
    days_ahead: int = Query(30, ge=1, le=365, description="Días hacia adelante"),
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Obtiene conductores con licencias próximas a expirar"""
    try:
        drivers = driver_service.check_license_expiry_alerts(db, days_ahead)
        return {
            "drivers": [DriverSummary.from_orm(driver) for driver in drivers],
            "count": len(drivers),
            "days_ahead": days_ahead
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/statistics/overview")
async def get_driver_statistics(
    db: Session = Depends(get_db),
    driver_service: DriverService = Depends(get_driver_service)
):
    """Obtiene estadísticas de conductores"""
    try:
        stats = driver_service.get_driver_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
