"""
Schemas para geocodificación
"""
from pydantic import BaseModel, Field


class GeocodingRequest(BaseModel):
    """Schema para solicitud de geocodificación"""
    address: str = Field(..., min_length=1, description="Dirección a geocodificar")


class GeocodingResponse(BaseModel):
    """Schema para respuesta de geocodificación"""
    address: str = Field(..., description="Dirección formateada")
    latitude: float = Field(..., description="Latitud")
    longitude: float = Field(..., description="Longitud")
    
    class Config:
        json_schema_extra = {
            "example": {
                "address": "Calle 100 #15-20, Bogotá, Colombia",
                "latitude": 4.6825,
                "longitude": -74.0481
            }
        }

