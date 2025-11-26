"""
Tests unitarios para VehicleRepository
"""
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.repositories.vehicle_repository import VehicleRepository
from app.models.vehicle import Vehicle


class TestVehicleRepositoryGetByLicensePlate:
    """Tests para get_by_license_plate"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return VehicleRepository()
    
    def test_get_by_license_plate_found(self, repository, mock_db):
        """Debe retornar vehículo cuando existe"""
        mock_vehicle = Mock(spec=Vehicle)
        mock_vehicle.license_plate = "ABC123"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_vehicle
        
        result = repository.get_by_license_plate(mock_db, "ABC123")
        
        assert result == mock_vehicle
    
    def test_get_by_license_plate_not_found(self, repository, mock_db):
        """Debe retornar None cuando no existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = repository.get_by_license_plate(mock_db, "ZZZ999")
        
        assert result is None


class TestVehicleRepositoryGetAvailableVehicles:
    """Tests para get_available_vehicles"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return VehicleRepository()
    
    def test_get_available_vehicles_returns_list(self, repository, mock_db):
        """Debe retornar lista de vehículos disponibles"""
        mock_vehicles = [Mock(spec=Vehicle), Mock(spec=Vehicle), Mock(spec=Vehicle)]
        
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_vehicles
        
        result = repository.get_available_vehicles(mock_db)
        
        assert result == mock_vehicles
        assert len(result) == 3
    
    def test_get_available_vehicles_empty(self, repository, mock_db):
        """Debe retornar lista vacía si no hay vehículos disponibles"""
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        result = repository.get_available_vehicles(mock_db)
        
        assert result == []
    
    def test_get_available_vehicles_with_pagination(self, repository, mock_db):
        """Debe aplicar paginación"""
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        repository.get_available_vehicles(mock_db, skip=20, limit=10)
        
        mock_db.query.return_value.filter.return_value.offset.assert_called_once_with(20)
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.assert_called_once_with(10)

