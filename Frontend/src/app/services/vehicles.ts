import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api';

export interface Vehicle {
  id: number;
  license_plate: string;
  brand: string;
  model: string;
  year: number;
  vehicle_type: string;
  status: string;
  is_available: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export type VehicleSummary = Vehicle;
export type VehicleCreate = Partial<Vehicle>;
export type VehicleUpdate = Partial<Vehicle>;

@Injectable({
  providedIn: 'root'
})
export class VehiclesService {
  constructor(private apiService: ApiService) {}

  getVehicles(): Observable<Vehicle[]> {
    return this.apiService.getVehicles();
  }

  getVehicle(id: number): Observable<Vehicle> {
    return this.apiService.getVehicle(id);
  }

  createVehicle(vehicle: VehicleCreate): Observable<Vehicle> {
    return this.apiService.createVehicle(vehicle);
  }

  updateVehicle(id: number, vehicle: VehicleUpdate): Observable<Vehicle> {
    return this.apiService.updateVehicle(id, vehicle);
  }

  deleteVehicle(id: number): Observable<void> {
    return this.apiService.deleteVehicle(id);
  }
}