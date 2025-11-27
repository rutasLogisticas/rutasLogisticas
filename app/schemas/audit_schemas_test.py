"""
Tests unitarios para schemas de auditoría
"""
import pytest
from pydantic import ValidationError
from datetime import datetime

from app.schemas.audit_schemas import (
    AuditBase, AuditCreate, AuditResponse, AuditLogOut
)


class TestAuditBase:
    """Tests para AuditBase schema"""
    
    def test_audit_base_valid(self):
        """Debe crear audit base válido"""
        audit = AuditBase(
            event_type="LOGIN",
            description="Usuario inició sesión"
        )
        assert audit.event_type == "LOGIN"
        assert audit.description == "Usuario inició sesión"
        assert audit.actor_id is None
    
    def test_audit_base_with_actor(self):
        """Debe crear audit con actor"""
        audit = AuditBase(
            actor_id=1,
            event_type="LOGOUT",
            description="Usuario cerró sesión",
            ip_address="192.168.1.1"
        )
        assert audit.actor_id == 1
        assert audit.ip_address == "192.168.1.1"
    
    def test_audit_base_with_extra_data(self):
        """Debe crear audit con datos extra"""
        audit = AuditBase(
            event_type="CREATE",
            description="Entidad creada",
            extra_data={"entity": "order", "id": 123}
        )
        assert audit.extra_data == {"entity": "order", "id": 123}
    
    def test_audit_base_missing_event_type(self):
        """Debe fallar sin event_type"""
        with pytest.raises(ValidationError):
            AuditBase(description="Test")
    
    def test_audit_base_missing_description(self):
        """Debe fallar sin description"""
        with pytest.raises(ValidationError):
            AuditBase(event_type="TEST")


class TestAuditCreate:
    """Tests para AuditCreate schema"""
    
    def test_create_valid(self):
        """Debe crear audit create válido"""
        audit = AuditCreate(
            event_type="LOGIN",
            description="Login exitoso"
        )
        assert audit.event_type == "LOGIN"
    
    def test_create_with_all_fields(self):
        """Debe crear con todos los campos"""
        audit = AuditCreate(
            actor_id=5,
            event_type="UPDATE",
            description="Actualización realizada",
            ip_address="10.0.0.1",
            extra_data={"field": "status"}
        )
        assert audit.actor_id == 5
        assert audit.ip_address == "10.0.0.1"


class TestAuditResponse:
    """Tests para AuditResponse schema"""
    
    def test_response_from_dict(self):
        """Debe crear response desde diccionario"""
        data = {
            "id": 1,
            "actor_id": 5,
            "event_type": "LOGIN",
            "description": "Login exitoso",
            "ip_address": "192.168.1.1",
            "extra_data": None,
            "created_at": datetime(2024, 1, 15, 10, 30, 0)
        }
        response = AuditResponse(**data)
        
        assert response.id == 1
        assert response.event_type == "LOGIN"
        assert response.created_at == datetime(2024, 1, 15, 10, 30, 0)
    
    def test_response_without_actor(self):
        """Debe crear response sin actor"""
        data = {
            "id": 2,
            "actor_id": None,
            "event_type": "FAILED_LOGIN",
            "description": "Intento fallido",
            "ip_address": "10.0.0.100",
            "extra_data": None,
            "created_at": datetime.now()
        }
        response = AuditResponse(**data)
        
        assert response.actor_id is None


class TestAuditLogOut:
    """Tests para AuditLogOut schema"""
    
    def test_log_out_from_dict(self):
        """Debe crear log out desde diccionario"""
        data = {
            "id": 1,
            "event_type": "LOGIN",
            "description": "Login exitoso",
            "ip_address": "192.168.1.1",
            "created_at": datetime(2024, 1, 15, 10, 30, 0),
            "usuario": "testuser"
        }
        log = AuditLogOut(**data)
        
        assert log.id == 1
        assert log.usuario == "testuser"
    
    def test_log_out_without_usuario(self):
        """Debe crear log out sin usuario"""
        data = {
            "id": 2,
            "event_type": "FAILED_LOGIN",
            "description": "Intento fallido",
            "ip_address": "10.0.0.1",
            "created_at": datetime.now(),
            "usuario": None
        }
        log = AuditLogOut(**data)
        
        assert log.usuario is None
    
    def test_log_out_missing_required(self):
        """Debe fallar sin campos requeridos"""
        with pytest.raises(ValidationError):
            AuditLogOut(
                id=1,
                event_type="TEST"
                # falta description, ip_address, created_at
            )

