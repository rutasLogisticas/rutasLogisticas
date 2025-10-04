"""
Endpoints para gestión de clientes
Implementa principio SRP y separación de responsabilidades
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_client_service
from app.services.client_service import ClientService
from app.schemas.client_schemas import (
    ClientCreate, ClientUpdate, ClientResponse, ClientSummary,
    ClientStatusUpdate, ClientPriorityUpdate, ClientNotificationUpdate,
    ClientCommercialUpdate, ClientFilter
)
from app.schemas.base_schemas import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/", response_model=ClientResponse, status_code=201)
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Crea un nuevo cliente"""
    try:
        # Verificar si el email ya existe
        if client_data.email:
            existing_client = client_service.get_by_email(db, client_data.email)
            if existing_client:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un cliente con este email"
                )
        
        # Verificar si el ID fiscal ya existe
        if client_data.tax_id:
            existing_client = client_service.get_by_tax_id(db, client_data.tax_id)
            if existing_client:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un cliente con este ID fiscal"
                )
        
        client = client_service.create_client(db, **client_data.dict())
        return client
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=PaginatedResponse[ClientSummary])
async def get_clients(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    client_type: Optional[str] = Query(None, description="Filtrar por tipo de cliente"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    city: Optional[str] = Query(None, description="Filtrar por ciudad"),
    priority_only: bool = Query(False, description="Solo clientes prioritarios"),
    active_only: bool = Query(False, description="Solo clientes activos"),
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene lista paginada de clientes"""
    try:
        skip = (page - 1) * size
        
        if priority_only:
            clients = client_service.get_priority_clients(db, skip, size)
            total = len(clients)
        elif active_only:
            clients = client_service.get_active_clients(db, skip, size)
            total = len(clients)
        elif client_type:
            from app.models.client import ClientType
            clients = client_service.get_clients_by_type(db, ClientType(client_type), skip, size)
            total = client_service.get_count(db)
        elif status:
            from app.models.client import ClientStatus
            clients = client_service.get_clients_by_status(db, ClientStatus(status), skip, size)
            total = client_service.get_count(db)
        elif city:
            clients = client_service.get_clients_by_city(db, city, skip, size)
            total = len(clients)
        else:
            clients = client_service.get_all(db, skip, size)
            total = client_service.get_count(db)
        
        client_summaries = [ClientSummary.from_orm(client) for client in clients]
        return PaginatedResponse.create(client_summaries, total, page, size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene un cliente por ID"""
    client = client_service.get_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Actualiza un cliente"""
    try:
        # Verificar email único si se proporciona
        if client_data.email:
            existing_client = client_service.get_by_email(db, client_data.email)
            if existing_client and existing_client.id != client_id:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un cliente con este email"
                )
        
        # Verificar ID fiscal único si se proporciona
        if client_data.tax_id:
            existing_client = client_service.get_by_tax_id(db, client_data.tax_id)
            if existing_client and existing_client.id != client_id:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un cliente con este ID fiscal"
                )
        
        client = client_service.update(db, client_id, **client_data.dict(exclude_unset=True))
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return client
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{client_id}", response_model=SuccessResponse)
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Elimina un cliente (eliminación lógica)"""
    try:
        success = client_service.delete(db, client_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return SuccessResponse(message="Cliente eliminado exitosamente")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{client_id}/status", response_model=ClientResponse)
async def update_client_status(
    client_id: int,
    status_data: ClientStatusUpdate,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Actualiza el estado de un cliente"""
    try:
        client = client_service.update_client_status(db, client_id, status_data.status)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return client
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{client_id}/priority", response_model=ClientResponse)
async def update_client_priority(
    client_id: int,
    priority_data: ClientPriorityUpdate,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Actualiza la prioridad de un cliente"""
    try:
        client = client_service.set_priority(db, client_id, priority_data.is_priority)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return client
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{client_id}/notifications", response_model=ClientResponse)
async def update_client_notifications(
    client_id: int,
    notification_data: ClientNotificationUpdate,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Actualiza las notificaciones de un cliente"""
    try:
        client = client_service.set_notifications(db, client_id, notification_data.receives_notifications)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return client
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/{client_id}/commercial", response_model=ClientResponse)
async def update_client_commercial_info(
    client_id: int,
    commercial_data: ClientCommercialUpdate,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Actualiza la información comercial de un cliente"""
    try:
        client = client_service.update(db, client_id, **commercial_data.dict(exclude_unset=True))
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return client
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/search", response_model=PaginatedResponse[ClientSummary])
async def search_clients(
    query: str = Query(..., min_length=2, description="Término de búsqueda"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Busca clientes por múltiples campos"""
    try:
        skip = (page - 1) * size
        clients = client_service.search_clients(db, query, skip, size)
        
        client_summaries = [ClientSummary.from_orm(client) for client in clients]
        return PaginatedResponse.create(client_summaries, len(clients), page, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/filter", response_model=PaginatedResponse[ClientSummary])
async def filter_clients(
    filter_data: ClientFilter,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Filtra clientes por múltiples criterios"""
    try:
        skip = (filter_data.page - 1) * filter_data.size
        
        filters = {}
        if filter_data.client_type:
            filters['client_type'] = filter_data.client_type
        if filter_data.status:
            filters['status'] = filter_data.status
        if filter_data.city:
            filters['city'] = filter_data.city
        if filter_data.state:
            filters['state'] = filter_data.state
        if filter_data.is_priority is not None:
            filters['is_priority'] = filter_data.is_priority
        
        if filters:
            clients = client_service.filter_by(db, filters, skip, filter_data.size)
        else:
            clients = client_service.get_all(db, skip, filter_data.size)
        
        client_summaries = [ClientSummary.from_orm(client) for client in clients]
        return PaginatedResponse.create(client_summaries, len(clients), filter_data.page, filter_data.size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{client_id}/summary")
async def get_client_summary(
    client_id: int,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene resumen completo de un cliente"""
    try:
        summary = client_service.get_client_summary(db, client_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/by-tags/{tag}")
async def get_clients_by_tag(
    tag: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene clientes por tag"""
    try:
        skip = (page - 1) * size
        clients = client_service.get_clients_by_tags(db, tag, skip, size)
        
        client_summaries = [ClientSummary.from_orm(client) for client in clients]
        return PaginatedResponse.create(client_summaries, len(clients), page, size)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/statistics/overview")
async def get_client_statistics(
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene estadísticas de clientes"""
    try:
        stats = client_service.get_client_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
