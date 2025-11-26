"""
Tests unitarios para DriverService
"""
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session


class TestGetByEmail:
    """Tests para get_by_email"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.driver_service import DriverService
        service = DriverService()
        service.repository = Mock()
        return service
    
    def test_get_by_email_found(self, service, mock_db):
        """Debe retornar conductor cuando existe"""
        expected_driver = Mock()
        expected_driver.email = "test@example.com"
        
        service.repository.get_by_email.return_value = expected_driver
        
        result = service.get_by_email(mock_db, "test@example.com")
        
        assert result == expected_driver
        service.repository.get_by_email.assert_called_once_with(mock_db, "test@example.com")
    
    def test_get_by_email_not_found(self, service, mock_db):
        """Debe retornar None cuando no existe"""
        service.repository.get_by_email.return_value = None
        
        result = service.get_by_email(mock_db, "noexiste@example.com")
        
        assert result is None


class TestGetByDocument:
    """Tests para get_by_document"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.driver_service import DriverService
        service = DriverService()
        service.repository = Mock()
        return service
    
    def test_get_by_document_found(self, service, mock_db):
        """Debe retornar conductor cuando existe"""
        expected_driver = Mock()
        expected_driver.document_number = "12345678"
        
        service.repository.get_by_document.return_value = expected_driver
        
        result = service.get_by_document(mock_db, "12345678")
        
        assert result == expected_driver
        service.repository.get_by_document.assert_called_once_with(mock_db, "12345678")
    
    def test_get_by_document_not_found(self, service, mock_db):
        """Debe retornar None cuando no existe"""
        service.repository.get_by_document.return_value = None
        
        result = service.get_by_document(mock_db, "99999999")
        
        assert result is None


class TestGetAvailableDrivers:
    """Tests para get_available_drivers"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.driver_service import DriverService
        service = DriverService()
        service.repository = Mock()
        return service
    
    def test_get_available_drivers_returns_list(self, service, mock_db):
        """Debe retornar lista de conductores disponibles"""
        mock_drivers = [Mock(), Mock()]
        service.repository.get_available_drivers.return_value = mock_drivers
        
        result = service.get_available_drivers(mock_db)
        
        assert result == mock_drivers
        assert len(result) == 2
    
    def test_get_available_drivers_with_pagination(self, service, mock_db):
        """Debe respetar parámetros de paginación"""
        service.repository.get_available_drivers.return_value = []
        
        service.get_available_drivers(mock_db, skip=10, limit=50)
        
        service.repository.get_available_drivers.assert_called_once_with(
            mock_db, 10, 50
        )
    
    def test_get_available_drivers_default_pagination(self, service, mock_db):
        """Debe usar paginación por defecto"""
        service.repository.get_available_drivers.return_value = []
        
        service.get_available_drivers(mock_db)
        
        service.repository.get_available_drivers.assert_called_once_with(
            mock_db, 0, 100
        )
    
    def test_get_available_drivers_empty(self, service, mock_db):
        """Debe retornar lista vacía si no hay conductores disponibles"""
        service.repository.get_available_drivers.return_value = []
        
        result = service.get_available_drivers(mock_db)
        
        assert result == []
