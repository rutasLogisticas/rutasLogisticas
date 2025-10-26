import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api';

export interface Driver {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  document_number: string;
  license_type: string;
  status: string;
  is_available: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export type DriverSummary = Driver;
export type DriverCreate = Partial<Driver>;
export type DriverUpdate = Partial<Driver>;

@Injectable({
  providedIn: 'root'
})
export class DriversService {
  constructor(private apiService: ApiService) {}

  getDrivers(): Observable<Driver[]> {
    return this.apiService.getDrivers();
  }

  getDriver(id: number): Observable<Driver> {
    return this.apiService.getDriver(id);
  }

  createDriver(driver: DriverCreate): Observable<Driver> {
    return this.apiService.createDriver(driver);
  }

  updateDriver(id: number, driver: DriverUpdate): Observable<Driver> {
    return this.apiService.updateDriver(id, driver);
  }

  deleteDriver(id: number): Observable<void> {
    return this.apiService.deleteDriver(id);
  }

  getAvailableDrivers(): Observable<Driver[]> {
    return this.apiService.getDrivers();
  }
}