import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

export interface AddressSummary {
  id: number;
  client_id: number;
  street: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  address_type: string;
  is_primary: boolean;
}

export interface AddressCreate {
  client_id: number;
  street: string;
  city: string;
  state: string;
  postal_code: string;
  country?: string;
  address_type?: string;
  is_primary?: boolean;
}

@Injectable({ providedIn: 'root' })
export class AddressesService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.apiUrl = isPlatformBrowser(this.platformId) 
      ? 'http://localhost:8000/api/v1'
      : 'http://app:8000/api/v1';
  }

  getAddresses(): Observable<AddressSummary[]> {
    return this.http.get<AddressSummary[]>(`${this.apiUrl}/addresses/`);
  }

  getAddress(id: number): Observable<AddressSummary> {
    return this.http.get<AddressSummary>(`${this.apiUrl}/addresses/${id}`);
  }

  getByClient(clientId: number): Observable<AddressSummary[]> {
    return this.http.get<AddressSummary[]>(`${this.apiUrl}/addresses/client/${clientId}`);
  }

  getByCity(city: string): Observable<AddressSummary[]> {
    return this.http.get<AddressSummary[]>(`${this.apiUrl}/addresses/city/${encodeURIComponent(city)}`);
  }

  createAddress(data: AddressCreate): Observable<AddressSummary> {
    return this.http.post<AddressSummary>(`${this.apiUrl}/addresses/`, data);
  }
}


