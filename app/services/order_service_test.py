"""
Tests unitarios para OrderService
"""
import pytest
from unittest.mock import Mock
from datetime import datetime
from sqlalchemy.orm import Session


class TestGetByClient:
    """Tests para get_by_client"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_get_by_client_returns_list(self, service, mock_db):
        """Debe retornar lista de pedidos del cliente"""
        mock_orders = [Mock(), Mock()]
        service.repository.get_by_client.return_value = mock_orders
        
        result = service.get_by_client(mock_db, client_id=1)
        
        assert result == mock_orders
        assert len(result) == 2
    
    def test_get_by_client_with_pagination(self, service, mock_db):
        """Debe respetar parámetros de paginación"""
        service.repository.get_by_client.return_value = []
        
        service.get_by_client(mock_db, client_id=1, skip=10, limit=50)
        
        service.repository.get_by_client.assert_called_once_with(mock_db, 1, 10, 50)


class TestGetByDriver:
    """Tests para get_by_driver"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_get_by_driver_returns_list(self, service, mock_db):
        """Debe retornar lista de pedidos del conductor"""
        mock_orders = [Mock()]
        service.repository.get_by_driver.return_value = mock_orders
        
        result = service.get_by_driver(mock_db, driver_id=1)
        
        assert result == mock_orders


class TestGetByStatus:
    """Tests para get_by_status"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_get_by_status_pendiente(self, service, mock_db):
        """Debe retornar pedidos pendientes"""
        mock_orders = [Mock()]
        service.repository.get_by_status.return_value = mock_orders
        
        result = service.get_by_status(mock_db, status="pendiente")
        
        assert result == mock_orders
        service.repository.get_by_status.assert_called_once_with(mock_db, "pendiente", 0, 100)


class TestGetByTrackingCode:
    """Tests para get_by_tracking_code"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_get_by_tracking_code_found(self, service, mock_db):
        """Debe retornar pedido cuando existe"""
        mock_order = Mock()
        service.repository.get_by_tracking_code.return_value = mock_order
        
        result = service.get_by_tracking_code(mock_db, "TRK-ABC123")
        
        assert result == mock_order
    
    def test_get_by_tracking_code_not_found(self, service, mock_db):
        """Debe retornar None cuando no existe"""
        service.repository.get_by_tracking_code.return_value = None
        
        result = service.get_by_tracking_code(mock_db, "TRK-INVALID")
        
        assert result is None


class TestGetByOrderNumber:
    """Tests para get_by_order_number"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_get_by_order_number_found(self, service, mock_db):
        """Debe retornar pedido cuando existe"""
        mock_order = Mock()
        service.repository.get_by_order_number.return_value = mock_order
        
        result = service.get_by_order_number(mock_db, "ORD-20241126-0001")
        
        assert result == mock_order


class TestGetUnassigned:
    """Tests para get_unassigned"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_get_unassigned_returns_list(self, service, mock_db):
        """Debe retornar lista de pedidos sin asignar"""
        mock_orders = [Mock()]
        service.repository.get_unassigned.return_value = mock_orders
        
        result = service.get_unassigned(mock_db)
        
        assert result == mock_orders


class TestUpdateStatus:
    """Tests para update_status"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_update_status_success(self, service, mock_db):
        """Debe actualizar estado exitosamente"""
        mock_order = Mock()
        service.repository.update_status.return_value = mock_order
        
        result = service.update_status(mock_db, order_id=1, status="entregado")
        
        assert result == mock_order
        service.repository.update_status.assert_called_once_with(mock_db, 1, "entregado")


class TestAssignDriverAndVehicle:
    """Tests para assign_driver_and_vehicle"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_assign_driver_and_vehicle_success(self, service, mock_db):
        """Debe asignar conductor y vehículo exitosamente"""
        assignment = Mock()
        assignment.driver_id = 1
        assignment.vehicle_id = 1
        assignment.tracking_code = "TRK-ABC123"
        
        mock_order = Mock()
        service.repository.assign_driver_and_vehicle.return_value = mock_order
        
        result = service.assign_driver_and_vehicle(mock_db, order_id=1, assignment=assignment)
        
        assert result == mock_order
        service.repository.assign_driver_and_vehicle.assert_called_once_with(
            mock_db, 1, 1, 1, "TRK-ABC123"
        )


class TestGetByDateRange:
    """Tests para get_by_date_range"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_get_by_date_range_returns_list(self, service, mock_db):
        """Debe retornar pedidos en el rango de fechas"""
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        mock_orders = [Mock(), Mock()]
        
        service.repository.get_by_date_range.return_value = mock_orders
        
        result = service.get_by_date_range(mock_db, start_date, end_date)
        
        assert result == mock_orders
        service.repository.get_by_date_range.assert_called_once_with(
            mock_db, start_date, end_date, 0, 100
        )


class TestGetByCity:
    """Tests para get_by_city"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.order_service import OrderService
        service = OrderService()
        service.repository = Mock()
        return service
    
    def test_get_by_city_returns_list(self, service, mock_db):
        """Debe retornar pedidos de la ciudad"""
        mock_orders = [Mock()]
        service.repository.get_by_city.return_value = mock_orders
        
        result = service.get_by_city(mock_db, "Bogotá")
        
        assert result == mock_orders
