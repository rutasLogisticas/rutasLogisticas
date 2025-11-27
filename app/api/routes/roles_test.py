"""
Tests unitarios para rutas de roles
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session


class TestGetRoles:
    """Tests para GET /roles"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_get_roles_success(self, mock_db):
        """Debe retornar lista de roles"""
        from app.api.routes.roles import get_roles
        
        mock_roles = [
            Mock(id=1, name="admin", description="Admin", is_active=True, permissions_count=5),
            Mock(id=2, name="operador", description="Operador", is_active=True, permissions_count=3)
        ]
        
        with patch('app.api.routes.roles.role_service') as mock_service:
            mock_service.get_roles_summary.return_value = mock_roles
            
            result = get_roles(db=mock_db)
            
            assert result == mock_roles
    
    def test_get_roles_empty(self, mock_db):
        """Debe retornar lista vacía"""
        from app.api.routes.roles import get_roles
        
        with patch('app.api.routes.roles.role_service') as mock_service:
            mock_service.get_roles_summary.return_value = []
            
            result = get_roles(db=mock_db)
            
            assert result == []


class TestGetRole:
    """Tests para GET /roles/{role_id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_get_role_not_found(self, mock_db):
        """Debe retornar 404 si no existe"""
        from app.api.routes.roles import get_role
        
        with patch('app.api.routes.roles.role_service') as mock_service:
            mock_service.get_role_by_id.return_value = None
            
            with pytest.raises(HTTPException) as exc_info:
                get_role(role_id=999, db=mock_db)
            
            assert exc_info.value.status_code == 404


class TestCreateRole:
    """Tests para POST /roles"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_create_role_duplicate(self, mock_db):
        """Debe retornar 400 si rol ya existe"""
        from app.api.routes.roles import create_role
        from app.schemas.role_schemas import RoleCreate
        
        role_data = RoleCreate(name="admin")
        
        with patch('app.api.routes.roles.role_service') as mock_service:
            mock_service.create_role.side_effect = ValueError("Rol ya existe")
            
            with pytest.raises(HTTPException) as exc_info:
                create_role(role_data=role_data, db=mock_db)
            
            assert exc_info.value.status_code == 400


class TestUpdateRole:
    """Tests para PUT /roles/{role_id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_update_role_validation_error(self, mock_db):
        """Debe retornar 400 si hay error de validación"""
        from app.api.routes.roles import update_role
        from app.schemas.role_schemas import RoleUpdate
        
        role_data = RoleUpdate(name="test")
        
        with patch('app.api.routes.roles.role_service') as mock_service:
            mock_service.update_role.side_effect = ValueError("Nombre duplicado")
            
            with pytest.raises(HTTPException) as exc_info:
                update_role(role_id=1, role_data=role_data, db=mock_db)
            
            assert exc_info.value.status_code == 400


class TestDeleteRole:
    """Tests para DELETE /roles/{role_id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_delete_role_success(self, mock_db):
        """Debe eliminar rol exitosamente"""
        from app.api.routes.roles import delete_role
        
        with patch('app.api.routes.roles.role_service') as mock_service:
            mock_service.delete_role.return_value = True
            
            result = delete_role(role_id=1, db=mock_db)
            
            assert "exitosamente" in result["message"]
    
    def test_delete_role_validation_error(self, mock_db):
        """Debe retornar 400 si hay error de validación"""
        from app.api.routes.roles import delete_role
        
        with patch('app.api.routes.roles.role_service') as mock_service:
            mock_service.delete_role.side_effect = ValueError("No se puede eliminar")
            
            with pytest.raises(HTTPException) as exc_info:
                delete_role(role_id=1, db=mock_db)
            
            assert exc_info.value.status_code == 400


class TestGetAllPermissions:
    """Tests para GET /roles/permissions/all"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_get_all_permissions_error(self, mock_db):
        """Debe retornar 500 si hay error"""
        from app.api.routes.roles import get_all_permissions
        
        with patch('app.api.routes.roles.permission_service') as mock_service:
            mock_service.get_all_permissions.side_effect = Exception("Error")
            
            with pytest.raises(HTTPException) as exc_info:
                get_all_permissions(db=mock_db)
            
            assert exc_info.value.status_code == 500

