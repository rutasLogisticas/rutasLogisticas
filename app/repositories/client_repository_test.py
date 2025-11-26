"""
Tests unitarios para ClientRepository
"""
import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session

from app.repositories.client_repository import ClientRepository
from app.models.client import Client


class TestClientRepositoryGetByEmail:
    """Tests para get_by_email"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return ClientRepository()
    
    def test_get_by_email_found(self, repository, mock_db):
        """Debe retornar cliente cuando existe"""
        mock_client = Mock(spec=Client)
        mock_client.email = "test@example.com"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_client
        
        result = repository.get_by_email(mock_db, "test@example.com")
        
        assert result == mock_client
    
    def test_get_by_email_not_found(self, repository, mock_db):
        """Debe retornar None cuando no existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = repository.get_by_email(mock_db, "noexiste@example.com")
        
        assert result is None


class TestClientRepositoryGetByCompany:
    """Tests para get_by_company"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return ClientRepository()
    
    def test_get_by_company_returns_list(self, repository, mock_db):
        """Debe retornar lista de clientes"""
        mock_clients = [Mock(spec=Client), Mock(spec=Client)]
        
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_clients
        
        result = repository.get_by_company(mock_db, "Empresa ABC")
        
        assert result == mock_clients
        assert len(result) == 2
    
    def test_get_by_company_empty(self, repository, mock_db):
        """Debe retornar lista vacía si no hay clientes"""
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        result = repository.get_by_company(mock_db, "Empresa Inexistente")
        
        assert result == []


class TestClientRepositoryGetActiveClients:
    """Tests para get_active_clients"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return ClientRepository()
    
    def test_get_active_clients_returns_list(self, repository, mock_db):
        """Debe retornar lista de clientes activos"""
        mock_clients = [Mock(spec=Client), Mock(spec=Client), Mock(spec=Client)]
        
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_clients
        
        result = repository.get_active_clients(mock_db)
        
        assert result == mock_clients
        assert len(result) == 3
    
    def test_get_active_clients_with_pagination(self, repository, mock_db):
        """Debe aplicar paginación"""
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        repository.get_active_clients(mock_db, skip=10, limit=50)
        
        # Verificar que se llamó offset y limit
        mock_db.query.return_value.filter.return_value.offset.assert_called_once_with(10)
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.assert_called_once_with(50)

