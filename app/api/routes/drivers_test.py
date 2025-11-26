"""
Tests unitarios para rutas de conductores
"""
import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from sqlalchemy.orm import Session


class TestGetDrivers:
    """Tests para GET /drivers"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_drivers_success(self, mock_db, mock_service):
        """Debe retornar lista de conductores"""
        from app.api.routes.drivers import get_drivers
        
        mock_drivers = [
            Mock(id=1, first_name="Carlos"),
            Mock(id=2, first_name="Juan")
        ]
        mock_service.get_all.return_value = mock_drivers
        
        result = await get_drivers(db=mock_db, driver_service=mock_service)
        
        assert result == mock_drivers
    
    @pytest.mark.asyncio
    async def test_get_drivers_empty(self, mock_db, mock_service):
        """Debe retornar lista vacía"""
        from app.api.routes.drivers import get_drivers
        
        mock_service.get_all.return_value = []
        
        result = await get_drivers(db=mock_db, driver_service=mock_service)
        
        assert result == []


class TestGetAvailableDrivers:
    """Tests para GET /drivers/available"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_available_drivers(self, mock_db, mock_service):
        """Debe retornar conductores disponibles"""
        from app.api.routes.drivers import get_available_drivers
        
        mock_drivers = [Mock(id=1, is_available=True)]
        mock_service.get_available_drivers.return_value = mock_drivers
        
        result = await get_available_drivers(db=mock_db, driver_service=mock_service)
        
        assert result == mock_drivers


class TestCreateDriver:
    """Tests para POST /drivers"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_create_driver_success(self, mock_db, mock_service):
        """Debe crear conductor exitosamente"""
        from app.api.routes.drivers import create_driver
        from app.schemas.driver_schemas import DriverCreate
        
        driver_data = DriverCreate(
            first_name="Carlos",
            last_name="García",
            email="carlos@example.com",
            phone="3001234567",
            document_number="12345678",
            license_type="C"
        )
        
        mock_service.get_by_email.return_value = None
        mock_service.get_by_document.return_value = None
        mock_created = Mock(id=1, first_name="Carlos")
        mock_service.create.return_value = mock_created
        
        result = await create_driver(
            driver_data=driver_data,
            db=mock_db,
            driver_service=mock_service
        )
        
        assert result == mock_created
    
    @pytest.mark.asyncio
    async def test_create_driver_email_exists(self, mock_db, mock_service):
        """Debe fallar si email ya existe"""
        from app.api.routes.drivers import create_driver
        from app.schemas.driver_schemas import DriverCreate
        
        driver_data = DriverCreate(
            first_name="Carlos",
            last_name="García",
            email="existente@example.com",
            phone="3001234567",
            document_number="12345678",
            license_type="C"
        )
        
        mock_service.get_by_email.return_value = Mock(email="existente@example.com")
        
        with pytest.raises(HTTPException) as exc_info:
            await create_driver(
                driver_data=driver_data,
                db=mock_db,
                driver_service=mock_service
            )
        
        assert exc_info.value.status_code == 400


class TestGetDriver:
    """Tests para GET /drivers/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_driver_found(self, mock_db, mock_service):
        """Debe retornar conductor cuando existe"""
        from app.api.routes.drivers import get_driver
        
        mock_driver = Mock(id=1, first_name="Carlos")
        mock_service.get_by_id.return_value = mock_driver
        
        result = await get_driver(
            driver_id=1,
            db=mock_db,
            driver_service=mock_service
        )
        
        assert result == mock_driver
    
    @pytest.mark.asyncio
    async def test_get_driver_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.drivers import get_driver
        
        mock_service.get_by_id.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_driver(
                driver_id=999,
                db=mock_db,
                driver_service=mock_service
            )
        
        assert exc_info.value.status_code == 404


class TestDeleteDriver:
    """Tests para DELETE /drivers/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_delete_driver_success(self, mock_db, mock_service):
        """Debe eliminar conductor exitosamente"""
        from app.api.routes.drivers import delete_driver
        
        mock_service.get_by_id.return_value = Mock(id=1)
        mock_service.delete.return_value = True
        
        result = await delete_driver(
            driver_id=1,
            db=mock_db,
            driver_service=mock_service
        )
        
        assert "exitosamente" in result["message"]
    
    @pytest.mark.asyncio
    async def test_delete_driver_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.drivers import delete_driver
        
        mock_service.get_by_id.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await delete_driver(
                driver_id=999,
                db=mock_db,
                driver_service=mock_service
            )
        
        assert exc_info.value.status_code == 404

