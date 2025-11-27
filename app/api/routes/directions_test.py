"""
Tests unitarios para rutas de direcciones
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException


class TestGetDirections:
    """Tests para POST /directions"""
    
    @pytest.mark.asyncio
    async def test_get_directions_success(self):
        """Debe retornar direcciones correctamente"""
        from app.api.routes.directions import get_directions
        from app.schemas.directions_schemas import DirectionsRequest
        
        request = DirectionsRequest(
            origin="Bogotá, Colombia",
            destination="Medellín, Colombia",
            mode="driving"
        )
        
        mock_geocode_result = Mock()
        mock_geocode_result.formatted_address = "Bogotá, Colombia"
        
        mock_directions_result = Mock(
            origin="Bogotá, Colombia",
            destination="Medellín, Colombia",
            distance_text="415 km",
            duration_text="8 horas",
            polyline="abc123",
            steps=[]
        )
        
        with patch('app.api.routes.directions.geocoding_service') as mock_geo, \
             patch('app.api.routes.directions.directions_service') as mock_dir:
            
            mock_geo.geocode_address.return_value = mock_geocode_result
            mock_dir.get_directions.return_value = mock_directions_result
            
            result = await get_directions(request)
            
            assert result == mock_directions_result
    
    @pytest.mark.asyncio
    async def test_get_directions_error(self):
        """Debe retornar 500 si hay error"""
        from app.api.routes.directions import get_directions
        from app.schemas.directions_schemas import DirectionsRequest
        
        request = DirectionsRequest(
            origin="A",
            destination="B",
            mode="driving"
        )
        
        with patch('app.api.routes.directions.geocoding_service') as mock_geo:
            mock_geo.geocode_address.side_effect = Exception("Error de API")
            
            with pytest.raises(HTTPException) as exc_info:
                await get_directions(request)
            
            assert exc_info.value.status_code == 500

