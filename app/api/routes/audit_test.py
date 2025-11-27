"""
Tests unitarios para rutas de auditoría
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from sqlalchemy.orm import Session


class TestGetLogs:
    """Tests para GET /audit"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    def test_get_logs_success(self, mock_db):
        """Debe retornar lista de logs"""
        from app.api.routes.audit import get_logs
        
        # Crear mock de logs con actor
        mock_actor = Mock()
        mock_actor.username = "testuser"
        
        mock_log1 = Mock(
            id=1,
            created_at=datetime(2024, 1, 1),
            event_type="LOGIN",
            description="Usuario inició sesión",
            ip_address="192.168.1.1",
            actor_id=1,
            actor=mock_actor
        )
        mock_log2 = Mock(
            id=2,
            created_at=datetime(2024, 1, 2),
            event_type="LOGOUT",
            description="Usuario cerró sesión",
            ip_address="192.168.1.1",
            actor_id=1,
            actor=mock_actor
        )
        
        with patch('app.api.routes.audit.audit_service') as mock_service:
            mock_service.buscar.return_value = [mock_log1, mock_log2]
            
            result = get_logs(db=mock_db)
            
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[0]["event_type"] == "LOGIN"
            assert result[0]["username"] == "testuser"
    
    def test_get_logs_empty(self, mock_db):
        """Debe retornar lista vacía"""
        from app.api.routes.audit import get_logs
        
        with patch('app.api.routes.audit.audit_service') as mock_service:
            mock_service.buscar.return_value = []
            
            result = get_logs(db=mock_db)
            
            assert result == []
    
    def test_get_logs_with_actor_filter(self, mock_db):
        """Debe filtrar por actor"""
        from app.api.routes.audit import get_logs
        
        mock_actor = Mock()
        mock_actor.username = "admin"
        
        mock_log = Mock(
            id=1,
            created_at=datetime(2024, 1, 1),
            event_type="CREATE_USER",
            description="Usuario creado",
            ip_address="10.0.0.1",
            actor_id=5,
            actor=mock_actor
        )
        
        with patch('app.api.routes.audit.audit_service') as mock_service:
            mock_service.buscar.return_value = [mock_log]
            
            result = get_logs(db=mock_db, actor_id=5)
            
            mock_service.buscar.assert_called_once()
            call_kwargs = mock_service.buscar.call_args[1]
            assert call_kwargs["actor"] == 5
    
    def test_get_logs_with_event_type_filter(self, mock_db):
        """Debe filtrar por tipo de evento"""
        from app.api.routes.audit import get_logs
        
        with patch('app.api.routes.audit.audit_service') as mock_service:
            mock_service.buscar.return_value = []
            
            get_logs(db=mock_db, event_type="LOGIN")
            
            call_kwargs = mock_service.buscar.call_args[1]
            assert call_kwargs["event_type"] == "LOGIN"
    
    def test_get_logs_with_date_filters(self, mock_db):
        """Debe filtrar por rango de fechas"""
        from app.api.routes.audit import get_logs
        
        date_from = datetime(2024, 1, 1)
        date_to = datetime(2024, 12, 31)
        
        with patch('app.api.routes.audit.audit_service') as mock_service:
            mock_service.buscar.return_value = []
            
            get_logs(db=mock_db, date_from=date_from, date_to=date_to)
            
            call_kwargs = mock_service.buscar.call_args[1]
            assert call_kwargs["fecha_desde"] == date_from
            assert call_kwargs["fecha_hasta"] == date_to
    
    def test_get_logs_without_actor(self, mock_db):
        """Debe manejar logs sin actor (anónimos)"""
        from app.api.routes.audit import get_logs
        
        mock_log = Mock(
            id=1,
            created_at=datetime(2024, 1, 1),
            event_type="FAILED_LOGIN",
            description="Intento fallido",
            ip_address="192.168.1.100",
            actor_id=None,
            actor=None
        )
        
        with patch('app.api.routes.audit.audit_service') as mock_service:
            mock_service.buscar.return_value = [mock_log]
            
            result = get_logs(db=mock_db)
            
            assert result[0]["actor_id"] is None
            assert result[0]["username"] is None

