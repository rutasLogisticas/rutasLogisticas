import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api';

export interface Order {
  id: number;
  order_number: string;
  client_id: number;
  driver_id?: number;
  vehicle_id?: number;
  origin_address: string;
  destination_address: string;
  origin_city: string;
  destination_city: string;
  description: string;
  weight?: number;
  volume?: number;
  value?: number;
  status: string;
  priority: string;
  delivery_date?: string;
  delivered_date?: string;
  notes?: string;
  tracking_code?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface OrderCreate {
  client_id: number;
  driver_id?: number;
  vehicle_id?: number;
  origin_address: string;
  destination_address: string;
  origin_city: string;
  destination_city: string;
  description: string;
  weight?: number;
  volume?: number;
  value?: number;
  priority?: string;
  delivery_date?: string;
  notes?: string;
}

export interface OrderUpdate {
  driver_id?: number;
  vehicle_id?: number;
  origin_address?: string;
  destination_address?: string;
  origin_city?: string;
  destination_city?: string;
  description?: string;
  weight?: number;
  volume?: number;
  value?: number;
  priority?: string;
  delivery_date?: string;
  notes?: string;
}

export interface OrderAssignment {
  driver_id: number;
  vehicle_id: number;
  tracking_code?: string;
}

@Injectable({
  providedIn: 'root'
})
export class OrdersService {
  constructor(private apiService: ApiService) {}

  getOrders(): Observable<Order[]> {
    return this.apiService.getOrders();
  }

  getOrder(id: number): Observable<Order> {
    return this.apiService.getOrder(id);
  }

  createOrder(order: OrderCreate): Observable<Order> {
    return this.apiService.createOrder(order);
  }

  updateOrder(id: number, order: OrderUpdate): Observable<Order> {
    return this.apiService.updateOrder(id, order);
  }

  deleteOrder(id: number): Observable<void> {
    return this.apiService.deleteOrder(id);
  }

  getOrdersByClient(clientId: number): Observable<Order[]> {
    return this.apiService.getOrdersByClient(clientId);
  }

  getOrdersByDriver(driverId: number): Observable<Order[]> {
    return this.apiService.getOrdersByDriver(driverId);
  }

  getOrdersByVehicle(vehicleId: number): Observable<Order[]> {
    return this.apiService.getOrdersByVehicle(vehicleId);
  }

  getOrdersByStatus(status: string): Observable<Order[]> {
    return this.apiService.getOrdersByStatus(status);
  }

  getUnassignedOrders(): Observable<Order[]> {
    return this.apiService.getUnassignedOrders();
  }

  getOrderByTracking(trackingCode: string): Observable<Order> {
    return this.apiService.getOrderByTracking(trackingCode);
  }

  assignOrderToRoute(orderId: number, assignment: OrderAssignment): Observable<Order> {
    return this.apiService.assignOrderToRoute(orderId, assignment);
  }

  updateOrderStatus(orderId: number, status: string): Observable<Order> {
    return this.apiService.updateOrderStatus(orderId, status);
  }

  getOrderStatuses(): string[] {
    return ['pendiente', 'asignado', 'en_transito', 'entregado', 'cancelado'];
  }

  getOrderPriorities(): string[] {
    return ['baja', 'media', 'alta', 'urgente'];
  }
}
