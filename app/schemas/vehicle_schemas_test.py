"""
Tests unitarios para schemas de vehículo
"""
import pytest
from pydantic import ValidationError

from app.schemas.vehicle_schemas import VehicleCreate, VehicleUpdate, VehicleResponse, VehicleSummary


class TestVehicleCreate:
    """Tests para VehicleCreate schema"""
    
    def test_create_valid_vehicle(self):
        """Debe crear vehículo con datos válidos"""
        vehicle = VehicleCreate(
            license_plate="ABC123",
            brand="Toyota",
            model="Hilux",
            year=2022,
            vehicle_type="camioneta"
        )
        assert vehicle.license_plate == "ABC123"
        assert vehicle.brand == "Toyota"
        assert vehicle.model == "Hilux"
        assert vehicle.year == 2022
        assert vehicle.status == "disponible"  # default
    
    def test_create_vehicle_custom_status(self):
        """Debe crear vehículo con estado personalizado"""
        vehicle = VehicleCreate(
            license_plate="ABC123",
            brand="Toyota",
            model="Hilux",
            year=2022,
            vehicle_type="camioneta",
            status="mantenimiento"
        )
        assert vehicle.status == "mantenimiento"
    
    def test_create_vehicle_missing_plate(self):
        """Debe fallar sin placa"""
        with pytest.raises(ValidationError):
            VehicleCreate(
                brand="Toyota",
                model="Hilux",
                year=2022,
                vehicle_type="camioneta"
            )
    
    def test_create_vehicle_missing_brand(self):
        """Debe fallar sin marca"""
        with pytest.raises(ValidationError):
            VehicleCreate(
                license_plate="ABC123",
                model="Hilux",
                year=2022,
                vehicle_type="camioneta"
            )
    
    def test_create_vehicle_missing_year(self):
        """Debe fallar sin año"""
        with pytest.raises(ValidationError):
            VehicleCreate(
                license_plate="ABC123",
                brand="Toyota",
                model="Hilux",
                vehicle_type="camioneta"
            )


class TestVehicleUpdate:
    """Tests para VehicleUpdate schema"""
    
    def test_update_all_fields_optional(self):
        """Todos los campos deben ser opcionales"""
        update = VehicleUpdate()
        assert update.brand is None
        assert update.model is None
        assert update.year is None
    
    def test_update_partial_fields(self):
        """Debe permitir actualización parcial"""
        update = VehicleUpdate(brand="Ford")
        assert update.brand == "Ford"
        assert update.model is None
    
    def test_update_status(self):
        """Debe permitir actualizar estado"""
        update = VehicleUpdate(status="en_ruta")
        assert update.status == "en_ruta"


class TestVehicleResponse:
    """Tests para VehicleResponse schema"""
    
    def test_response_from_dict(self):
        """Debe crear response desde diccionario"""
        data = {
            "id": 1,
            "license_plate": "ABC123",
            "brand": "Toyota",
            "model": "Hilux",
            "year": 2022,
            "vehicle_type": "camioneta",
            "status": "disponible",
            "is_available": True,
            "is_active": True
        }
        response = VehicleResponse(**data)
        assert response.id == 1
        assert response.license_plate == "ABC123"
        assert response.is_available is True
    
    def test_response_with_timestamps(self):
        """Debe aceptar timestamps opcionales"""
        data = {
            "id": 1,
            "license_plate": "ABC123",
            "brand": "Toyota",
            "model": "Hilux",
            "year": 2022,
            "vehicle_type": "camioneta",
            "status": "disponible",
            "is_available": True,
            "is_active": True,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00"
        }
        response = VehicleResponse(**data)
        assert response.created_at == "2024-01-01T00:00:00"


class TestVehicleSummary:
    """Tests para VehicleSummary schema"""
    
    def test_summary_from_dict(self):
        """Debe crear summary desde diccionario"""
        data = {
            "id": 1,
            "license_plate": "ABC123",
            "brand": "Toyota",
            "model": "Hilux",
            "year": 2022,
            "vehicle_type": "camioneta",
            "status": "disponible",
            "is_available": True
        }
        summary = VehicleSummary(**data)
        assert summary.id == 1
        assert summary.license_plate == "ABC123"
    
    def test_summary_year_optional(self):
        """Year debe ser opcional en summary"""
        data = {
            "id": 1,
            "license_plate": "ABC123",
            "brand": "Toyota",
            "model": "Hilux",
            "year": None,
            "vehicle_type": "camioneta",
            "status": "disponible",
            "is_available": True
        }
        summary = VehicleSummary(**data)
        assert summary.year is None

