"""
Tests unitarios para AuditService
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.audit_service import AuditService


class TestAuditServiceRegistrarEvento:
    """Tests para registrar_evento"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        service = AuditService()
        service.repository = Mock()
        return service
    
    def test_registrar_evento_success(self, service, mock_db):
        """Debe registrar evento correctamente"""
        mock_log = Mock(id=1, event_type="LOGIN")
        service.repository.create_log.return_value = mock_log
        
        result = service.registrar_evento(
            db=mock_db,
            actor=1,
            event_type="LOGIN",
            description="Usuario inició sesión",
            ip_address="192.168.1.1",
            details={"browser": "Chrome"}
        )
        
        assert result == mock_log
        service.repository.create_log.assert_called_once()
    
    def test_registrar_evento_without_actor(self, service, mock_db):
        """Debe registrar evento sin actor (anónimo)"""
        mock_log = Mock(id=2, event_type="FAILED_LOGIN")
        service.repository.create_log.return_value = mock_log
        
        result = service.registrar_evento(
            db=mock_db,
            actor=None,
            event_type="FAILED_LOGIN",
            description="Intento de login fallido",
            ip_address="192.168.1.100",
            details=None
        )
        
        assert result == mock_log
        call_args = service.repository.create_log.call_args[0][1]
        assert call_args["actor_id"] is None
    
    def test_registrar_evento_with_details(self, service, mock_db):
        """Debe registrar evento con detalles JSON"""
        mock_log = Mock(id=3)
        service.repository.create_log.return_value = mock_log
        
        details = {"action": "create", "entity": "order", "entity_id": 123}
        
        service.registrar_evento(
            db=mock_db,
            actor=5,
            event_type="CREATE_ORDER",
            description="Pedido creado",
            ip_address="10.0.0.1",
            details=details
        )
        
        call_args = service.repository.create_log.call_args[0][1]
        assert "extra_data" in call_args
        assert "create" in call_args["extra_data"]


class TestAuditServiceBuscar:
    """Tests para buscar"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def service(self):
        service = AuditService()
        service.repository = Mock()
        return service
    
    def test_buscar_all_logs(self, service, mock_db):
        """Debe buscar todos los logs sin filtros"""
        mock_logs = [Mock(id=1), Mock(id=2), Mock(id=3)]
        service.repository.get_logs.return_value = mock_logs
        
        result = service.buscar(db=mock_db)
        
        assert result == mock_logs
        service.repository.get_logs.assert_called_once_with(
            db=mock_db,
            actor_id=None,
            event_type=None,
            start_date=None,
            end_date=None
        )
    
    def test_buscar_by_actor(self, service, mock_db):
        """Debe filtrar por actor"""
        mock_logs = [Mock(id=1, actor_id=5)]
        service.repository.get_logs.return_value = mock_logs
        
        result = service.buscar(db=mock_db, actor=5)
        
        assert result == mock_logs
        service.repository.get_logs.assert_called_once_with(
            db=mock_db,
            actor_id=5,
            event_type=None,
            start_date=None,
            end_date=None
        )
    
    def test_buscar_by_event_type(self, service, mock_db):
        """Debe filtrar por tipo de evento"""
        mock_logs = [Mock(id=1, event_type="LOGIN")]
        service.repository.get_logs.return_value = mock_logs
        
        result = service.buscar(db=mock_db, event_type="LOGIN")
        
        assert result == mock_logs
        service.repository.get_logs.assert_called_once_with(
            db=mock_db,
            actor_id=None,
            event_type="LOGIN",
            start_date=None,
            end_date=None
        )
    
    def test_buscar_by_date_range(self, service, mock_db):
        """Debe filtrar por rango de fechas"""
        mock_logs = [Mock(id=1)]
        service.repository.get_logs.return_value = mock_logs
        
        fecha_desde = datetime(2024, 1, 1)
        fecha_hasta = datetime(2024, 12, 31)
        
        result = service.buscar(
            db=mock_db,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
        
        assert result == mock_logs
        service.repository.get_logs.assert_called_once_with(
            db=mock_db,
            actor_id=None,
            event_type=None,
            start_date=fecha_desde,
            end_date=fecha_hasta
        )
    
    def test_buscar_with_all_filters(self, service, mock_db):
        """Debe aplicar todos los filtros"""
        mock_logs = [Mock(id=1)]
        service.repository.get_logs.return_value = mock_logs
        
        fecha_desde = datetime(2024, 6, 1)
        fecha_hasta = datetime(2024, 6, 30)
        
        result = service.buscar(
            db=mock_db,
            actor=10,
            event_type="LOGOUT",
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
        
        assert result == mock_logs
        service.repository.get_logs.assert_called_once_with(
            db=mock_db,
            actor_id=10,
            event_type="LOGOUT",
            start_date=fecha_desde,
            end_date=fecha_hasta
        )
    
    def test_buscar_empty_results(self, service, mock_db):
        """Debe retornar lista vacía si no hay resultados"""
        service.repository.get_logs.return_value = []
        
        result = service.buscar(db=mock_db, actor=999)
        
        assert result == []

