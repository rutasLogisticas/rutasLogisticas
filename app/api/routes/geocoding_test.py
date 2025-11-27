"""
Tests unitarios para rutas de geocodificación
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException


class TestGeocodeAddress:
    """Tests para POST /geocoding"""
    
    @pytest.mark.asyncio
    async def test_geocode_address_success(self):
        """Debe geocodificar dirección correctamente"""
        from app.api.routes.geocoding import geocode_address
        from app.schemas.geocoding_schemas import GeocodingRequest, GeocodingResponse
        
        request = GeocodingRequest(address="Bogotá, Colombia")
        
        mock_result = GeocodingResponse(
            address="Bogotá, Colombia",
            latitude=4.6097,
            longitude=-74.0817,
            formatted_address="Bogotá, Bogotá, Colombia",
            status="OK"
        )
        
        with patch('app.api.routes.geocoding.geocoding_service') as mock_service:
            mock_service.geocode_address.return_value = mock_result
            
            result = await geocode_address(request)
            
            assert result.latitude == 4.6097
            assert result.longitude == -74.0817
            assert result.status == "OK"
    
    @pytest.mark.asyncio
    async def test_geocode_address_not_found(self):
        """Debe retornar 404 si no encuentra dirección"""
        from app.api.routes.geocoding import geocode_address
        from app.schemas.geocoding_schemas import GeocodingRequest
        
        request = GeocodingRequest(address="Dirección inexistente XYZ")
        
        with patch('app.api.routes.geocoding.geocoding_service') as mock_service:
            mock_service.geocode_address.side_effect = ValueError("No se encontró")
            
            with pytest.raises(HTTPException) as exc_info:
                await geocode_address(request)
            
            assert exc_info.value.status_code == 404
    
    @pytest.mark.asyncio
    async def test_geocode_address_server_error(self):
        """Debe retornar 500 si hay error interno"""
        from app.api.routes.geocoding import geocode_address
        from app.schemas.geocoding_schemas import GeocodingRequest
        
        request = GeocodingRequest(address="Bogotá")
        
        with patch('app.api.routes.geocoding.geocoding_service') as mock_service:
            mock_service.geocode_address.side_effect = Exception("Error interno")
            
            with pytest.raises(HTTPException) as exc_info:
                await geocode_address(request)
            
            assert exc_info.value.status_code == 500


class TestHealthCheck:
    """Tests para GET /geocoding/health"""
    
    @pytest.mark.asyncio
    async def test_health_check_healthy(self):
        """Debe retornar healthy cuando funciona"""
        from app.api.routes.geocoding import health_check
        
        with patch('app.api.routes.geocoding.geocoding_service') as mock_service:
            mock_service.health_check.return_value = {
                "status": "healthy",
                "message": "OK",
                "api_key_configured": True
            }
            
            result = await health_check()
            
            assert result.status_code == 200
    
    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self):
        """Debe retornar 503 cuando no funciona"""
        from app.api.routes.geocoding import health_check
        
        with patch('app.api.routes.geocoding.geocoding_service') as mock_service:
            mock_service.health_check.return_value = {
                "status": "unhealthy",
                "message": "Error"
            }
            
            result = await health_check()
            
            assert result.status_code == 503


class TestTestGeocodingEndpoint:
    """Tests para GET /geocoding/test"""
    
    @pytest.mark.asyncio
    async def test_geocoding_test_success(self):
        """Debe retornar resultado de test"""
        from app.api.routes.geocoding import test_geocoding
        from app.schemas.geocoding_schemas import GeocodingResponse
        
        mock_result = GeocodingResponse(
            address="Carrera 7 #32-16, Bogotá, Colombia",
            latitude=4.6097,
            longitude=-74.0817,
            formatted_address="Carrera 7 #32-16, Bogotá, Colombia",
            status="OK"
        )
        
        with patch('app.api.routes.geocoding.geocoding_service') as mock_service:
            mock_service.geocode_address.return_value = mock_result
            
            result = await test_geocoding()
            
            assert "message" in result
            assert "test_address" in result
            assert result["result"] == mock_result
    
    @pytest.mark.asyncio
    async def test_geocoding_test_error(self):
        """Debe retornar 500 si falla el test"""
        from app.api.routes.geocoding import test_geocoding
        
        with patch('app.api.routes.geocoding.geocoding_service') as mock_service:
            mock_service.geocode_address.side_effect = Exception("Error")
            
            with pytest.raises(HTTPException) as exc_info:
                await test_geocoding()
            
            assert exc_info.value.status_code == 500

