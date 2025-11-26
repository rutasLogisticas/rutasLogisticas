"""
Tests unitarios para rutas de clientes
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import HTTPException
from sqlalchemy.orm import Session


class TestGetClients:
    """Tests para GET /clients"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_clients_success(self, mock_db, mock_service):
        """Debe retornar lista de clientes"""
        from app.api.routes.clients import get_clients
        
        mock_clients = [
            Mock(id=1, name="Cliente 1"),
            Mock(id=2, name="Cliente 2")
        ]
        mock_service.get_all.return_value = mock_clients
        
        result = await get_clients(db=mock_db, client_service=mock_service)
        
        assert result == mock_clients
        mock_service.get_all.assert_called_once_with(mock_db, skip=0, limit=100)
    
    @pytest.mark.asyncio
    async def test_get_clients_empty(self, mock_db, mock_service):
        """Debe retornar lista vacía"""
        from app.api.routes.clients import get_clients
        
        mock_service.get_all.return_value = []
        
        result = await get_clients(db=mock_db, client_service=mock_service)
        
        assert result == []


class TestCreateClient:
    """Tests para POST /clients"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_create_client_success(self, mock_db, mock_service):
        """Debe crear cliente exitosamente"""
        from app.api.routes.clients import create_client
        from app.schemas.client_schemas import ClientCreate
        
        client_data = ClientCreate(
            name="Nuevo Cliente",
            email="nuevo@example.com",
            phone="3001234567"
        )
        
        mock_service.get_by_email.return_value = None
        mock_created = Mock(id=1, name="Nuevo Cliente")
        mock_service.create.return_value = mock_created
        
        result = await create_client(
            client_data=client_data,
            db=mock_db,
            client_service=mock_service
        )
        
        assert result == mock_created
    
    @pytest.mark.asyncio
    async def test_create_client_email_exists(self, mock_db, mock_service):
        """Debe fallar si email ya existe"""
        from app.api.routes.clients import create_client
        from app.schemas.client_schemas import ClientCreate
        
        client_data = ClientCreate(
            name="Nuevo Cliente",
            email="existente@example.com",
            phone="3001234567"
        )
        
        mock_service.get_by_email.return_value = Mock(email="existente@example.com")
        
        with pytest.raises(HTTPException) as exc_info:
            await create_client(
                client_data=client_data,
                db=mock_db,
                client_service=mock_service
            )
        
        assert exc_info.value.status_code == 400
        assert "email" in exc_info.value.detail.lower()


class TestGetClient:
    """Tests para GET /clients/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_client_found(self, mock_db, mock_service):
        """Debe retornar cliente cuando existe"""
        from app.api.routes.clients import get_client
        
        mock_client = Mock(id=1, name="Cliente 1")
        mock_service.get_by_id.return_value = mock_client
        
        result = await get_client(
            client_id=1,
            db=mock_db,
            client_service=mock_service
        )
        
        assert result == mock_client
    
    @pytest.mark.asyncio
    async def test_get_client_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.clients import get_client
        
        mock_service.get_by_id.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_client(
                client_id=999,
                db=mock_db,
                client_service=mock_service
            )
        
        assert exc_info.value.status_code == 404


class TestUpdateClient:
    """Tests para PUT /clients/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_update_client_success(self, mock_db, mock_service):
        """Debe actualizar cliente exitosamente"""
        from app.api.routes.clients import update_client
        from app.schemas.client_schemas import ClientUpdate
        
        client_data = ClientUpdate(name="Nombre Actualizado")
        
        mock_existing = Mock(id=1, email="test@example.com")
        mock_service.get_by_id.return_value = mock_existing
        mock_updated = Mock(id=1, name="Nombre Actualizado")
        mock_service.update.return_value = mock_updated
        
        result = await update_client(
            client_id=1,
            client_data=client_data,
            db=mock_db,
            client_service=mock_service
        )
        
        assert result == mock_updated
    
    @pytest.mark.asyncio
    async def test_update_client_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.clients import update_client
        from app.schemas.client_schemas import ClientUpdate
        
        client_data = ClientUpdate(name="Nombre")
        mock_service.get_by_id.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await update_client(
                client_id=999,
                client_data=client_data,
                db=mock_db,
                client_service=mock_service
            )
        
        assert exc_info.value.status_code == 404


class TestDeleteClient:
    """Tests para DELETE /clients/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_delete_client_success(self, mock_db, mock_service):
        """Debe eliminar cliente exitosamente"""
        from app.api.routes.clients import delete_client
        
        mock_service.get_by_id.return_value = Mock(id=1)
        mock_service.delete.return_value = True
        
        result = await delete_client(
            client_id=1,
            db=mock_db,
            client_service=mock_service
        )
        
        assert "exitosamente" in result["message"]
    
    @pytest.mark.asyncio
    async def test_delete_client_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.clients import delete_client
        
        mock_service.get_by_id.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await delete_client(
                client_id=999,
                db=mock_db,
                client_service=mock_service
            )
        
        assert exc_info.value.status_code == 404

