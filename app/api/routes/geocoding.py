"""
Rutas para el servicio de geocodificación
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging

from app.schemas.geocoding_schemas import GeocodingRequest, GeocodingResponse, GeocodingErrorResponse
from app.services.geocoding_service import GeocodingService

logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(prefix="/geocoding", tags=["Geocodificación"])

# Instancia del servicio
geocoding_service = GeocodingService()


@router.post(
    "/",
    response_model=GeocodingResponse,
    summary="Geocodificar dirección",
    description="Convierte una dirección en coordenadas geográficas usando Google Maps API"
)
async def geocode_address(request: GeocodingRequest) -> GeocodingResponse:
    """
    Geocodifica una dirección y retorna sus coordenadas
    
    - **address**: Dirección a geocodificar (ej: "Carrera 116B 74A 40, Bogotá, Colombia")
    
    Returns:
    - **address**: Dirección original
    - **latitude**: Latitud
    - **longitude**: Longitud
    - **formatted_address**: Dirección formateada por Google
    - **status**: Estado de la respuesta
    """
    try:
        logger.info(f"Recibida solicitud de geocodificación para: {request.address}")
        
        result = geocoding_service.geocode_address(request.address)
        
        logger.info(f"Geocodificación exitosa: {request.address}")
        return result
        
    except ValueError as e:
        logger.error(f"Error de geocodificación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en geocodificación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/health",
    summary="Verificar estado del servicio",
    description="Verifica que el servicio de geocodificación esté funcionando correctamente"
)
async def health_check():
    """
    Verifica el estado del servicio de geocodificación
    
    Returns:
    - **status**: Estado del servicio (healthy/unhealthy)
    - **message**: Mensaje descriptivo
    - **api_key_configured**: Si la API key está configurada
    - **test_result**: Resultado del test (si está healthy)
    """
    try:
        health_info = geocoding_service.health_check()
        
        if health_info["status"] == "healthy":
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=health_info
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content=health_info
            )
            
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": f"Error verificando el estado: {str(e)}"
            }
        )


@router.get(
    "/test",
    summary="Probar geocodificación",
    description="Endpoint de prueba para verificar que la geocodificación funciona"
)
async def test_geocoding():
    """
    Endpoint de prueba para verificar la geocodificación
    
    Returns:
    - Resultado de geocodificar una dirección de prueba
    """
    try:
        test_address = "Carrera 7 #32-16, Bogotá, Colombia"
        result = geocoding_service.geocode_address(test_address)
        
        return {
            "message": "Test de geocodificación exitoso",
            "test_address": test_address,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error en test de geocodificación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en test: {str(e)}"
        )
