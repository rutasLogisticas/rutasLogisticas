"""
Endpoints para geocodificación
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict

from app.schemas.geocoding_schemas import GeocodingRequest, GeocodingResponse
from app.services.geocoding_service import geocoding_service

router = APIRouter(prefix="/geocoding", tags=["Geocoding"])


@router.post(
    "/",
    response_model=GeocodingResponse,
    status_code=status.HTTP_200_OK,
    summary="Geocodificar dirección",
    description="Convierte una dirección en coordenadas geográficas (latitud, longitud)"
)
async def geocode_address(request: GeocodingRequest) -> GeocodingResponse:
    """
    Geocodifica una dirección y retorna sus coordenadas.
    
    - **address**: Dirección completa a geocodificar
    
    Retorna la dirección formateada con latitud y longitud.
    """
    try:
        result = geocoding_service.get_coordinates(request.address)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se pudo geocodificar la dirección: {request.address}"
            )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/health",
    response_model=Dict[str, str],
    summary="Estado del servicio de geocodificación"
)
async def geocoding_health() -> Dict[str, str]:
    """Verifica si el servicio de geocodificación está configurado correctamente"""
    from app.core.config import config
    
    if config.GOOGLE_MAPS_API_KEY:
        return {"status": "ok", "message": "API Key configurada"}
    else:
        return {"status": "warning", "message": "API Key no configurada"}
