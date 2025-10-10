import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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
  private apiUrl = 'http://localhost:8000/api/v1'

  constructor(private http: HttpClient) {}

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


