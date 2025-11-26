"""
Tests unitarios para DriverRepository
"""
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.repositories.driver_repository import DriverRepository
from app.models.driver import Driver


class TestDriverRepositoryGetByEmail:
    """Tests para get_by_email"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return DriverRepository()
    
    def test_get_by_email_found(self, repository, mock_db):
        """Debe retornar conductor cuando existe"""
        mock_driver = Mock(spec=Driver)
        mock_driver.email = "test@example.com"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_driver
        
        result = repository.get_by_email(mock_db, "test@example.com")
        
        assert result == mock_driver
    
    def test_get_by_email_not_found(self, repository, mock_db):
        """Debe retornar None cuando no existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = repository.get_by_email(mock_db, "noexiste@example.com")
        
        assert result is None


class TestDriverRepositoryGetByDocument:
    """Tests para get_by_document"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return DriverRepository()
    
    def test_get_by_document_found(self, repository, mock_db):
        """Debe retornar conductor cuando existe"""
        mock_driver = Mock(spec=Driver)
        mock_driver.document_number = "12345678"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_driver
        
        result = repository.get_by_document(mock_db, "12345678")
        
        assert result == mock_driver
    
    def test_get_by_document_not_found(self, repository, mock_db):
        """Debe retornar None cuando no existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = repository.get_by_document(mock_db, "99999999")
        
        assert result is None


class TestDriverRepositoryGetAvailableDrivers:
    """Tests para get_available_drivers"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return DriverRepository()
    
    def test_get_available_drivers_returns_list(self, repository, mock_db):
        """Debe retornar lista de conductores disponibles"""
        mock_drivers = [Mock(spec=Driver), Mock(spec=Driver)]
        
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_drivers
        
        result = repository.get_available_drivers(mock_db)
        
        assert result == mock_drivers
        assert len(result) == 2
    
    def test_get_available_drivers_empty(self, repository, mock_db):
        """Debe retornar lista vacía si no hay conductores disponibles"""
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        result = repository.get_available_drivers(mock_db)
        
        assert result == []
    
    def test_get_available_drivers_with_pagination(self, repository, mock_db):
        """Debe aplicar paginación"""
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        repository.get_available_drivers(mock_db, skip=5, limit=25)
        
        mock_db.query.return_value.filter.return_value.offset.assert_called_once_with(5)
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.assert_called_once_with(25)

