import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

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

export interface DriverUpdate {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  license_type?: string;
  status?: string;
}

@Injectable({ providedIn: 'root' })
export class DriversService {
  private apiUrl: string;
  
  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.apiUrl = isPlatformBrowser(this.platformId) 
      ? 'http://localhost:8000/api/v1'
      : 'http://app:8000/api/v1';
  }

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

  updateDriver(id: number, data: DriverUpdate): Observable<DriverSummary> {
    return this.http.put<DriverSummary>(`${this.apiUrl}/drivers/${id}`, data);
  }

  deleteDriver(id: number): Observable<{message: string}> {
    return this.http.delete<{message: string}>(`${this.apiUrl}/drivers/${id}`);
  }
}


