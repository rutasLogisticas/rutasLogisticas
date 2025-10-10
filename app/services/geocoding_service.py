"""
Servicio de geocodificación usando Google Maps API
"""
import requests
import logging
from typing import Optional

from app.core.config import config
from app.schemas.geocoding_schemas import GeocodingResponse

logger = logging.getLogger(__name__)


class GeocodingService:
    """Servicio para convertir direcciones en coordenadas geográficas"""
    
    def __init__(self):
        self.api_key = config.GOOGLE_MAPS_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.timeout = 10  # segundos
        
        if not self.api_key:
            logger.warning("Google Maps API Key no configurada")
    
    def get_coordinates(self, address: str) -> Optional[GeocodingResponse]:
        """
        Obtiene las coordenadas geográficas de una dirección.
        
        Args:
            address: Dirección a geocodificar
            
        Returns:
            GeocodingResponse con los datos de ubicación o None si falla
            
        Raises:
            ValueError: Si no hay API key configurada
        """
        if not self.api_key:
            raise ValueError("Google Maps API Key no configurada. Configura GOOGLE_MAPS_API_KEY en el archivo .env")
        
        params = {
            "address": address,
            "key": self.api_key
        }
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            # Verificar si hay resultados
            if data.get("status") != "OK" or not data.get("results"):
                logger.warning(f"No se encontraron resultados para: {address}. Status: {data.get('status')}")
                return None
            
            # Extraer primer resultado
            result = data["results"][0]
            location = result["geometry"]["location"]
            
            return GeocodingResponse(
                address=result["formatted_address"],
                latitude=location["lat"],
                longitude=location["lng"]
            )
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout al geocodificar: {address}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en solicitud HTTP: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error procesando respuesta de la API: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado en geocodificación: {e}")
            return None


# Instancia singleton
geocoding_service = GeocodingService()
