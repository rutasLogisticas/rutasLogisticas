"""
Servicio de geocodificación usando Google Maps API
"""
import requests
import logging
from typing import Optional, Dict, Any
from app.core.config import config
from app.schemas.geocoding_schemas import GeocodingResponse

logger = logging.getLogger(__name__)


class GeocodingService:
    """Servicio para geocodificar direcciones usando Google Maps API"""
    
    def __init__(self):
        self.api_key = config.google_maps_api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    def geocode_address(self, address: str) -> GeocodingResponse:
        """
        Geocodifica una dirección usando Google Maps API
        
        Args:
            address: Dirección a geocodificar
            
        Returns:
            GeocodingResponse: Respuesta con coordenadas
            
        Raises:
            ValueError: Si la dirección no se puede geocodificar
        """
        try:
            # Parámetros para la API de Google Maps
            params = {
                'address': address,
                'key': self.api_key
            }
            
            logger.info(f"Geocodificando dirección: {address}")
            
            # Realizar petición a Google Maps API
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Verificar estado de la respuesta
            if data.get('status') != 'OK':
                error_msg = f"Google Maps API error: {data.get('status')}"
                if data.get('error_message'):
                    error_msg += f" - {data.get('error_message')}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Extraer resultados
            results = data.get('results', [])
            if not results:
                raise ValueError(f"No se encontraron coordenadas para la dirección: {address}")
            
            # Obtener el primer resultado
            result = results[0]
            geometry = result.get('geometry', {})
            location = geometry.get('location', {})
            
            latitude = location.get('lat')
            longitude = location.get('lng')
            
            if not latitude or not longitude:
                raise ValueError("Coordenadas no válidas en la respuesta de Google Maps")
            
            # Crear respuesta
            geocoding_response = GeocodingResponse(
                address=address,
                latitude=latitude,
                longitude=longitude,
                formatted_address=result.get('formatted_address'),
                status='OK'
            )
            
            logger.info(f"Geocodificación exitosa: {address} -> ({latitude}, {longitude})")
            return geocoding_response
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error de conexión con Google Maps API: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        except Exception as e:
            error_msg = f"Error inesperado en geocodificación: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica que el servicio esté funcionando correctamente
        
        Returns:
            Dict con información del estado del servicio
        """
        try:
            # Probar con una dirección conocida
            test_address = "Bogotá, Colombia"
            result = self.geocode_address(test_address)
            
            return {
                "status": "healthy",
                "message": "Servicio de geocodificación funcionando correctamente",
                "api_key_configured": bool(self.api_key),
                "test_result": {
                    "address": result.address,
                    "coordinates": f"({result.latitude}, {result.longitude})"
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Error en el servicio: {str(e)}",
                "api_key_configured": bool(self.api_key)
            }
