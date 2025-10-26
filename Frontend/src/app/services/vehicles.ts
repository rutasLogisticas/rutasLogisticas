import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

export interface VehicleSummary {
  id: number;
  license_plate: string;
  brand: string;
  model: string;
  year: number;
  vehicle_type: string;
  status: string;
  is_available: boolean;
}

export interface VehicleCreate {
  license_plate: string;
  brand: string;
  model: string;
  year: number;
  vehicle_type: string;
  status?: string;
  is_available?: boolean;
}

export interface VehicleUpdate {
  brand?: string;
  model?: string;
  year?: number;
  vehicle_type?: string;
  status?: string;
}

@Injectable({ providedIn: 'root' })
export class VehiclesService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.apiUrl = isPlatformBrowser(this.platformId) 
      ? 'http://localhost:8000/api/v1'
      : 'http://app:8000/api/v1';
  }

  getVehicles(): Observable<VehicleSummary[]> {
    return this.http.get<VehicleSummary[]>(`${this.apiUrl}/vehicles/`);
  }

  getVehicle(id: number): Observable<VehicleSummary> {
    return this.http.get<VehicleSummary>(`${this.apiUrl}/vehicles/${id}`);
  }

  createVehicle(data: VehicleCreate): Observable<VehicleSummary> {
    return this.http.post<VehicleSummary>(`${this.apiUrl}/vehicles/`, data);
  }

  updateVehicle(id: number, data: VehicleUpdate): Observable<VehicleSummary> {
    return this.http.put<VehicleSummary>(`${this.apiUrl}/vehicles/${id}`, data);
  }

  deleteVehicle(id: number): Observable<{message: string}> {
    return this.http.delete<{message: string}>(`${this.apiUrl}/vehicles/${id}`);
  }
}


