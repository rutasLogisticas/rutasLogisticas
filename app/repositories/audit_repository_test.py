"""
Tests unitarios para AuditRepository
"""
import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from sqlalchemy.orm import Session

from app.repositories.audit_repository import AuditRepository
from app.models.audit_log import AuditLog


class TestAuditRepositoryCreateLog:
    """Tests para create_log"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return AuditRepository()
    
    def test_create_log_success(self, repository, mock_db):
        """Debe crear log correctamente"""
        log_data = {
            "actor_id": 1,
            "event_type": "LOGIN",
            "description": "Usuario inició sesión",
            "ip_address": "192.168.1.1",
            "extra_data": "{}"
        }
        
        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()
        
        result = repository.create_log(mock_db, log_data)
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_create_log_without_actor(self, repository, mock_db):
        """Debe crear log sin actor (anónimo)"""
        log_data = {
            "actor_id": None,
            "event_type": "FAILED_LOGIN",
            "description": "Intento fallido",
            "ip_address": "10.0.0.1",
            "extra_data": "{}"
        }
        
        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()
        
        result = repository.create_log(mock_db, log_data)
        
        mock_db.add.assert_called_once()


class TestAuditRepositoryGetLogs:
    """Tests para get_logs"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def repository(self):
        return AuditRepository()
    
    def test_get_logs_all(self, repository, mock_db):
        """Debe obtener todos los logs"""
        mock_logs = [Mock(spec=AuditLog), Mock(spec=AuditLog)]
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = mock_logs
        
        mock_db.query.return_value = mock_query
        
        result = repository.get_logs(mock_db)
        
        assert result == mock_logs
    
    def test_get_logs_by_actor(self, repository, mock_db):
        """Debe filtrar por actor"""
        mock_logs = [Mock(spec=AuditLog, actor_id=5)]
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = mock_logs
        
        mock_db.query.return_value = mock_query
        
        result = repository.get_logs(mock_db, actor_id=5)
        
        assert result == mock_logs
    
    def test_get_logs_by_event_type(self, repository, mock_db):
        """Debe filtrar por tipo de evento"""
        mock_logs = [Mock(spec=AuditLog, event_type="LOGIN")]
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = mock_logs
        
        mock_db.query.return_value = mock_query
        
        result = repository.get_logs(mock_db, event_type="LOGIN")
        
        assert result == mock_logs
    
    def test_get_logs_by_date_range(self, repository, mock_db):
        """Debe filtrar por rango de fechas"""
        mock_logs = [Mock(spec=AuditLog)]
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = mock_logs
        
        mock_db.query.return_value = mock_query
        
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        result = repository.get_logs(
            mock_db,
            start_date=start_date,
            end_date=end_date
        )
        
        assert result == mock_logs
    
    def test_get_logs_empty(self, repository, mock_db):
        """Debe retornar lista vacía si no hay logs"""
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = []
        
        mock_db.query.return_value = mock_query
        
        result = repository.get_logs(mock_db, actor_id=999)
        
        assert result == []
    
    def test_get_logs_with_all_filters(self, repository, mock_db):
        """Debe aplicar todos los filtros"""
        mock_logs = [Mock(spec=AuditLog)]
        
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = mock_logs
        
        mock_db.query.return_value = mock_query
        
        result = repository.get_logs(
            mock_db,
            actor_id=1,
            event_type="LOGOUT",
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31)
        )
        
        assert result == mock_logs

