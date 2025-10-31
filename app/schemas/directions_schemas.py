"""
Esquemas para el servicio de direcciones (rutas)
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class DirectionsRequest(BaseModel):
    """Solicitud de cálculo de ruta"""
    origin: str = Field(..., description="Dirección o coordenadas de origen")
    destination: str = Field(..., description="Dirección o coordenadas de destino")
    mode: Optional[str] = Field("driving", description="Modo de transporte: driving, walking, bicycling, transit")


class RouteStep(BaseModel):
    """Paso individual de la ruta"""
    instruction: str
    distance_text: str
    duration_text: str


class DirectionsResponse(BaseModel):
    """Respuesta con detalles de la ruta"""
    origin: str
    destination: str
    distance_text: str
    duration_text: str
    polyline: str
    steps: List[RouteStep]
