"""
Tests unitarios para ClientService
"""
import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session


class TestClientService:
    """Tests para ClientService usando mocks directos"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock de sesión de base de datos"""
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_repository(self):
        """Mock del repository"""
        return Mock()
    
    @pytest.fixture
    def client_service(self, mock_repository):
        """Instancia de ClientService con repository mockeado"""
        from app.services.client_service import ClientService
        service = ClientService()
        service.repository = mock_repository
        return service


class TestGetByEmail:
    """Tests para get_by_email"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.client_service import ClientService
        service = ClientService()
        service.repository = Mock()
        return service
    
    def test_get_by_email_found(self, service, mock_db):
        """Debe retornar cliente cuando existe"""
        expected_client = Mock()
        expected_client.email = "test@example.com"
        
        service.repository.get_by_email.return_value = expected_client
        
        result = service.get_by_email(mock_db, "test@example.com")
        
        assert result == expected_client
        service.repository.get_by_email.assert_called_once_with(mock_db, "test@example.com")
    
    def test_get_by_email_not_found(self, service, mock_db):
        """Debe retornar None cuando no existe"""
        service.repository.get_by_email.return_value = None
        
        result = service.get_by_email(mock_db, "noexiste@example.com")
        
        assert result is None


class TestGetByCompany:
    """Tests para get_by_company"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.client_service import ClientService
        service = ClientService()
        service.repository = Mock()
        return service
    
    def test_get_by_company_returns_list(self, service, mock_db):
        """Debe retornar lista de clientes por empresa"""
        mock_clients = [Mock(), Mock()]
        service.repository.get_by_company.return_value = mock_clients
        
        result = service.get_by_company(mock_db, "Empresa ABC")
        
        assert result == mock_clients
        assert len(result) == 2
    
    def test_get_by_company_with_pagination(self, service, mock_db):
        """Debe respetar parámetros de paginación"""
        service.repository.get_by_company.return_value = []
        
        service.get_by_company(mock_db, "Empresa", skip=10, limit=50)
        
        service.repository.get_by_company.assert_called_once_with(
            mock_db, "Empresa", 10, 50
        )
    
    def test_get_by_company_empty(self, service, mock_db):
        """Debe retornar lista vacía si no hay clientes"""
        service.repository.get_by_company.return_value = []
        
        result = service.get_by_company(mock_db, "Empresa Inexistente")
        
        assert result == []


class TestGetActiveClients:
    """Tests para get_active_clients"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.client_service import ClientService
        service = ClientService()
        service.repository = Mock()
        return service
    
    def test_get_active_clients_returns_list(self, service, mock_db):
        """Debe retornar lista de clientes activos"""
        mock_clients = [Mock(), Mock(), Mock()]
        service.repository.get_active_clients.return_value = mock_clients
        
        result = service.get_active_clients(mock_db)
        
        assert result == mock_clients
        assert len(result) == 3
    
    def test_get_active_clients_with_pagination(self, service, mock_db):
        """Debe respetar parámetros de paginación"""
        service.repository.get_active_clients.return_value = []
        
        service.get_active_clients(mock_db, skip=5, limit=25)
        
        service.repository.get_active_clients.assert_called_once_with(
            mock_db, 5, 25
        )
    
    def test_get_active_clients_default_pagination(self, service, mock_db):
        """Debe usar paginación por defecto"""
        service.repository.get_active_clients.return_value = []
        
        service.get_active_clients(mock_db)
        
        service.repository.get_active_clients.assert_called_once_with(
            mock_db, 0, 100
        )
