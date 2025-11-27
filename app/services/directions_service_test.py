"""
Tests unitarios para DirectionsService
"""
import pytest
from unittest.mock import Mock, patch

from app.services.directions_service import DirectionsService


class TestDirectionsServiceGetDirections:
    """Tests para get_directions"""
    
    @pytest.fixture
    def service(self):
        return DirectionsService()
    
    @patch('app.services.directions_service.requests.get')
    def test_get_directions_success(self, mock_get, service):
        """Debe obtener direcciones correctamente"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "OK",
            "routes": [{
                "legs": [{
                    "start_address": "Bogotá, Colombia",
                    "end_address": "Medellín, Colombia",
                    "distance": {"text": "415 km"},
                    "duration": {"text": "8 horas 30 min"},
                    "steps": [
                        {
                            "html_instructions": "Dirígete al norte",
                            "distance": {"text": "100 m"},
                            "duration": {"text": "1 min"}
                        },
                        {
                            "html_instructions": "Gira a la derecha",
                            "distance": {"text": "500 m"},
                            "duration": {"text": "2 min"}
                        }
                    ]
                }],
                "overview_polyline": {"points": "abc123xyz"}
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = service.get_directions("Bogotá", "Medellín")
        
        assert result.origin == "Bogotá, Colombia"
        assert result.destination == "Medellín, Colombia"
        assert result.distance_text == "415 km"
        assert result.duration_text == "8 horas 30 min"
        assert result.polyline == "abc123xyz"
        assert len(result.steps) == 2
    
    @patch('app.services.directions_service.requests.get')
    def test_get_directions_with_mode(self, mock_get, service):
        """Debe aceptar modo de transporte"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "OK",
            "routes": [{
                "legs": [{
                    "start_address": "A",
                    "end_address": "B",
                    "distance": {"text": "5 km"},
                    "duration": {"text": "1 hora"},
                    "steps": []
                }],
                "overview_polyline": {"points": "xyz"}
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = service.get_directions("A", "B", mode="walking")
        
        # Verificar que se llamó con el modo correcto
        call_args = mock_get.call_args
        assert call_args[1]["params"]["mode"] == "walking"
    
    @patch('app.services.directions_service.requests.get')
    def test_get_directions_not_found(self, mock_get, service):
        """Debe lanzar error si no encuentra ruta"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "NOT_FOUND",
            "error_message": "Dirección no encontrada"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            service.get_directions("Dirección falsa", "Otra falsa")
        
        assert "NOT_FOUND" in str(exc_info.value)
    
    @patch('app.services.directions_service.requests.get')
    def test_get_directions_zero_results(self, mock_get, service):
        """Debe lanzar error si no hay resultados"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "ZERO_RESULTS"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            service.get_directions("Isla remota", "Otra isla")
        
        assert "ZERO_RESULTS" in str(exc_info.value)
    
    @patch('app.services.directions_service.requests.get')
    def test_get_directions_request_denied(self, mock_get, service):
        """Debe lanzar error si API key inválida"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "REQUEST_DENIED",
            "error_message": "API key inválida"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            service.get_directions("A", "B")
        
        assert "REQUEST_DENIED" in str(exc_info.value)
    
    @patch('app.services.directions_service.requests.get')
    def test_get_directions_over_query_limit(self, mock_get, service):
        """Debe lanzar error si excede límite"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "OVER_QUERY_LIMIT"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            service.get_directions("A", "B")
        
        assert "OVER_QUERY_LIMIT" in str(exc_info.value)
    
    @patch('app.services.directions_service.requests.get')
    def test_get_directions_connection_error(self, mock_get, service):
        """Debe manejar errores de conexión"""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Sin conexión")
        
        with pytest.raises(ValueError) as exc_info:
            service.get_directions("A", "B")
        
        assert "conexión" in str(exc_info.value).lower()
    
    @patch('app.services.directions_service.requests.get')
    def test_get_directions_invalid_request(self, mock_get, service):
        """Debe manejar solicitud inválida"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "INVALID_REQUEST"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            service.get_directions("", "")
        
        assert "INVALID_REQUEST" in str(exc_info.value)

