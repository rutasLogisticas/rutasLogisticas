import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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

@Injectable({ providedIn: 'root' })
export class VehiclesService {
  private apiUrl = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  getVehicles(): Observable<VehicleSummary[]> {
    return this.http.get<VehicleSummary[]>(`${this.apiUrl}/vehicles/`);
  }

  getVehicle(id: number): Observable<VehicleSummary> {
    return this.http.get<VehicleSummary>(`${this.apiUrl}/vehicles/${id}`);
  }

  createVehicle(data: VehicleCreate): Observable<VehicleSummary> {
    return this.http.post<VehicleSummary>(`${this.apiUrl}/vehicles/`, data);
  }
}


