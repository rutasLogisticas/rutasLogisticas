"""
Rutas simples para clientes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_client_service
from app.services.client_service import ClientService
from app.schemas.client_schemas import ClientCreate, ClientResponse, ClientSummary

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=List[ClientSummary])
async def get_clients(
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene lista de clientes"""
    try:
        clients = client_service.get_all(db, skip=0, limit=100)
        return clients
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Crea un nuevo cliente"""
    try:
        # Verificar si el email ya existe
        existing = client_service.get_by_email(db, client_data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Ya existe un cliente con este email")
        
        client = client_service.create(db, **client_data.model_dump())
        return client
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene un cliente por ID"""
    try:
        client = client_service.get_by_id(db, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return client
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/company/{company}", response_model=List[ClientSummary])
async def get_clients_by_company(
    company: str,
    db: Session = Depends(get_db),
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene clientes por empresa"""
    try:
        clients = client_service.get_by_company(db, company)
        return clients
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")