import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

export interface OrdersSummary {
  total_orders: number;
  by_status: { [status: string]: number };
  by_priority: { [priority: string]: number };
  by_destination?: { [city: string]: number };
  assigned?: number;
  unassigned?: number;
  total_value?: number;
}

export interface VehiclesSummary {
  total_vehicles: number;
  by_type: { [type: string]: number };
  available?: number;
  busy?: number;
  top_vehicles?: Array<{
    id: number;
    license_plate: string;
    vehicle_type: string;
    order_count: number;
  }>;
}

export interface DriversSummary {
  total_drivers: number;
  available_drivers: number;
  busy_drivers: number;
  top_drivers?: Array<{
    id: number;
    name: string;
    document_number: string;
    order_count: number;
  }>;
  drivers_without_orders?: number;
}

export interface ClientsSummary {
  total_clients: number;
  top_clients: Array<{
    id: number;
    name: string;
    company: string;
    email: string;
    order_count: number;
    total_value: number;
  }>;
  clients_without_orders?: number;
  by_company?: { [company: string]: number };
}

export interface SystemOverview {
  summary: {
    total_orders: number;
    total_vehicles: number;
    total_drivers: number;
    total_clients: number;
    pending_orders: number;
    assigned_orders?: number;
    delivered_orders?: number;
    available_vehicles?: number;
    available_drivers?: number;
    total_value?: number;
    recent_orders?: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class ReportsService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? 'http://localhost:8000/api/v1'
      : 'http://app:8000/api/v1';
  }

  getOrdersSummary(startDate?: string, endDate?: string): Observable<OrdersSummary> {
    let url = `${this.apiUrl}/reports/orders/summary`;
    const params: string[] = [];
    if (startDate) params.push(`start_date=${startDate}`);
    if (endDate) params.push(`end_date=${endDate}`);
    if (params.length > 0) url += '?' + params.join('&');
    return this.http.get<OrdersSummary>(url);
  }

  getVehiclesSummary(): Observable<VehiclesSummary> {
    return this.http.get<VehiclesSummary>(`${this.apiUrl}/reports/vehicles/summary`);
  }

  getDriversSummary(): Observable<DriversSummary> {
    return this.http.get<DriversSummary>(`${this.apiUrl}/reports/drivers/summary`);
  }

  getClientsSummary(): Observable<ClientsSummary> {
    return this.http.get<ClientsSummary>(`${this.apiUrl}/reports/clients/summary`);
  }

  getOverview(): Observable<SystemOverview> {
    return this.http.get<SystemOverview>(`${this.apiUrl}/reports/overview`);
  }
}

