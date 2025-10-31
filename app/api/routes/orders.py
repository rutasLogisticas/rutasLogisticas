"""
Endpoints API para Pedidos

Este módulo define los endpoints REST para manejar pedidos.
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_order_service
from app.services.order_service import OrderService
from app.schemas.order_schemas import (
    OrderCreate, OrderUpdate, OrderResponse, OrderSummary, OrderWithDetails, OrderAssignment,
    OrderRouteResponse, MultipleOrderRoutesRequest
)

router = APIRouter(prefix="/orders", tags=["orders"])

# Manejar peticiones OPTIONS para CORS
@router.options("/{path:path}")
async def options_handler(path: str):
    """Maneja peticiones OPTIONS para CORS"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:4200",
            "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
        }
    )


@router.get("/", response_model=List[OrderSummary])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene lista de pedidos"""
    return order_service.get_all(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderWithDetails)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene un pedido por ID con detalles completos"""
    order_details = order_service.get_order_with_details(db, order_id)
    if not order_details:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order_details


@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Crea un nuevo pedido"""
    try:
        return order_service.create_order(db, order_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear pedido: {str(e)}")


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Actualiza un pedido"""
    order = order_service.update(db, order_id, **order_data.model_dump(exclude_unset=True))
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order


@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Elimina un pedido (soft delete)"""
    success = order_service.delete(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"message": "Pedido eliminado exitosamente"}


@router.get("/client/{client_id}", response_model=List[OrderSummary])
async def get_orders_by_client(
    client_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene pedidos por cliente"""
    return order_service.get_by_client(db, client_id, skip, limit)


@router.get("/driver/{driver_id}", response_model=List[OrderSummary])
async def get_orders_by_driver(
    driver_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene pedidos por conductor"""
    return order_service.get_by_driver(db, driver_id, skip, limit)


@router.get("/vehicle/{vehicle_id}", response_model=List[OrderSummary])
async def get_orders_by_vehicle(
    vehicle_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene pedidos por vehículo"""
    return order_service.get_by_vehicle(db, vehicle_id, skip, limit)


@router.get("/status/{status}", response_model=List[OrderSummary])
async def get_orders_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene pedidos por estado"""
    return order_service.get_by_status(db, status, skip, limit)


@router.get("/tracking/{tracking_code}", response_model=OrderWithDetails)
async def get_order_by_tracking(
    tracking_code: str,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene pedido por código de seguimiento"""
    order = order_service.get_by_tracking_code(db, tracking_code)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    order_details = order_service.get_order_with_details(db, order.id)
    return order_details


@router.get("/number/{order_number}", response_model=OrderWithDetails)
async def get_order_by_number(
    order_number: str,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene pedido por número de pedido"""
    order = order_service.get_by_order_number(db, order_number)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    order_details = order_service.get_order_with_details(db, order.id)
    return order_details


@router.get("/unassigned/list", response_model=List[OrderSummary])
async def get_unassigned_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene pedidos sin asignar"""
    return order_service.get_unassigned(db, skip, limit)


@router.get("/city/{city}", response_model=List[OrderSummary])
async def get_orders_by_city(
    city: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene pedidos por ciudad"""
    return order_service.get_by_city(db, city, skip, limit)


@router.post("/{order_id}/assign", response_model=OrderResponse)
async def assign_order(
    order_id: int,
    assignment: OrderAssignment,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Asigna conductor y vehículo a un pedido"""
    order = order_service.assign_driver_and_vehicle(db, order_id, assignment)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status: str = Query(..., description="Nuevo estado del pedido"),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Actualiza el estado de un pedido"""
    order = order_service.update_status(db, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order


@router.get("/{order_id}/route", response_model=OrderRouteResponse)
async def get_order_route(
    order_id: int,
    mode: str = Query("driving", description="Modo de transporte: driving, walking, bicycling, transit"),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene la ruta calculada para un pedido específico"""
    try:
        route_data = order_service.get_order_route(db, order_id, mode)
        if not route_data:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return route_data
    except ValueError as e:
        error_msg = str(e)
        # Determinar el código de estado según el tipo de error
        if "NOT_FOUND" in error_msg or "ZERO_RESULTS" in error_msg:
            # Error de direcciones no encontradas - 422 (Unprocessable Entity)
            raise HTTPException(status_code=422, detail=error_msg)
        elif "REQUEST_DENIED" in error_msg or "OVER_QUERY_LIMIT" in error_msg:
            # Error de API - 503 (Service Unavailable)
            raise HTTPException(status_code=503, detail=error_msg)
        else:
            # Otros errores de validación - 400 (Bad Request)
            raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular ruta: {str(e)}")


@router.post("/batch-routes", response_model=List[OrderRouteResponse])
async def get_multiple_order_routes(
    request: MultipleOrderRoutesRequest,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Calcula rutas para múltiples pedidos simultáneamente"""
    try:
        routes = order_service.get_multiple_order_routes(db, request.order_ids, request.mode)
        if not routes:
            raise HTTPException(status_code=404, detail="No se encontraron pedidos válidos")
        return routes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular rutas: {str(e)}")


@router.get("/driver/{driver_id}/routes", response_model=List[OrderRouteResponse])
async def get_driver_routes(
    driver_id: int,
    mode: str = Query("driving", description="Modo de transporte"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service)
):
    """Obtiene rutas de todos los pedidos asignados a un conductor"""
    try:
        # Obtener pedidos del conductor
        orders = order_service.get_by_driver(db, driver_id, skip, limit)
        if not orders:
            raise HTTPException(status_code=404, detail="No se encontraron pedidos para este conductor")
        
        # Calcular rutas para cada pedido
        order_ids = [order.id for order in orders]
        routes = order_service.get_multiple_order_routes(db, order_ids, mode)
        
        return routes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener rutas del conductor: {str(e)}")
