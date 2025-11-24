from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.audit_service import AuditService
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/audit", tags=["Auditoría"])
audit_service = AuditService()


@router.get("/")
def get_logs(
    db: Session = Depends(get_db),
    actor_id: Optional[int] = Query(None),
    event_type: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
):
    """
    Obtener todos los logs con filtros opcionales
    """

    logs = audit_service.buscar(
        db=db,
        actor=actor_id,
        event_type=event_type,
        fecha_desde=date_from,
        fecha_hasta=date_to,
    )

    return [
        {
            "id": log.id,
            "created_at": log.created_at,
            "event_type": log.event_type,
            "description": log.description,
            "ip_address": log.ip_address,
            "actor_id": log.actor_id,
            "username": log.actor.username if log.actor else None
        }
        for log in logs
    ]
