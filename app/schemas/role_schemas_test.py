"""
Tests unitarios para schemas de roles
"""
import pytest
from pydantic import ValidationError

from app.schemas.role_schemas import (
    PermissionBase, PermissionCreate, PermissionResponse,
    RoleBase, RoleCreate, RoleUpdate, RoleResponse, RoleSummary
)


class TestPermissionBase:
    """Tests para PermissionBase schema"""
    
    def test_permission_base_valid(self):
        """Debe crear permiso base válido"""
        permission = PermissionBase(
            name="crear_usuarios",
            resource="users",
            action="create"
        )
        assert permission.name == "crear_usuarios"
        assert permission.resource == "users"
        assert permission.action == "create"
    
    def test_permission_base_with_description(self):
        """Debe crear permiso con descripción"""
        permission = PermissionBase(
            name="crear_usuarios",
            resource="users",
            action="create",
            description="Permite crear nuevos usuarios"
        )
        assert permission.description == "Permite crear nuevos usuarios"
    
    def test_permission_base_missing_name(self):
        """Debe fallar sin nombre"""
        with pytest.raises(ValidationError):
            PermissionBase(resource="users", action="create")


class TestPermissionCreate:
    """Tests para PermissionCreate schema"""
    
    def test_create_permission_valid(self):
        """Debe crear permiso válido"""
        permission = PermissionCreate(
            name="leer_vehiculos",
            resource="vehicles",
            action="read"
        )
        assert permission.name == "leer_vehiculos"


class TestPermissionResponse:
    """Tests para PermissionResponse schema"""
    
    def test_response_from_dict(self):
        """Debe crear response desde diccionario"""
        data = {
            "id": 1,
            "name": "crear_usuarios",
            "resource": "users",
            "action": "create",
            "description": None,
            "is_active": True
        }
        response = PermissionResponse(**data)
        assert response.id == 1
        assert response.is_active is True


class TestRoleBase:
    """Tests para RoleBase schema"""
    
    def test_role_base_valid(self):
        """Debe crear rol base válido"""
        role = RoleBase(name="admin")
        assert role.name == "admin"
        assert role.description is None
    
    def test_role_base_with_description(self):
        """Debe crear rol con descripción"""
        role = RoleBase(
            name="admin",
            description="Administrador del sistema"
        )
        assert role.description == "Administrador del sistema"
    
    def test_role_base_missing_name(self):
        """Debe fallar sin nombre"""
        with pytest.raises(ValidationError):
            RoleBase()


class TestRoleCreate:
    """Tests para RoleCreate schema"""
    
    def test_create_role_valid(self):
        """Debe crear rol válido"""
        role = RoleCreate(name="operador")
        assert role.name == "operador"
        assert role.permission_ids == []  # default
    
    def test_create_role_with_permissions(self):
        """Debe crear rol con permisos"""
        role = RoleCreate(
            name="operador",
            permission_ids=[1, 2, 3]
        )
        assert len(role.permission_ids) == 3


class TestRoleUpdate:
    """Tests para RoleUpdate schema"""
    
    def test_update_all_fields_optional(self):
        """Todos los campos deben ser opcionales"""
        update = RoleUpdate()
        assert update.name is None
        assert update.description is None
        assert update.permission_ids is None
        assert update.is_active is None
    
    def test_update_partial_fields(self):
        """Debe permitir actualización parcial"""
        update = RoleUpdate(name="nuevo_nombre")
        assert update.name == "nuevo_nombre"
        assert update.description is None
    
    def test_update_permissions(self):
        """Debe actualizar permisos"""
        update = RoleUpdate(permission_ids=[4, 5, 6])
        assert update.permission_ids == [4, 5, 6]
    
    def test_update_deactivate(self):
        """Debe desactivar rol"""
        update = RoleUpdate(is_active=False)
        assert update.is_active is False


class TestRoleResponse:
    """Tests para RoleResponse schema"""
    
    def test_response_from_dict(self):
        """Debe crear response desde diccionario"""
        data = {
            "id": 1,
            "name": "admin",
            "description": "Administrador",
            "is_active": True,
            "permissions": []
        }
        response = RoleResponse(**data)
        assert response.id == 1
        assert response.name == "admin"
        assert response.permissions == []
    
    def test_response_with_permissions(self):
        """Debe crear response con permisos"""
        data = {
            "id": 1,
            "name": "admin",
            "description": None,
            "is_active": True,
            "permissions": [
                {"id": 1, "name": "crear", "resource": "users", "action": "create", "description": None, "is_active": True}
            ]
        }
        response = RoleResponse(**data)
        assert len(response.permissions) == 1


class TestRoleSummary:
    """Tests para RoleSummary schema"""
    
    def test_summary_from_dict(self):
        """Debe crear summary desde diccionario"""
        data = {
            "id": 1,
            "name": "admin",
            "description": "Administrador",
            "is_active": True,
            "permissions_count": 5
        }
        summary = RoleSummary(**data)
        assert summary.id == 1
        assert summary.permissions_count == 5
    
    def test_summary_default_permissions_count(self):
        """Permissions count debe tener default 0"""
        data = {
            "id": 1,
            "name": "admin",
            "description": None,
            "is_active": True
        }
        summary = RoleSummary(**data)
        assert summary.permissions_count == 0

