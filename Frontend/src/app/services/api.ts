import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    // En el navegador usa localhost, en SSR usa el nombre del servicio Docker
    this.apiUrl = isPlatformBrowser(this.platformId) 
      ? 'http://localhost:8000/api/v1'
      : 'http://app:8000/api/v1';
  }

  // Vehículos
  getVehicles(): Observable<any> {
    return this.http.get(`${this.apiUrl}/vehicles`);
  }

  getVehicle(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/vehicles/${id}`);
  }

  createVehicle(vehicle: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/vehicles`, vehicle);
  }

  updateVehicle(id: number, vehicle: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/vehicles/${id}`, vehicle);
  }

  deleteVehicle(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/vehicles/${id}`);
  }

  // Conductores
  getDrivers(): Observable<any> {
    return this.http.get(`${this.apiUrl}/drivers`);
  }

  getDriver(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/drivers/${id}`);
  }

  createDriver(driver: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/drivers`, driver);
  }

  updateDriver(id: number, driver: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/drivers/${id}`, driver);
  }

  deleteDriver(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/drivers/${id}`);
  }

  // Clientes
  getClients(): Observable<any> {
    return this.http.get(`${this.apiUrl}/clients`);
  }

  getClient(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/clients/${id}`);
  }

  createClient(client: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/clients`, client);
  }

  updateClient(id: number, client: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/clients/${id}`, client);
  }

  deleteClient(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/clients/${id}`);
  }

  // Usuarios
  getUsers(): Observable<any> {
    return this.http.get(`${this.apiUrl}/users`);
  }

  // Pedidos
  getOrders(): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders`);
  }

  getOrder(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/${id}`);
  }

  createOrder(order: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/orders`, order);
  }

  updateOrder(id: number, order: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/orders/${id}`, order);
  }

  deleteOrder(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/orders/${id}`);
  }

  getOrdersByClient(clientId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/client/${clientId}`);
  }

  getOrdersByDriver(driverId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/driver/${driverId}`);
  }

  getOrdersByVehicle(vehicleId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/vehicle/${vehicleId}`);
  }

  getOrdersByStatus(status: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/status/${status}`);
  }

  getUnassignedOrders(): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/unassigned/list`);
  }

  getOrderByTracking(trackingCode: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/tracking/${trackingCode}`);
  }

  assignOrderToRoute(orderId: number, assignment: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/orders/${orderId}/assign`, assignment);
  }

  updateOrderStatus(orderId: number, status: string): Observable<any> {
    return this.http.patch(`${this.apiUrl}/orders/${orderId}/status?status=${status}`, {});
  }
}