"""
Tests unitarios para users_repository
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from sqlalchemy.orm import Session

# Note: users_repository uses functions, not a class


class TestGetUserByUsername:
    """Tests para get_user_by_username"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_get_user_by_username_found(self, mock_db):
        """Debe retornar usuario cuando existe"""
        from app.repositories.users_repository import get_user_by_username
        
        mock_user = Mock(id=1, username="testuser")
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_user
        
        mock_db.query.return_value = mock_query
        
        result = get_user_by_username(mock_db, "testuser")
        
        assert result == mock_user
    
    def test_get_user_by_username_not_found(self, mock_db):
        """Debe retornar None si no existe"""
        from app.repositories.users_repository import get_user_by_username
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        mock_db.query.return_value = mock_query
        
        result = get_user_by_username(mock_db, "noexiste")
        
        assert result is None


class TestGetUsers:
    """Tests para get_users"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_get_users_returns_list(self, mock_db):
        """Debe retornar lista de usuarios"""
        from app.repositories.users_repository import get_users
        
        mock_users = [Mock(id=1), Mock(id=2)]
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.all.return_value = mock_users
        
        mock_db.query.return_value = mock_query
        
        result = get_users(mock_db)
        
        assert result == mock_users
    
    def test_get_users_empty(self, mock_db):
        """Debe retornar lista vacía"""
        from app.repositories.users_repository import get_users
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.all.return_value = []
        
        mock_db.query.return_value = mock_query
        
        result = get_users(mock_db)
        
        assert result == []


class TestGetUserById:
    """Tests para get_user_by_id"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_get_user_by_id_found(self, mock_db):
        """Debe retornar usuario cuando existe"""
        from app.repositories.users_repository import get_user_by_id
        
        mock_user = Mock(id=1, username="testuser")
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_user
        
        mock_db.query.return_value = mock_query
        
        result = get_user_by_id(mock_db, 1)
        
        assert result == mock_user
    
    def test_get_user_by_id_not_found(self, mock_db):
        """Debe retornar None si no existe"""
        from app.repositories.users_repository import get_user_by_id
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        mock_db.query.return_value = mock_query
        
        result = get_user_by_id(mock_db, 999)
        
        assert result is None


class TestGetSecurityQuestions:
    """Tests para get_security_questions"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_get_security_questions_found(self, mock_db):
        """Debe retornar preguntas de seguridad"""
        from app.repositories.users_repository import get_security_questions
        
        mock_user = Mock(
            security_question1="¿Mascota?",
            security_question2="¿Ciudad?"
        )
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_user
        
        mock_db.query.return_value = mock_query
        
        result = get_security_questions(mock_db, "testuser")
        
        assert result is not None
        assert "questions" in result
        assert len(result["questions"]) == 2
    
    def test_get_security_questions_user_not_found(self, mock_db):
        """Debe retornar None si usuario no existe"""
        from app.repositories.users_repository import get_security_questions
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        mock_db.query.return_value = mock_query
        
        result = get_security_questions(mock_db, "noexiste")
        
        assert result is None


class TestDeleteUser:
    """Tests para delete_user"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_delete_user_success(self, mock_db):
        """Debe desactivar usuario (soft delete)"""
        from app.repositories.users_repository import delete_user
        
        mock_user = Mock(id=1, is_active=True)
        
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_user
        
        mock_db.query.return_value = mock_query
        mock_db.flush = Mock()
        mock_db.refresh = Mock()
        
        result = delete_user(mock_db, 1)
        
        assert result is not None
        assert mock_user.is_active is False
    
    def test_delete_user_not_found(self, mock_db):
        """Debe retornar None si usuario no existe"""
        from app.repositories.users_repository import delete_user
        
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        mock_db.query.return_value = mock_query
        
        result = delete_user(mock_db, 999)
        
        assert result is None

