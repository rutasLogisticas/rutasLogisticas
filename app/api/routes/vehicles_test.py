"""
Tests unitarios para rutas de vehículos
"""
import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from sqlalchemy.orm import Session


class TestGetVehicles:
    """Tests para GET /vehicles"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_vehicles_success(self, mock_db, mock_service):
        """Debe retornar lista de vehículos"""
        from app.api.routes.vehicles import get_vehicles
        
        mock_vehicles = [
            Mock(id=1, license_plate="ABC123"),
            Mock(id=2, license_plate="XYZ789")
        ]
        mock_service.get_all.return_value = mock_vehicles
        
        result = await get_vehicles(db=mock_db, vehicle_service=mock_service)
        
        assert result == mock_vehicles
    
    @pytest.mark.asyncio
    async def test_get_vehicles_empty(self, mock_db, mock_service):
        """Debe retornar lista vacía"""
        from app.api.routes.vehicles import get_vehicles
        
        mock_service.get_all.return_value = []
        
        result = await get_vehicles(db=mock_db, vehicle_service=mock_service)
        
        assert result == []


class TestCreateVehicle:
    """Tests para POST /vehicles"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_create_vehicle_success(self, mock_db, mock_service):
        """Debe crear vehículo exitosamente"""
        from app.api.routes.vehicles import create_vehicle
        from app.schemas.vehicle_schemas import VehicleCreate
        
        vehicle_data = VehicleCreate(
            license_plate="ABC123",
            brand="Toyota",
            model="Hilux",
            year=2022,
            vehicle_type="camioneta"
        )
        
        mock_service.get_by_license_plate.return_value = None
        mock_created = Mock(id=1, license_plate="ABC123")
        mock_service.create.return_value = mock_created
        
        result = await create_vehicle(
            vehicle_data=vehicle_data,
            db=mock_db,
            vehicle_service=mock_service
        )
        
        assert result == mock_created
    
    @pytest.mark.asyncio
    async def test_create_vehicle_plate_exists(self, mock_db, mock_service):
        """Debe fallar si placa ya existe"""
        from app.api.routes.vehicles import create_vehicle
        from app.schemas.vehicle_schemas import VehicleCreate
        
        vehicle_data = VehicleCreate(
            license_plate="ABC123",
            brand="Toyota",
            model="Hilux",
            year=2022,
            vehicle_type="camioneta"
        )
        
        mock_service.get_by_license_plate.return_value = Mock(license_plate="ABC123")
        
        with pytest.raises(HTTPException) as exc_info:
            await create_vehicle(
                vehicle_data=vehicle_data,
                db=mock_db,
                vehicle_service=mock_service
            )
        
        assert exc_info.value.status_code == 400


class TestGetVehicle:
    """Tests para GET /vehicles/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_get_vehicle_found(self, mock_db, mock_service):
        """Debe retornar vehículo cuando existe"""
        from app.api.routes.vehicles import get_vehicle
        
        mock_vehicle = Mock(id=1, license_plate="ABC123")
        mock_service.get_by_id.return_value = mock_vehicle
        
        result = await get_vehicle(
            vehicle_id=1,
            db=mock_db,
            vehicle_service=mock_service
        )
        
        assert result == mock_vehicle
    
    @pytest.mark.asyncio
    async def test_get_vehicle_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.vehicles import get_vehicle
        
        mock_service.get_by_id.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_vehicle(
                vehicle_id=999,
                db=mock_db,
                vehicle_service=mock_service
            )
        
        assert exc_info.value.status_code == 404


class TestUpdateVehicle:
    """Tests para PUT /vehicles/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_update_vehicle_success(self, mock_db, mock_service):
        """Debe actualizar vehículo exitosamente"""
        from app.api.routes.vehicles import update_vehicle
        from app.schemas.vehicle_schemas import VehicleUpdate
        
        vehicle_data = VehicleUpdate(brand="Ford")
        
        mock_existing = Mock(id=1)
        mock_service.get_by_id.return_value = mock_existing
        mock_updated = Mock(id=1, brand="Ford")
        mock_service.update.return_value = mock_updated
        
        result = await update_vehicle(
            vehicle_id=1,
            vehicle_data=vehicle_data,
            db=mock_db,
            vehicle_service=mock_service
        )
        
        assert result == mock_updated
    
    @pytest.mark.asyncio
    async def test_update_vehicle_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.vehicles import update_vehicle
        from app.schemas.vehicle_schemas import VehicleUpdate
        
        vehicle_data = VehicleUpdate(brand="Ford")
        mock_service.get_by_id.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await update_vehicle(
                vehicle_id=999,
                vehicle_data=vehicle_data,
                db=mock_db,
                vehicle_service=mock_service
            )
        
        assert exc_info.value.status_code == 404


class TestDeleteVehicle:
    """Tests para DELETE /vehicles/{id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_service(self):
        return Mock()
    
    @pytest.mark.asyncio
    async def test_delete_vehicle_success(self, mock_db, mock_service):
        """Debe eliminar vehículo exitosamente"""
        from app.api.routes.vehicles import delete_vehicle
        
        mock_service.get_by_id.return_value = Mock(id=1)
        mock_service.delete.return_value = True
        
        result = await delete_vehicle(
            vehicle_id=1,
            db=mock_db,
            vehicle_service=mock_service
        )
        
        assert "exitosamente" in result["message"]
    
    @pytest.mark.asyncio
    async def test_delete_vehicle_not_found(self, mock_db, mock_service):
        """Debe retornar 404 si no existe"""
        from app.api.routes.vehicles import delete_vehicle
        
        mock_service.get_by_id.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await delete_vehicle(
                vehicle_id=999,
                db=mock_db,
                vehicle_service=mock_service
            )
        
        assert exc_info.value.status_code == 404

