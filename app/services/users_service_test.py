"""
Tests unitarios para UsersService
"""
import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session


class TestCreateUser:
    """Tests para create_user"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.users_service import UsersService
        service = UsersService()
        service.repository = Mock()
        return service
    
    def test_create_user_success(self, service, mock_db):
        """Debe crear usuario exitosamente"""
        user_create = Mock()
        user_create.username = "newuser"
        
        service.repository.get_user_by_username.return_value = None
        service.repository.create_user.return_value = Mock(id=1, username="newuser")
        
        result = service.create_user(mock_db, user_create)
        
        assert result.username == "newuser"
        service.repository.create_user.assert_called_once()
    
    def test_create_user_already_exists(self, service, mock_db):
        """Debe lanzar error si usuario ya existe"""
        user_create = Mock()
        user_create.username = "existinguser"
        
        service.repository.get_user_by_username.return_value = Mock(username="existinguser")
        
        with pytest.raises(ValueError) as exc_info:
            service.create_user(mock_db, user_create)
        
        assert "ya existe" in str(exc_info.value)
        service.repository.create_user.assert_not_called()


class TestLoginUser:
    """Tests para login_user"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.users_service import UsersService
        service = UsersService()
        service.repository = Mock()
        return service
    
    def test_login_user_success(self, service, mock_db):
        """Debe autenticar usuario correctamente"""
        user_login = Mock()
        user_login.username = "testuser"
        user_login.password = "correctpassword"
        
        mock_user = Mock(password_hash="hashed_password")
        service.repository.get_user_by_username.return_value = mock_user
        service.repository.verify_password.return_value = True
        
        result = service.login_user(mock_db, user_login)
        
        assert result == mock_user
    
    def test_login_user_not_found(self, service, mock_db):
        """Debe lanzar error si usuario no existe"""
        user_login = Mock()
        user_login.username = "nonexistent"
        
        service.repository.get_user_by_username.return_value = None
        
        with pytest.raises(ValueError) as exc_info:
            service.login_user(mock_db, user_login)
        
        assert "no encontrado" in str(exc_info.value)
    
    def test_login_user_wrong_password(self, service, mock_db):
        """Debe lanzar error si contraseña es incorrecta"""
        user_login = Mock()
        user_login.username = "testuser"
        user_login.password = "wrongpassword"
        
        mock_user = Mock(password_hash="hashed_password")
        service.repository.get_user_by_username.return_value = mock_user
        service.repository.verify_password.return_value = False
        
        with pytest.raises(ValueError) as exc_info:
            service.login_user(mock_db, user_login)
        
        assert "incorrecta" in str(exc_info.value)


class TestListUsers:
    """Tests para list_users"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.users_service import UsersService
        service = UsersService()
        service.repository = Mock()
        return service
    
    def test_list_users_returns_list(self, service, mock_db):
        """Debe retornar lista de usuarios"""
        mock_users = [Mock(), Mock(), Mock()]
        service.repository.get_users.return_value = mock_users
        
        result = service.list_users(mock_db)
        
        assert result == mock_users
        assert len(result) == 3


class TestGetUserByUsername:
    """Tests para get_user_by_username"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.users_service import UsersService
        service = UsersService()
        service.repository = Mock()
        return service
    
    def test_get_user_by_username_found(self, service, mock_db):
        """Debe retornar usuario cuando existe"""
        mock_user = Mock(username="testuser")
        service.repository.get_user_by_username.return_value = mock_user
        
        result = service.get_user_by_username(mock_db, "testuser")
        
        assert result == mock_user
    
    def test_get_user_by_username_not_found(self, service, mock_db):
        """Debe retornar None cuando no existe"""
        service.repository.get_user_by_username.return_value = None
        
        result = service.get_user_by_username(mock_db, "nonexistent")
        
        assert result is None


class TestUpdatePassword:
    """Tests para update_password"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.users_service import UsersService
        service = UsersService()
        service.repository = Mock()
        return service
    
    def test_update_password_success(self, service, mock_db):
        """Debe actualizar contraseña exitosamente"""
        mock_user = Mock()
        service.repository.update_password.return_value = mock_user
        
        result = service.update_password(mock_db, "testuser", "NewPass123!")
        
        assert result == mock_user
    
    def test_update_password_user_not_found(self, service, mock_db):
        """Debe lanzar error si usuario no existe"""
        service.repository.update_password.return_value = None
        
        with pytest.raises(ValueError) as exc_info:
            service.update_password(mock_db, "nonexistent", "NewPass123!")
        
        assert "no encontrado" in str(exc_info.value)


class TestDeleteUser:
    """Tests para delete_user"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.users_service import UsersService
        service = UsersService()
        service.repository = Mock()
        return service
    
    def test_delete_user_success(self, service, mock_db):
        """Debe eliminar usuario exitosamente"""
        service.repository.delete_user.return_value = True
        
        result = service.delete_user(mock_db, 1)
        
        assert result is True
    
    def test_delete_user_not_found(self, service, mock_db):
        """Debe lanzar error si usuario no existe"""
        service.repository.delete_user.return_value = None
        
        with pytest.raises(ValueError) as exc_info:
            service.delete_user(mock_db, 999)
        
        assert "no encontrado" in str(exc_info.value)


class TestGetUserById:
    """Tests para get_user_by_id"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        from app.services.users_service import UsersService
        service = UsersService()
        service.repository = Mock()
        return service
    
    def test_get_user_by_id_found(self, service, mock_db):
        """Debe retornar usuario cuando existe"""
        mock_user = Mock(id=1)
        service.repository.get_user_by_id.return_value = mock_user
        
        result = service.get_user_by_id(mock_db, 1)
        
        assert result == mock_user
    
    def test_get_user_by_id_not_found(self, service, mock_db):
        """Debe retornar None cuando no existe"""
        service.repository.get_user_by_id.return_value = None
        
        result = service.get_user_by_id(mock_db, 999)
        
        assert result is None
