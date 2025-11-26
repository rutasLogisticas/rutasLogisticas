"""
Tests unitarios para RoleService
"""
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.services.role_service import RoleService, PermissionService


class TestRoleServiceGetRoleByName:
    """Tests para get_role_by_name"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        return RoleService()
    
    def test_get_role_by_name_found(self, service, mock_db):
        """Debe retornar rol por nombre"""
        mock_role = Mock(id=1, name="admin")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_role
        
        result = service.get_role_by_name(mock_db, "admin")
        
        assert result == mock_role
    
    def test_get_role_by_name_not_found(self, service, mock_db):
        """Debe retornar None si no existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = service.get_role_by_name(mock_db, "inexistente")
        
        assert result is None


class TestPermissionServiceGetById:
    """Tests para PermissionService.get_permission_by_id"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        return PermissionService()
    
    def test_get_permission_by_id_found(self, service, mock_db):
        """Debe retornar permiso por ID"""
        mock_permission = Mock(id=1, name="crear_usuario")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_permission
        
        result = service.get_permission_by_id(mock_db, 1)
        
        assert result == mock_permission
    
    def test_get_permission_by_id_not_found(self, service, mock_db):
        """Debe retornar None si no existe"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = service.get_permission_by_id(mock_db, 999)
        
        assert result is None
