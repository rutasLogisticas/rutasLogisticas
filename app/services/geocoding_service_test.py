"""
Tests unitarios para GeocodingService
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

from app.services.geocoding_service import GeocodingService
from app.schemas.geocoding_schemas import GeocodingResponse


class TestGeocodingServiceGeocodeAddress:
    """Tests para geocode_address"""
    
    @pytest.fixture
    def service(self):
        return GeocodingService()
    
    @patch('app.services.geocoding_service.requests.get')
    def test_geocode_address_success(self, mock_get, service):
        """Debe geocodificar dirección correctamente"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [{
                "geometry": {
                    "location": {
                        "lat": 4.6097,
                        "lng": -74.0817
                    }
                },
                "formatted_address": "Bogotá, Colombia"
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = service.geocode_address("Bogotá, Colombia")
        
        assert result.latitude == 4.6097
        assert result.longitude == -74.0817
        assert result.status == "OK"
    
    @patch('app.services.geocoding_service.requests.get')
    def test_geocode_address_not_found(self, mock_get, service):
        """Debe lanzar error si no encuentra dirección"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "ZERO_RESULTS",
            "results": []
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            service.geocode_address("Dirección inexistente XYZ123")
        
        assert "ZERO_RESULTS" in str(exc_info.value)
    
    @patch('app.services.geocoding_service.requests.get')
    def test_geocode_address_api_error(self, mock_get, service):
        """Debe manejar errores de API"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "REQUEST_DENIED",
            "error_message": "API key inválida"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            service.geocode_address("Bogotá")
        
        assert "REQUEST_DENIED" in str(exc_info.value)
    
    @patch('app.services.geocoding_service.requests.get')
    def test_geocode_address_connection_error(self, mock_get, service):
        """Debe manejar errores de conexión"""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Sin conexión")
        
        with pytest.raises(ValueError) as exc_info:
            service.geocode_address("Bogotá")
        
        assert "conexión" in str(exc_info.value).lower()
    
    @patch('app.services.geocoding_service.requests.get')
    def test_geocode_address_timeout(self, mock_get, service):
        """Debe manejar timeout"""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")
        
        with pytest.raises(ValueError) as exc_info:
            service.geocode_address("Bogotá")
        
        assert "conexión" in str(exc_info.value).lower() or "Timeout" in str(exc_info.value)


class TestGeocodingServiceHealthCheck:
    """Tests para health_check"""
    
    @pytest.fixture
    def service(self):
        return GeocodingService()
    
    @patch('app.services.geocoding_service.requests.get')
    def test_health_check_healthy(self, mock_get, service):
        """Debe retornar healthy cuando funciona"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [{
                "geometry": {
                    "location": {"lat": 4.6097, "lng": -74.0817}
                },
                "formatted_address": "Bogotá, Colombia"
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = service.health_check()
        
        assert result["status"] == "healthy"
        assert "test_result" in result
    
    @patch('app.services.geocoding_service.requests.get')
    def test_health_check_unhealthy(self, mock_get, service):
        """Debe retornar unhealthy cuando falla"""
        mock_get.side_effect = Exception("Error de conexión")
        
        result = service.health_check()
        
        assert result["status"] == "unhealthy"
        assert "Error" in result["message"]

