"""
Endpoints API para Reportes

Este módulo define los endpoints REST para generar reportes y estadísticas.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, select, and_, or_

from app.api.dependencies import get_db
from app.models.order import Order
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.client import Client

router = APIRouter(prefix="/reports", tags=["reports"])

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


@router.get("/orders/summary")
async def get_orders_summary(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """Obtiene resumen de pedidos con relaciones"""
    try:
        query = db.query(Order).filter(Order.is_active == True)
        
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        
        total_orders = query.count()
        
        # Pedidos por estado
        base_query = db.query(Order).filter(Order.is_active == True)
        if start_date:
            base_query = base_query.filter(Order.created_at >= start_date)
        if end_date:
            base_query = base_query.filter(Order.created_at <= end_date)
            
        orders_by_status = base_query.with_entities(
            Order.status,
            func.count(Order.id).label('count')
        ).group_by(Order.status).all()
        
        # Pedidos por prioridad
        orders_by_priority = base_query.with_entities(
            Order.priority,
            func.count(Order.id).label('count')
        ).group_by(Order.priority).all()
        
        # Pedidos por ciudad de destino
        orders_by_destination = base_query.with_entities(
            Order.destination_city,
            func.count(Order.id).label('count')
        ).group_by(Order.destination_city).order_by(func.count(Order.id).desc()).limit(10).all()
        
        # Pedidos asignados vs no asignados
        assigned_count = base_query.filter(Order.driver_id.isnot(None)).count()
        unassigned_count = base_query.filter(Order.driver_id.is_(None)).count()
        
        # Valor total de pedidos
        total_value = base_query.with_entities(
            func.sum(Order.value).label('total')
        ).scalar() or 0
        
        return {
            "total_orders": total_orders,
            "by_status": {status: count for status, count in orders_by_status},
            "by_priority": {priority: count for priority, count in orders_by_priority},
            "by_destination": {city: count for city, count in orders_by_destination},
            "assigned": assigned_count,
            "unassigned": unassigned_count,
            "total_value": float(total_value)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")


@router.get("/vehicles/summary")
async def get_vehicles_summary(
    db: Session = Depends(get_db)
):
    """Obtiene resumen de vehículos con relaciones"""
    try:
        total_vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).count()
        
        # Vehículos por tipo
        vehicles_by_type = db.query(
            Vehicle.vehicle_type,
            func.count(Vehicle.id).label('count')
        ).filter(Vehicle.is_active == True).group_by(Vehicle.vehicle_type).all()
        
        # Vehículos disponibles vs en uso
        available_vehicles = db.query(Vehicle).filter(
            Vehicle.is_available == True, 
            Vehicle.is_active == True
        ).count()
        busy_vehicles = total_vehicles - available_vehicles
        
        # Vehículos con más pedidos asignados
        vehicles_with_orders = db.query(
            Vehicle.id,
            Vehicle.license_plate,
            Vehicle.vehicle_type,
            func.count(Order.id).label('order_count')
        ).filter(Vehicle.is_active == True).join(
            Order, and_(Vehicle.id == Order.vehicle_id, Order.is_active == True)
        ).group_by(
            Vehicle.id, Vehicle.license_plate, Vehicle.vehicle_type
        ).order_by(func.count(Order.id).desc()).limit(10).all()
        
        return {
            "total_vehicles": total_vehicles,
            "by_type": {vehicle_type: count for vehicle_type, count in vehicles_by_type},
            "available": available_vehicles,
            "busy": busy_vehicles,
            "top_vehicles": [
                {
                    "id": v_id,
                    "license_plate": plate,
                    "vehicle_type": v_type,
                    "order_count": count
                }
                for v_id, plate, v_type, count in vehicles_with_orders
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")


@router.get("/drivers/summary")
async def get_drivers_summary(
    db: Session = Depends(get_db)
):
    """Obtiene resumen de conductores con relaciones"""
    try:
        total_drivers = db.query(Driver).filter(Driver.is_active == True).count()
        
        # Conductores disponibles
        available_drivers = db.query(Driver).filter(
            Driver.is_available == True,
            Driver.is_active == True
        ).count()
        busy_drivers = total_drivers - available_drivers
        
        # Conductores con más pedidos asignados
        drivers_with_orders = db.query(
            Driver.id,
            Driver.first_name,
            Driver.last_name,
            Driver.document_number,
            func.count(Order.id).label('order_count')
        ).filter(Driver.is_active == True).join(
            Order, and_(Driver.id == Order.driver_id, Order.is_active == True)
        ).group_by(
            Driver.id, Driver.first_name, Driver.last_name, Driver.document_number
        ).order_by(func.count(Order.id).desc()).limit(10).all()
        
        # Conductores sin pedidos asignados
        drivers_without_orders = db.query(Driver).filter(
            Driver.is_active == True,
            ~Driver.id.in_(
                db.query(Order.driver_id).filter(
                    Order.driver_id.isnot(None),
                    Order.is_active == True
                ).distinct()
            )
        ).count()
        
        return {
            "total_drivers": total_drivers,
            "available_drivers": available_drivers,
            "busy_drivers": busy_drivers,
            "top_drivers": [
                {
                    "id": d_id,
                    "name": f"{first_name} {last_name}",
                    "document_number": doc,
                    "order_count": count
                }
                for d_id, first_name, last_name, doc, count in drivers_with_orders
            ],
            "drivers_without_orders": drivers_without_orders
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")


@router.get("/clients/summary")
async def get_clients_summary(
    db: Session = Depends(get_db)
):
    """Obtiene resumen de clientes con relaciones"""
    try:
        total_clients = db.query(Client).filter(Client.is_active == True).count()
        
        # Clientes con más pedidos
        clients_with_orders = db.query(
            Client.id,
            Client.name,
            Client.company,
            Client.email,
            func.count(Order.id).label('order_count'),
            func.sum(Order.value).label('total_value')
        ).filter(Client.is_active == True).join(
            Order, and_(Client.id == Order.client_id, Order.is_active == True)
        ).group_by(
            Client.id, Client.name, Client.company, Client.email
        ).order_by(func.count(Order.id).desc()).limit(10).all()
        
        # Clientes sin pedidos
        clients_without_orders = db.query(Client).filter(
            Client.is_active == True,
            ~Client.id.in_(
                db.query(Order.client_id).filter(Order.is_active == True).distinct()
            )
        ).count()
        
        # Clientes por empresa
        clients_by_company = db.query(
            Client.company,
            func.count(Client.id).label('count')
        ).filter(Client.is_active == True, Client.company.isnot(None)).group_by(Client.company).order_by(
            func.count(Client.id).desc()
        ).limit(10).all()
        
        return {
            "total_clients": total_clients,
            "top_clients": [
                {
                    "id": c_id,
                    "name": name,
                    "company": company or "N/A",
                    "email": email,
                    "order_count": count,
                    "total_value": float(value or 0)
                }
                for c_id, name, company, email, count, value in clients_with_orders
            ],
            "clients_without_orders": clients_without_orders,
            "by_company": {company: count for company, count in clients_by_company}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")


@router.get("/overview")
async def get_overview(
    db: Session = Depends(get_db)
):
    """Obtiene un resumen general del sistema con todas las relaciones"""
    try:
        total_orders = db.query(Order).filter(Order.is_active == True).count()
        total_vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).count()
        total_drivers = db.query(Driver).filter(Driver.is_active == True).count()
        total_clients = db.query(Client).filter(Client.is_active == True).count()
        
        # Pedidos por estado
        pending_orders = db.query(Order).filter(
            Order.is_active == True,
            Order.status.in_(["pendiente", "en_proceso"])
        ).count()
        
        assigned_orders = db.query(Order).filter(
            Order.is_active == True,
            Order.driver_id.isnot(None)
        ).count()
        delivered_orders = db.query(Order).filter(
            Order.is_active == True,
            Order.status == "entregado"
        ).count()
        
        # Recursos disponibles
        available_vehicles = db.query(Vehicle).filter(
            Vehicle.is_available == True,
            Vehicle.is_active == True
        ).count()
        available_drivers = db.query(Driver).filter(
            Driver.is_available == True,
            Driver.is_active == True
        ).count()
        
        # Valor total
        total_value = db.query(func.sum(Order.value)).filter(Order.is_active == True).scalar() or 0
        
        # Estadísticas recientes (últimos 30 días)
        from datetime import timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_orders = db.query(Order).filter(
            Order.is_active == True,
            Order.created_at >= thirty_days_ago
        ).count()
        
        return {
            "summary": {
                "total_orders": total_orders,
                "total_vehicles": total_vehicles,
                "total_drivers": total_drivers,
                "total_clients": total_clients,
                "pending_orders": pending_orders,
                "assigned_orders": assigned_orders,
                "delivered_orders": delivered_orders,
                "available_vehicles": available_vehicles,
                "available_drivers": available_drivers,
                "total_value": float(total_value),
                "recent_orders": recent_orders
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")

