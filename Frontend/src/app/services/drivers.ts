import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DriverSummary {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  document_number: string;
  license_type: string;
  status: string;
  is_available: boolean;
}

export interface DriverCreate {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  document_number: string;
  license_type: string;
  status?: string;
  is_available?: boolean;
}

@Injectable({ providedIn: 'root' })
export class DriversService {
  private apiUrl = 'http://localhost:8000/api/v1';
  
  constructor(private http: HttpClient) {}

  getDrivers(): Observable<DriverSummary[]> {
    return this.http.get<DriverSummary[]>(`${this.apiUrl}/drivers/`);
  }

  getAvailableDrivers(): Observable<DriverSummary[]> {
    return this.http.get<DriverSummary[]>(`${this.apiUrl}/drivers/available/`);
  }

  getDriver(id: number): Observable<DriverSummary> {
    return this.http.get<DriverSummary>(`${this.apiUrl}/drivers/${id}`);
  }

  createDriver(data: DriverCreate): Observable<DriverSummary> {
    return this.http.post<DriverSummary>(`${this.apiUrl}/drivers/`, data);
  }
}


