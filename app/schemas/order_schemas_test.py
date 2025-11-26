"""
Tests unitarios para schemas de pedidos
"""
import pytest
from pydantic import ValidationError
from decimal import Decimal
from datetime import datetime

from app.schemas.order_schemas import (
    OrderCreate, OrderUpdate, OrderResponse, OrderSummary,
    OrderAssignment, MultipleOrderRoutesRequest
)


class TestOrderCreate:
    """Tests para OrderCreate schema"""
    
    def test_create_valid_order(self):
        """Debe crear pedido con datos válidos"""
        order = OrderCreate(
            client_id=1,
            origin_address="Calle 100 #10-20, Bogotá",
            destination_address="Carrera 50 #30-40, Medellín",
            origin_city="Bogotá",
            destination_city="Medellín",
            description="Envío de documentos importantes"
        )
        assert order.client_id == 1
        assert order.priority == "media"  # default
    
    def test_create_order_with_all_fields(self):
        """Debe crear pedido con todos los campos"""
        order = OrderCreate(
            client_id=1,
            driver_id=2,
            vehicle_id=3,
            origin_address="Calle 100 #10-20, Bogotá",
            destination_address="Carrera 50 #30-40, Medellín",
            origin_city="Bogotá",
            destination_city="Medellín",
            description="Envío de documentos importantes",
            weight=10.5,
            volume=2.0,
            value=Decimal("50000"),
            priority="alta"
        )
        assert order.driver_id == 2
        assert order.vehicle_id == 3
        assert order.weight == 10.5
        assert order.priority == "alta"
    
    def test_create_order_invalid_priority(self):
        """Debe fallar con prioridad inválida"""
        with pytest.raises(ValidationError):
            OrderCreate(
                client_id=1,
                origin_address="Calle 100 #10-20, Bogotá",
                destination_address="Carrera 50 #30-40, Medellín",
                origin_city="Bogotá",
                destination_city="Medellín",
                description="Envío de documentos importantes",
                priority="invalida"
            )
    
    def test_create_order_same_addresses(self):
        """Debe fallar si origen y destino son iguales"""
        with pytest.raises(ValidationError):
            OrderCreate(
                client_id=1,
                origin_address="Calle 100 #10-20, Bogotá",
                destination_address="Calle 100 #10-20, Bogotá",
                origin_city="Bogotá",
                destination_city="Bogotá",
                description="Envío de documentos importantes"
            )
    
    def test_create_order_missing_client_id(self):
        """Debe fallar sin client_id"""
        with pytest.raises(ValidationError):
            OrderCreate(
                origin_address="Calle 100 #10-20, Bogotá",
                destination_address="Carrera 50 #30-40, Medellín",
                origin_city="Bogotá",
                destination_city="Medellín",
                description="Envío de documentos importantes"
            )
    
    def test_create_order_short_description(self):
        """Debe fallar con descripción muy corta"""
        with pytest.raises(ValidationError):
            OrderCreate(
                client_id=1,
                origin_address="Calle 100 #10-20, Bogotá",
                destination_address="Carrera 50 #30-40, Medellín",
                origin_city="Bogotá",
                destination_city="Medellín",
                description="Corto"
            )


class TestOrderUpdate:
    """Tests para OrderUpdate schema"""
    
    def test_update_all_fields_optional(self):
        """Todos los campos deben ser opcionales"""
        update = OrderUpdate()
        assert update.driver_id is None
        assert update.priority is None
    
    def test_update_partial_fields(self):
        """Debe permitir actualización parcial"""
        update = OrderUpdate(driver_id=5, vehicle_id=10)
        assert update.driver_id == 5
        assert update.vehicle_id == 10
        assert update.origin_address is None


class TestOrderSummary:
    """Tests para OrderSummary schema"""
    
    def test_summary_from_dict(self):
        """Debe crear summary desde diccionario"""
        data = {
            "id": 1,
            "order_number": "ORD-001",
            "client_id": 1,
            "driver_id": 2,
            "vehicle_id": 3,
            "origin_address": "Calle 100",
            "origin_city": "Bogotá",
            "destination_address": "Carrera 50",
            "destination_city": "Medellín",
            "status": "pendiente",
            "priority": "alta",
            "delivery_date": None,
            "delivered_date": None,
            "tracking_code": "TRK123"
        }
        summary = OrderSummary(**data)
        assert summary.id == 1
        assert summary.order_number == "ORD-001"


class TestOrderAssignment:
    """Tests para OrderAssignment schema"""
    
    def test_assignment_valid(self):
        """Debe crear asignación válida"""
        assignment = OrderAssignment(driver_id=1, vehicle_id=2)
        assert assignment.driver_id == 1
        assert assignment.vehicle_id == 2
        assert assignment.tracking_code is None
    
    def test_assignment_with_tracking(self):
        """Debe crear asignación con código de seguimiento"""
        assignment = OrderAssignment(
            driver_id=1,
            vehicle_id=2,
            tracking_code="TRK-CUSTOM-001"
        )
        assert assignment.tracking_code == "TRK-CUSTOM-001"
    
    def test_assignment_missing_driver(self):
        """Debe fallar sin driver_id"""
        with pytest.raises(ValidationError):
            OrderAssignment(vehicle_id=2)
    
    def test_assignment_missing_vehicle(self):
        """Debe fallar sin vehicle_id"""
        with pytest.raises(ValidationError):
            OrderAssignment(driver_id=1)


class TestMultipleOrderRoutesRequest:
    """Tests para MultipleOrderRoutesRequest schema"""
    
    def test_valid_request(self):
        """Debe crear request válido"""
        request = MultipleOrderRoutesRequest(order_ids=[1, 2, 3])
        assert len(request.order_ids) == 3
        assert request.mode == "driving"  # default
    
    def test_request_with_mode(self):
        """Debe crear request con modo personalizado"""
        request = MultipleOrderRoutesRequest(
            order_ids=[1, 2],
            mode="walking"
        )
        assert request.mode == "walking"

