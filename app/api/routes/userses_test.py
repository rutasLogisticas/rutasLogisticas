"""
Tests unitarios para rutas de usuarios
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import HTTPException
from sqlalchemy.orm import Session


class TestLogin:
    """Tests para POST /userses/login"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_request(self):
        request = Mock()
        request.client.host = "127.0.0.1"
        return request
    
    def test_login_success(self, mock_db, mock_request):
        """Debe hacer login exitosamente"""
        from app.api.routes.userses import login
        from app.schemas.users_schemas import UserLogin
        
        user_data = UserLogin(username="testuser", password="TestPass123!")
        
        mock_user = Mock(
            id=1, username="testuser", 
            password_hash="hashed_password",
            role=Mock(id=1, name="admin")
        )
        
        with patch('app.api.routes.userses.service') as mock_service, \
             patch('app.api.routes.userses.verify_password') as mock_verify, \
             patch('app.api.routes.userses.create_access_token') as mock_token, \
             patch('app.api.routes.userses.audit_service'):
            
            mock_service.get_user_by_username.return_value = mock_user
            mock_verify.return_value = True
            mock_token.return_value = "test_token"
            
            result = login(user=user_data, request=mock_request, db=mock_db)
            
            assert result["access_token"] == "test_token"
            assert result["user_id"] == 1
    
    def test_login_user_not_found(self, mock_db, mock_request):
        """Debe retornar 404 si usuario no existe"""
        from app.api.routes.userses import login
        from app.schemas.users_schemas import UserLogin
        
        user_data = UserLogin(username="noexiste", password="pass")
        
        with patch('app.api.routes.userses.service') as mock_service, \
             patch('app.api.routes.userses.audit_service'):
            
            mock_service.get_user_by_username.return_value = None
            
            with pytest.raises(HTTPException) as exc_info:
                login(user=user_data, request=mock_request, db=mock_db)
            
            assert exc_info.value.status_code == 404
    
    def test_login_wrong_password(self, mock_db, mock_request):
        """Debe retornar 401 si contraseña incorrecta"""
        from app.api.routes.userses import login
        from app.schemas.users_schemas import UserLogin
        
        user_data = UserLogin(username="testuser", password="wrongpass")
        
        mock_user = Mock(id=1, username="testuser", password_hash="hash")
        
        with patch('app.api.routes.userses.service') as mock_service, \
             patch('app.api.routes.userses.verify_password') as mock_verify, \
             patch('app.api.routes.userses.audit_service'):
            
            mock_service.get_user_by_username.return_value = mock_user
            mock_verify.return_value = False
            
            with pytest.raises(HTTPException) as exc_info:
                login(user=user_data, request=mock_request, db=mock_db)
            
            assert exc_info.value.status_code == 401


class TestRegisterUser:
    """Tests para POST /userses/register"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_register_success(self, mock_db):
        """Debe registrar usuario exitosamente"""
        from app.api.routes.userses import register_user
        from app.schemas.users_schemas import UserCreate
        
        user_data = UserCreate(username="newuser", password="TestPass123!")
        
        mock_user = Mock(id=1, username="newuser", is_active=True, role_id=None)
        
        with patch('app.api.routes.userses.service') as mock_service:
            mock_service.create_user.return_value = mock_user
            
            result = register_user(user=user_data, db=mock_db)
            
            assert result.username == "newuser"
    
    def test_register_duplicate(self, mock_db):
        """Debe retornar 400 si usuario ya existe"""
        from app.api.routes.userses import register_user
        from app.schemas.users_schemas import UserCreate
        
        user_data = UserCreate(username="existente", password="TestPass123!")
        
        with patch('app.api.routes.userses.service') as mock_service:
            mock_service.create_user.side_effect = ValueError("Usuario ya existe")
            
            with pytest.raises(HTTPException) as exc_info:
                register_user(user=user_data, db=mock_db)
            
            assert exc_info.value.status_code == 400


class TestRecoveryStart:
    """Tests para POST /userses/recovery/start"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_recovery_start_success(self, mock_db):
        """Debe retornar preguntas de seguridad"""
        from app.api.routes.userses import recovery_start
        from app.schemas.users_schemas import RecoveryStartIn
        
        payload = RecoveryStartIn(username="testuser")
        
        with patch('app.api.routes.userses.service') as mock_service:
            mock_service.get_security_questions.return_value = {
                "questions": ["¿Mascota?", "¿Ciudad?"]
            }
            
            result = recovery_start(payload=payload, db=mock_db)
            
            assert result["username"] == "testuser"
            assert len(result["questions"]) == 2
    
    def test_recovery_start_user_not_found(self, mock_db):
        """Debe retornar 404 si usuario no existe"""
        from app.api.routes.userses import recovery_start
        from app.schemas.users_schemas import RecoveryStartIn
        
        payload = RecoveryStartIn(username="noexiste")
        
        with patch('app.api.routes.userses.service') as mock_service:
            mock_service.get_security_questions.return_value = None
            
            with pytest.raises(HTTPException) as exc_info:
                recovery_start(payload=payload, db=mock_db)
            
            assert exc_info.value.status_code == 404


