"""
Esquemas para el servicio de geocodificación
"""
from pydantic import BaseModel, Field
from typing import Optional


class GeocodingRequest(BaseModel):
    """Esquema para solicitud de geocodificación"""
    address: str = Field(..., description="Dirección a geocodificar", min_length=1)


class GeocodingResponse(BaseModel):
    """Esquema para respuesta de geocodificación"""
    address: str = Field(..., description="Dirección original")
    latitude: float = Field(..., description="Latitud")
    longitude: float = Field(..., description="Longitud")
    formatted_address: Optional[str] = Field(None, description="Dirección formateada por Google")
    status: str = Field(..., description="Estado de la respuesta")


class GeocodingErrorResponse(BaseModel):
    """Esquema para errores de geocodificación"""
    error: str = Field(..., description="Mensaje de error")
    address: str = Field(..., description="Dirección que causó el error")
