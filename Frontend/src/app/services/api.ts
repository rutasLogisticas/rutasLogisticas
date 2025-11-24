import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http'; // ← agregamos HttpParams
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

  // Rutas de pedidos
  getOrderRoute(orderId: number, mode: string = 'driving'): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/${orderId}/route?mode=${mode}`);
  }

  getMultipleOrderRoutes(orderIds: number[], mode: string = 'driving'): Observable<any> {
    return this.http.post(`${this.apiUrl}/orders/batch-routes`, {
      order_ids: orderIds,
      mode: mode
    });
  }

  getDriverRoutes(driverId: number, mode: string = 'driving'): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/driver/${driverId}/routes?mode=${mode}`);
  }

  // MÓDULO DE AUDITORÍA

  /**
   * Obtiene los registros de auditoría desde el backend.
   *  - event_type: tipo de evento (LOGIN_SUCCESS, ORDER_CREATED, etc.)
   *  - actor_id: id del usuario responsable
   *  - start_date: fecha inicial (YYYY-MM-DD)
   *  - end_date: fecha final (YYYY-MM-DD)
   */
  getAuditLogs(params?: {
    event_type?: string;
    actor_id?: number;
    start_date?: string;
    end_date?: string;
  }): Observable<any> {
    let httpParams = new HttpParams();

    // Construimos los query params solo con los filtros que vengan definidos
    if (params) {
      if (params.event_type) {
        httpParams = httpParams.set('event_type', params.event_type);
      }
      if (params.actor_id !== undefined && params.actor_id !== null) {
        httpParams = httpParams.set('actor_id', params.actor_id.toString());
      }
      if (params.start_date) {
        httpParams = httpParams.set('start_date', params.start_date);
      }
      if (params.end_date) {
        httpParams = httpParams.set('end_date', params.end_date);
      }
    }

    // Llamamos al endpoint del backend /api/v1/audit/
    return this.http.get(`${this.apiUrl}/audit/`, { params: httpParams });
  }


  // Geocodificación
  geocodeAddress(address: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/geocoding/`, { address });
  }

  // Direcciones
  getDirections(origin: string, destination: string, mode: string = 'driving'): Observable<any> {
    return this.http.post(`${this.apiUrl}/directions/`, {
      origin,
      destination,
      mode
    });
  }

  post(endpoint: string, body: any) {
    return this.http.post(`${this.apiUrl}${endpoint}`, body);
  }

}