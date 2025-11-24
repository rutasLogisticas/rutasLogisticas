from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import joinedload




class AuditRepository:

    def create_log(self, db: Session, log_data: dict):
        log = AuditLog(**log_data)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    def get_logs(
        self,
        db: Session,
        actor_id: Optional[int] = None,
        event_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        query = (
            db.query(AuditLog)
            .options(joinedload(AuditLog.actor))
        )

        if actor_id:
            query = query.filter(AuditLog.actor_id == actor_id)

        if event_type:
            query = query.filter(AuditLog.event_type == event_type)

        if start_date:
            query = query.filter(AuditLog.created_at >= start_date)

        if end_date:
            query = query.filter(AuditLog.created_at <= end_date)

        return query.order_by(AuditLog.created_at.desc()).all()