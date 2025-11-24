from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel


# ==========================================================
# Schema base (lo que comparten todos)
# ==========================================================
class AuditBase(BaseModel):
    actor_id: Optional[int] = None
    event_type: str
    description: str
    ip_address: Optional[str] = None
    extra_data: Optional[Any] = None


# ==========================================================
# Para crear registros desde el backend
# ==========================================================
class AuditCreate(AuditBase):
    pass


# ==========================================================
# Respuesta al consultar auditoría
# ==========================================================
class AuditResponse(AuditBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Antes "orm_mode = True" en Pydantic v1

class AuditLogOut(BaseModel):
    id: int
    event_type: str
    description: str
    ip_address: str
    created_at: datetime
    usuario: Optional[str]

    class Config:
        orm_mode = True
