"""
Tests unitarios para schemas de conductor
"""
import pytest
from pydantic import ValidationError

from app.schemas.driver_schemas import DriverCreate, DriverUpdate, DriverResponse, DriverSummary


class TestDriverCreate:
    """Tests para DriverCreate schema"""
    
    def test_create_valid_driver(self):
        """Debe crear conductor con datos válidos"""
        driver = DriverCreate(
            first_name="Carlos",
            last_name="García",
            email="carlos@example.com",
            phone="3001234567",
            document_number="12345678",
            license_type="C"
        )
        assert driver.first_name == "Carlos"
        assert driver.last_name == "García"
        assert driver.email == "carlos@example.com"
        assert driver.status == "disponible"  # default
        assert driver.is_available is True  # default
    
    def test_create_driver_custom_status(self):
        """Debe crear conductor con estado personalizado"""
        driver = DriverCreate(
            first_name="Carlos",
            last_name="García",
            email="carlos@example.com",
            phone="3001234567",
            document_number="12345678",
            license_type="C",
            status="ocupado",
            is_available=False
        )
        assert driver.status == "ocupado"
        assert driver.is_available is False
    
    def test_create_driver_missing_first_name(self):
        """Debe fallar sin nombre"""
        with pytest.raises(ValidationError):
            DriverCreate(
                last_name="García",
                email="carlos@example.com",
                phone="3001234567",
                document_number="12345678",
                license_type="C"
            )
    
    def test_create_driver_missing_email(self):
        """Debe fallar sin email"""
        with pytest.raises(ValidationError):
            DriverCreate(
                first_name="Carlos",
                last_name="García",
                phone="3001234567",
                document_number="12345678",
                license_type="C"
            )
    
    def test_create_driver_missing_document(self):
        """Debe fallar sin documento"""
        with pytest.raises(ValidationError):
            DriverCreate(
                first_name="Carlos",
                last_name="García",
                email="carlos@example.com",
                phone="3001234567",
                license_type="C"
            )


class TestDriverUpdate:
    """Tests para DriverUpdate schema"""
    
    def test_update_all_fields_optional(self):
        """Todos los campos deben ser opcionales"""
        update = DriverUpdate()
        assert update.first_name is None
        assert update.last_name is None
        assert update.email is None
    
    def test_update_partial_fields(self):
        """Debe permitir actualización parcial"""
        update = DriverUpdate(first_name="Nuevo Nombre")
        assert update.first_name == "Nuevo Nombre"
        assert update.last_name is None
    
    def test_update_availability(self):
        """Debe permitir actualizar disponibilidad"""
        update = DriverUpdate(is_available=False, status="ocupado")
        assert update.is_available is False
        assert update.status == "ocupado"


class TestDriverResponse:
    """Tests para DriverResponse schema"""
    
    def test_response_from_dict(self):
        """Debe crear response desde diccionario"""
        data = {
            "id": 1,
            "first_name": "Carlos",
            "last_name": "García",
            "email": "carlos@example.com",
            "phone": "3001234567",
            "document_number": "12345678",
            "license_type": "C",
            "status": "disponible",
            "is_available": True
        }
        response = DriverResponse(**data)
        assert response.id == 1
        assert response.first_name == "Carlos"
        assert response.license_type == "C"


class TestDriverSummary:
    """Tests para DriverSummary schema"""
    
    def test_summary_from_dict(self):
        """Debe crear summary desde diccionario"""
        data = {
            "id": 1,
            "first_name": "Carlos",
            "last_name": "García",
            "email": "carlos@example.com",
            "phone": "3001234567",
            "document_number": "12345678",
            "license_type": "C",
            "status": "disponible",
            "is_available": True
        }
        summary = DriverSummary(**data)
        assert summary.id == 1
    
    def test_summary_optional_phone(self):
        """Phone debe ser opcional en summary"""
        data = {
            "id": 1,
            "first_name": "Carlos",
            "last_name": "García",
            "email": "carlos@example.com",
            "phone": None,
            "document_number": None,
            "license_type": "C",
            "status": "disponible",
            "is_available": True
        }
        summary = DriverSummary(**data)
        assert summary.phone is None

