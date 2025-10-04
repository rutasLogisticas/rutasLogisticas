"""
Esquemas base para validación de datos
Implementa principio DRY y validaciones consistentes
"""
from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')


class BaseSchema(BaseModel):
    """Esquema base con configuración común"""
    
    class Config:
        from_attributes = True
        use_enum_values = True
        validate_assignment = True


class BaseCreateSchema(BaseSchema):
    """Esquema base para creación de recursos"""
    pass


class BaseUpdateSchema(BaseSchema):
    """Esquema base para actualización de recursos"""
    pass


class BaseResponseSchema(BaseSchema):
    """Esquema base para respuestas de la API"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


class PaginatedResponse(BaseModel, Generic[T]):
    """Esquema para respuestas paginadas"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    @classmethod
    def create(cls, items: List[T], total: int, page: int, size: int) -> 'PaginatedResponse[T]':
        """Crea respuesta paginada calculando el número de páginas"""
        pages = (total + size - 1) // size if total > 0 else 1
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )


class ErrorResponse(BaseModel):
    """Esquema para respuestas de error"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SuccessResponse(BaseModel):
    """Esquema para respuestas de éxito"""
    message: str
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SearchRequest(BaseModel):
    """Esquema para búsquedas"""
    query: str = Field(..., min_length=2, max_length=100)
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)


class FilterRequest(BaseModel):
    """Esquema para filtros genéricos"""
    filters: dict = Field(default_factory=dict)
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)
