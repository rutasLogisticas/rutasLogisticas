"""
Tests unitarios para rutas de pedidos
"""
import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from sqlalchemy.orm import Session


class TestGetOrders:
    """Tests para GET /orders"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_orders_success(self, mock_db, mock_service):
        """Debe retornar lista de pedidos"""
        from app.api.routes.orders import get_orders
        
        mock_orders = [Mock(id=1), Mock(id=2)]
        mock_service.get_all.return_value = mock_orders
        
        result = await get_orders(skip=0, limit=100, db=mock_db, order_service=mock_service)
        
        assert result == mock_orders
    
    @pytest.mark.asyncio
    async def test_get_orders_empty(self, mock_db, mock_service):
        """Debe retornar lista vacía"""
        from app.api.routes.orders import get_orders
        
        mock_service.get_all.return_value = []
        
        result = await get_orders(skip=0, limit=100, db=mock_db, order_service=mock_service)
        
        assert result == []


class TestGetOrder:
    """Tests para GET /orders/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_order_found(self, mock_db, mock_service):
        """Debe retornar pedido cuando existe"""
        from app.api.routes.orders import get_order
        
        mock_order = Mock(id=1)
        mock_service.get_order_with_details.return_value = mock_order
        
        result = await get_order(order_id=1, db=mock_db, order_service=mock_service)
        
        assert result == mock_order
    
    @pytest.mark.asyncio
    async def test_get_order_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.orders import get_order
        
        mock_service.get_order_with_details.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_order(order_id=999, db=mock_db, order_service=mock_service)
        
        assert exc_info.value.status_code == 404


class TestDeleteOrder:
    """Tests para DELETE /orders/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_delete_order_success(self, mock_db, mock_service):
        """Debe eliminar pedido exitosamente"""
        from app.api.routes.orders import delete_order
        
        mock_service.delete.return_value = True
        
        result = await delete_order(order_id=1, db=mock_db, order_service=mock_service)
        
        assert "exitosamente" in result["message"]
    
    @pytest.mark.asyncio
    async def test_delete_order_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.orders import delete_order
        
        mock_service.delete.return_value = False
        
        with pytest.raises(HTTPException) as exc_info:
            await delete_order(order_id=999, db=mock_db, order_service=mock_service)
        
        assert exc_info.value.status_code == 404


class TestGetOrdersByClient:
    """Tests para GET /orders/client/{client_id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_orders_by_client(self, mock_db, mock_service):
        """Debe retornar pedidos del cliente"""
        from app.api.routes.orders import get_orders_by_client
        
        mock_orders = [Mock(id=1, client_id=1)]
        mock_service.get_by_client.return_value = mock_orders
        
        result = await get_orders_by_client(
            client_id=1, skip=0, limit=100,
            db=mock_db, order_service=mock_service
        )
        
        assert result == mock_orders


class TestGetOrdersByStatus:
    """Tests para GET /orders/status/{status}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_orders_by_status(self, mock_db, mock_service):
        """Debe retornar pedidos por estado"""
        from app.api.routes.orders import get_orders_by_status
        
        mock_orders = [Mock(id=1, status="pendiente")]
        mock_service.get_by_status.return_value = mock_orders
        
        result = await get_orders_by_status(
            status="pendiente", skip=0, limit=100,
            db=mock_db, order_service=mock_service
        )
        
        assert result == mock_orders


class TestGetOrderByTracking:
    """Tests para GET /orders/tracking/{tracking_code}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_order_by_tracking_found(self, mock_db, mock_service):
        """Debe retornar pedido por tracking"""
        from app.api.routes.orders import get_order_by_tracking
        
        mock_order = Mock(id=1, tracking_code="TRK123")
        mock_service.get_by_tracking_code.return_value = mock_order
        mock_service.get_order_with_details.return_value = mock_order
        
        result = await get_order_by_tracking(
            tracking_code="TRK123",
            db=mock_db, order_service=mock_service
        )
        
        assert result == mock_order
    
    @pytest.mark.asyncio
    async def test_get_order_by_tracking_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.orders import get_order_by_tracking
        
        mock_service.get_by_tracking_code.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_order_by_tracking(
                tracking_code="NOEXISTE",
                db=mock_db, order_service=mock_service
            )
        
        assert exc_info.value.status_code == 404


class TestGetUnassignedOrders:
    """Tests para GET /orders/unassigned/list"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_unassigned_orders(self, mock_db, mock_service):
        """Debe retornar pedidos sin asignar"""
        from app.api.routes.orders import get_unassigned_orders
        
        mock_orders = [Mock(id=1, driver_id=None)]
        mock_service.get_unassigned.return_value = mock_orders
        
        result = await get_unassigned_orders(
            skip=0, limit=100,
            db=mock_db, order_service=mock_service
        )
        
        assert result == mock_orders


class TestAssignOrder:
    """Tests para POST /orders/{id}/assign"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_assign_order_success(self, mock_db, mock_service):
        """Debe asignar pedido exitosamente"""
        from app.api.routes.orders import assign_order
        from app.schemas.order_schemas import OrderAssignment
        
        assignment = OrderAssignment(driver_id=1, vehicle_id=2)
        mock_order = Mock(id=1, driver_id=1, vehicle_id=2)
        mock_service.assign_driver_and_vehicle.return_value = mock_order
        
        result = await assign_order(
            order_id=1, assignment=assignment,
            db=mock_db, order_service=mock_service
        )
        
        assert result == mock_order
    
    @pytest.mark.asyncio
    async def test_assign_order_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si pedido no existe"""
        from app.api.routes.orders import assign_order
        from app.schemas.order_schemas import OrderAssignment
        
        assignment = OrderAssignment(driver_id=1, vehicle_id=2)
        mock_service.assign_driver_and_vehicle.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await assign_order(
                order_id=999, assignment=assignment,
                db=mock_db, order_service=mock_service
            )
        
        assert exc_info.value.status_code == 404


class TestUpdateOrderStatus:
    """Tests para PATCH /orders/{id}/status"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_update_status_success(self, mock_db, mock_service):
        """Debe actualizar estado exitosamente"""
        from app.api.routes.orders import update_order_status
        
        mock_order = Mock(id=1, status="en_camino")
        mock_service.update_status.return_value = mock_order
        
        result = await update_order_status(
            order_id=1, status="en_camino",
            db=mock_db, order_service=mock_service
        )
        
        assert result == mock_order
    
    @pytest.mark.asyncio
    async def test_update_status_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.orders import update_order_status
        
        mock_service.update_status.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await update_order_status(
                order_id=999, status="entregado",
                db=mock_db, order_service=mock_service
            )
        
        assert exc_info.value.status_code == 404

