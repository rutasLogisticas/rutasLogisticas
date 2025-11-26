"""
Tests unitarios para OrderRepository
"""
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.repositories.order_repository import OrderRepository
from app.models.order import Order


class TestOrderRepositoryGetByClient:
    """Tests para get_by_client"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return OrderRepository()
    
    def test_get_by_client_returns_list(self, repository, mock_db):
        """Debe retornar lista de pedidos"""
        mock_orders = [Mock(spec=Order), Mock(spec=Order)]
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_orders
        
        result = repository.get_by_client(mock_db, client_id=1)
        
        assert result == mock_orders
        assert len(result) == 2
    
    def test_get_by_client_empty(self, repository, mock_db):
        """Debe retornar lista vacía si no hay pedidos"""
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        result = repository.get_by_client(mock_db, client_id=999)
        
        assert result == []


class TestOrderRepositoryGetByDriver:
    """Tests para get_by_driver"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return OrderRepository()
    
    def test_get_by_driver_returns_list(self, repository, mock_db):
        """Debe retornar lista de pedidos"""
        mock_orders = [Mock(spec=Order)]
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_orders
        
        result = repository.get_by_driver(mock_db, driver_id=1)
        
        assert result == mock_orders


class TestOrderRepositoryGetByStatus:
    """Tests para get_by_status"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return OrderRepository()
    
    def test_get_by_status_returns_list(self, repository, mock_db):
        """Debe retornar lista de pedidos por estado"""
        mock_orders = [Mock(spec=Order, status="pendiente")]
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_orders
        
        result = repository.get_by_status(mock_db, status="pendiente")
        
        assert result == mock_orders


class TestOrderRepositoryGetByTrackingCode:
    """Tests para get_by_tracking_code"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return OrderRepository()
    
    def test_get_by_tracking_code_found(self, repository, mock_db):
        """Debe retornar pedido cuando existe"""
        mock_order = Mock(spec=Order, tracking_code="TRK123")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_order
        
        result = repository.get_by_tracking_code(mock_db, "TRK123")
        
        assert result == mock_order
    
    def test_get_by_tracking_code_not_found(self, repository, mock_db):
        """Debe retornar None cuando no existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = repository.get_by_tracking_code(mock_db, "NOEXISTE")
        
        assert result is None


class TestOrderRepositoryGetByOrderNumber:
    """Tests para get_by_order_number"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return OrderRepository()
    
    def test_get_by_order_number_found(self, repository, mock_db):
        """Debe retornar pedido cuando existe"""
        mock_order = Mock(spec=Order, order_number="ORD-001")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_order
        
        result = repository.get_by_order_number(mock_db, "ORD-001")
        
        assert result == mock_order
    
    def test_get_by_order_number_not_found(self, repository, mock_db):
        """Debe retornar None cuando no existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = repository.get_by_order_number(mock_db, "NOEXISTE")
        
        assert result is None


class TestOrderRepositoryGetUnassigned:
    """Tests para get_unassigned"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return OrderRepository()
    
    def test_get_unassigned_returns_list(self, repository, mock_db):
        """Debe retornar lista de pedidos sin asignar"""
        mock_orders = [Mock(spec=Order, driver_id=None)]
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_orders
        
        result = repository.get_unassigned(mock_db)
        
        assert result == mock_orders


class TestOrderRepositoryGetByCity:
    """Tests para get_by_city"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return OrderRepository()
    
    def test_get_by_city_returns_list(self, repository, mock_db):
        """Debe retornar lista de pedidos por ciudad"""
        mock_orders = [Mock(spec=Order, origin_city="Bogotá")]
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_orders
        
        result = repository.get_by_city(mock_db, "Bogotá")
        
        assert result == mock_orders

