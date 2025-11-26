"""
Tests unitarios para schemas de cliente
"""
import pytest
from pydantic import ValidationError

from app.schemas.client_schemas import ClientCreate, ClientUpdate, ClientResponse, ClientSummary


class TestClientCreate:
    """Tests para ClientCreate schema"""
    
    def test_create_valid_client(self):
        """Debe crear cliente con datos válidos"""
        client = ClientCreate(
            name="Juan Pérez",
            email="juan@example.com",
            phone="3001234567"
        )
        assert client.name == "Juan Pérez"
        assert client.email == "juan@example.com"
        assert client.phone == "3001234567"
        assert client.client_type == "individual"  # default
        assert client.status == "activo"  # default
        assert client.is_active is True  # default
    
    def test_create_client_with_company(self):
        """Debe crear cliente con empresa"""
        client = ClientCreate(
            name="Juan Pérez",
            email="juan@example.com",
            phone="3001234567",
            company="Empresa ABC"
        )
        assert client.company == "Empresa ABC"
    
    def test_create_client_custom_type(self):
        """Debe crear cliente con tipo personalizado"""
        client = ClientCreate(
            name="Empresa XYZ",
            email="empresa@example.com",
            phone="3009876543",
            client_type="empresa"
        )
        assert client.client_type == "empresa"
    
    def test_create_client_missing_name(self):
        """Debe fallar sin nombre"""
        with pytest.raises(ValidationError):
            ClientCreate(
                email="test@example.com",
                phone="3001234567"
            )
    
    def test_create_client_missing_email(self):
        """Debe fallar sin email"""
        with pytest.raises(ValidationError):
            ClientCreate(
                name="Juan Pérez",
                phone="3001234567"
            )
    
    def test_create_client_missing_phone(self):
        """Debe fallar sin teléfono"""
        with pytest.raises(ValidationError):
            ClientCreate(
                name="Juan Pérez",
                email="juan@example.com"
            )


class TestClientUpdate:
    """Tests para ClientUpdate schema"""
    
    def test_update_all_fields_optional(self):
        """Todos los campos deben ser opcionales"""
        update = ClientUpdate()
        assert update.name is None
        assert update.email is None
        assert update.phone is None
    
    def test_update_partial_fields(self):
        """Debe permitir actualización parcial"""
        update = ClientUpdate(name="Nuevo Nombre")
        assert update.name == "Nuevo Nombre"
        assert update.email is None
    
    def test_update_multiple_fields(self):
        """Debe permitir actualizar múltiples campos"""
        update = ClientUpdate(
            name="Nuevo Nombre",
            email="nuevo@email.com",
            status="inactivo"
        )
        assert update.name == "Nuevo Nombre"
        assert update.email == "nuevo@email.com"
        assert update.status == "inactivo"


class TestClientResponse:
    """Tests para ClientResponse schema"""
    
    def test_response_from_dict(self):
        """Debe crear response desde diccionario"""
        data = {
            "id": 1,
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "phone": "3001234567",
            "company": "Empresa ABC",
            "client_type": "individual",
            "status": "activo",
            "is_active": True
        }
        response = ClientResponse(**data)
        assert response.id == 1
        assert response.name == "Juan Pérez"
    
    def test_response_company_optional(self):
        """Company debe ser opcional"""
        data = {
            "id": 1,
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "phone": "3001234567",
            "company": None,
            "client_type": "individual",
            "status": "activo",
            "is_active": True
        }
        response = ClientResponse(**data)
        assert response.company is None


class TestClientSummary:
    """Tests para ClientSummary schema"""
    
    def test_summary_from_dict(self):
        """Debe crear summary desde diccionario"""
        data = {
            "id": 1,
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "phone": "3001234567",
            "company": None,
            "client_type": "individual",
            "status": "activo",
            "is_active": True
        }
        summary = ClientSummary(**data)
        assert summary.id == 1
        assert summary.name == "Juan Pérez"

