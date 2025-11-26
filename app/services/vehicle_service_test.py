"""
Tests unitarios para VehicleService
"""
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session


class TestGetByLicensePlate:
    """Tests para get_by_license_plate"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.vehicle_service import VehicleService
        service = VehicleService()
        service.repository = Mock()
        return service
    
    def test_get_by_license_plate_found(self, service, mock_db):
        """Debe retornar vehículo cuando existe"""
        expected_vehicle = Mock()
        expected_vehicle.license_plate = "ABC123"
        
        service.repository.get_by_license_plate.return_value = expected_vehicle
        
        result = service.get_by_license_plate(mock_db, "ABC123")
        
        assert result == expected_vehicle
        service.repository.get_by_license_plate.assert_called_once_with(mock_db, "ABC123")
    
    def test_get_by_license_plate_not_found(self, service, mock_db):
        """Debe retornar None cuando no existe"""
        service.repository.get_by_license_plate.return_value = None
        
        result = service.get_by_license_plate(mock_db, "ZZZ999")
        
        assert result is None
    
    def test_get_by_license_plate_case_sensitive(self, service, mock_db):
        """Debe buscar con la placa exacta proporcionada"""
        service.repository.get_by_license_plate.return_value = None
        
        service.get_by_license_plate(mock_db, "abc123")
        
        service.repository.get_by_license_plate.assert_called_once_with(mock_db, "abc123")


class TestGetAvailableVehicles:
    """Tests para get_available_vehicles"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.vehicle_service import VehicleService
        service = VehicleService()
        service.repository = Mock()
        return service
    
    def test_get_available_vehicles_returns_list(self, service, mock_db):
        """Debe retornar lista de vehículos disponibles"""
        mock_vehicles = [Mock(), Mock(), Mock()]
        service.repository.get_available_vehicles.return_value = mock_vehicles
        
        result = service.get_available_vehicles(mock_db)
        
        assert result == mock_vehicles
        assert len(result) == 3
    
    def test_get_available_vehicles_with_pagination(self, service, mock_db):
        """Debe respetar parámetros de paginación"""
        service.repository.get_available_vehicles.return_value = []
        
        service.get_available_vehicles(mock_db, skip=20, limit=10)
        
        service.repository.get_available_vehicles.assert_called_once_with(
            mock_db, 20, 10
        )
    
    def test_get_available_vehicles_default_pagination(self, service, mock_db):
        """Debe usar paginación por defecto"""
        service.repository.get_available_vehicles.return_value = []
        
        service.get_available_vehicles(mock_db)
        
        service.repository.get_available_vehicles.assert_called_once_with(
            mock_db, 0, 100
        )
    
    def test_get_available_vehicles_empty(self, service, mock_db):
        """Debe retornar lista vacía si no hay vehículos disponibles"""
        service.repository.get_available_vehicles.return_value = []
        
        result = service.get_available_vehicles(mock_db)
        
        assert result == []
        assert isinstance(result, list)
