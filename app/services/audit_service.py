from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.repositories.audit_repository import AuditRepository
import json



class AuditService:
    def __init__(self):
        self.repository = AuditRepository()

    def registrar_evento(self, db, actor, event_type, description, ip_address, details):
        log_data = {
            "actor_id": actor,  # Puede ser None
            "event_type": event_type,
            "description": description,
            "ip_address": ip_address,
            "extra_data": json.dumps(details or {}),
        }
        return self.repository.create_log(db, log_data)

    def buscar(
        self,
        db: Session,
        actor: Optional[int] = None,
        event_type: Optional[str] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
    ):
        return self.repository.get_logs(
            db=db,
            actor_id=actor,
            event_type=event_type,
            start_date=fecha_desde,
            end_date=fecha_hasta,
        )