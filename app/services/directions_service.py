"""
Servicio de direcciones usando Google Directions API
"""
import requests
import logging
from typing import Dict, Any, List
from app.core.config import config
from app.schemas.directions_schemas import DirectionsResponse, RouteStep

logger = logging.getLogger(__name__)


class DirectionsService:
    """Servicio para calcular rutas entre dos puntos"""
    
    def __init__(self):
        self.api_key = config.google_maps_api_key
        self.base_url = "https://maps.googleapis.com/maps/api/directions/json"

    def get_directions(self, origin: str, destination: str, mode: str = "driving") -> DirectionsResponse:
        """
        Obtiene la ruta entre dos direcciones usando Google Directions API
        """
        try:
            params = {
                "origin": origin,
                "destination": destination,
                "mode": mode,
                "key": self.api_key
            }

            logger.info(f"Calculando ruta de {origin} a {destination} en modo {mode}")

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("status") != "OK":
                raise ValueError(f"Error en Directions API: {data.get('status')}")

            route = data["routes"][0]
            leg = route["legs"][0]

            steps = [
                RouteStep(
                    instruction=s["html_instructions"],
                    distance_text=s["distance"]["text"],
                    duration_text=s["duration"]["text"]
                )
                for s in leg["steps"]
            ]

            return DirectionsResponse(
                origin=leg["start_address"],
                destination=leg["end_address"],
                distance_text=leg["distance"]["text"],
                duration_text=leg["duration"]["text"],
                polyline=route["overview_polyline"]["points"],
                steps=steps
            )

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error de conexión con Google Directions API: {e}")

        except Exception as e:
            raise ValueError(f"Error inesperado en DirectionsService: {e}")