class TestRecoveryVerify:
    """Tests para POST /userses/recovery/verify"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_recovery_verify_success(self, mock_db):
        """Debe verificar respuestas correctamente"""
        from app.api.routes.userses import recovery_verify
        from app.schemas.users_schemas import VerifyAnswersIn
        
        payload = VerifyAnswersIn(username="testuser", answers=["resp1", "resp2"])
        
        with patch('app.api.routes.userses.service') as mock_service, \
             patch('app.api.routes.userses.create_reset_token') as mock_token:
            
            mock_service.verify_security_answers.return_value = True
            mock_token.return_value = "reset_token"
            
            result = recovery_verify(payload=payload, db=mock_db)
            
            assert result["reset_token"] == "reset_token"
    
    def test_recovery_verify_wrong_answers(self, mock_db):
        """Debe retornar 401 si respuestas incorrectas"""
        from app.api.routes.userses import recovery_verify
        from app.schemas.users_schemas import VerifyAnswersIn
        
        payload = VerifyAnswersIn(username="testuser", answers=["wrong1", "wrong2"])
        
        with patch('app.api.routes.userses.service') as mock_service:
            mock_service.verify_security_answers.return_value = False
            
            with pytest.raises(HTTPException) as exc_info:
                recovery_verify(payload=payload, db=mock_db)
            
            assert exc_info.value.status_code == 401


class TestGetUser:
    """Tests para GET /userses/{user_id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_current_user(self):
        return Mock(id=1, username="admin")
    
    def test_get_user_found(self, mock_db, mock_current_user):
        """Debe retornar usuario cuando existe"""
        from app.api.routes.userses import get_user
        
        mock_user = Mock(id=2, username="testuser", is_active=True)
        
        with patch('app.api.routes.userses.service') as mock_service:
            mock_service.get_user_by_id.return_value = mock_user
            
            result = get_user(
                user_id=2,
                current_user=mock_current_user,
                db=mock_db
            )
            
            assert result.username == "testuser"
    
    def test_get_user_not_found(self, mock_db, mock_current_user):
        """Debe retornar 404 si no existe"""
        from app.api.routes.userses import get_user
        
        with patch('app.api.routes.userses.service') as mock_service:
            mock_service.get_user_by_id.return_value = None
            
            with pytest.raises(HTTPException) as exc_info:
                get_user(
                    user_id=999,
                    current_user=mock_current_user,
                    db=mock_db
                )
            
            assert exc_info.value.status_code == 404


class TestDeleteUser:
    """Tests para DELETE /userses/{user_id}"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_current_user(self):
        return Mock(id=1, username="admin")
    
    def test_delete_user_success(self, mock_db, mock_current_user):
        """Debe eliminar usuario exitosamente"""
        from app.api.routes.userses import delete_user
        
        with patch('app.api.routes.userses.service') as mock_service:
            mock_service.delete_user.return_value = True
            
            result = delete_user(
                user_id=2,
                current_user=mock_current_user,
                db=mock_db
            )
            
            assert "exitosamente" in result["message"]

