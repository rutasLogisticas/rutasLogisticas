"""
Rutas para el servicio de direcciones (Google Directions)
"""
from fastapi import APIRouter, HTTPException
from app.services.directions_service import DirectionsService
from app.services.geocoding_service import GeocodingService
from app.schemas.directions_schemas import DirectionsRequest, DirectionsResponse

router = APIRouter(prefix="/directions", tags=["Rutas"])

directions_service = DirectionsService()
geocoding_service = GeocodingService()


@router.post("/", response_model=DirectionsResponse)
async def get_directions(request: DirectionsRequest):
    """
    Obtiene la ruta, distancia y duración entre dos direcciones.
    """
    try:
        # Geocodificar si no son coordenadas
        origin = geocoding_service.geocode_address(request.origin).formatted_address or request.origin
        destination = geocoding_service.geocode_address(request.destination).formatted_address or request.destination

        result = directions_service.get_directions(origin, destination, request.mode)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
