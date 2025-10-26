"""
Rutas simples para direcciones
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_address_service
from app.services.address_service import AddressService
from app.schemas.address_schemas import AddressCreate, AddressUpdate, AddressResponse, AddressSummary

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.get("/", response_model=List[AddressSummary])
async def get_addresses(
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene lista de direcciones"""
    try:
        addresses = address_service.get_all(db, skip=0, limit=100)
        return addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/", response_model=AddressResponse)
async def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Crea una nueva dirección"""
    try:
        # Verificar que el cliente existe
        from app.services.client_service import ClientService
        client_service = ClientService()
        client = client_service.get_by_id(db, address_data.client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Si es dirección principal, marcar otras como no principales
        if address_data.is_primary:
            from app.repositories.address_repository import AddressRepository
            address_repo = AddressRepository()
            existing_addresses = address_repo.get_by_client_id(db, address_data.client_id)
            for addr in existing_addresses:
                addr.is_primary = False
            db.commit()
        
        address = address_service.create(db, **address_data.model_dump())
        return address
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene una dirección por ID"""
    try:
        address = address_service.get_by_id(db, address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        return address
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/client/{client_id}", response_model=List[AddressSummary])
async def get_addresses_by_client(
    client_id: int,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene direcciones por cliente"""
    try:
        addresses = address_service.get_by_client_id(db, client_id)
        return addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/city/{city}", response_model=List[AddressSummary])
async def get_addresses_by_city(
    city: str,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Obtiene direcciones por ciudad"""
    try:
        addresses = address_service.get_by_city(db, city)
        return addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Actualiza una dirección"""
    try:
        # Verificar que la dirección existe
        existing_address = address_service.get_by_id(db, address_id)
        if not existing_address:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        
        # Si se está marcando como principal, desmarcar otras direcciones del mismo cliente
        if address_data.is_primary is True:
            from app.repositories.address_repository import AddressRepository
            address_repo = AddressRepository()
            existing_addresses = address_repo.get_by_client_id(db, existing_address.client_id)
            for addr in existing_addresses:
                if addr.id != address_id:
                    addr.is_primary = False
            db.commit()
        
        # Actualizar solo los campos proporcionados
        update_data = address_data.model_dump(exclude_unset=True)
        updated_address = address_service.update(db, address_id, **update_data)
        return updated_address
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{address_id}")
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service)
):
    """Elimina una dirección (soft delete)"""
    try:
        # Verificar que la dirección existe
        existing_address = address_service.get_by_id(db, address_id)
        if not existing_address:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        
        # Realizar eliminación lógica
        success = address_service.delete(db, address_id)
        if success:
            return {"message": "Dirección eliminada exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar la dirección")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")