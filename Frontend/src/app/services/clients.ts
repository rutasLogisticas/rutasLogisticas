import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ClientSummary {
  id: number;
  name: string;
  email: string;
  phone: string;
  company?: string | null;
  client_type: string;
  status: string;
  is_active: boolean;
}

export interface ClientCreate {
  name: string;
  email: string;
  phone: string;
  company?: string | null;
  client_type?: string;
  status?: string;
  is_active?: boolean;
}

@Injectable({ providedIn: 'root' })
export class ClientsService {
 private apiUrl = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  getClients(): Observable<ClientSummary[]> {
    return this.http.get<ClientSummary[]>(`${this.apiUrl}/clients/`);
  }

  getClientsByCompany(company: string): Observable<ClientSummary[]> {
    return this.http.get<ClientSummary[]>(`${this.apiUrl}/clients/company/${encodeURIComponent(company)}`);
  }

  getClient(id: number): Observable<ClientSummary> {
    return this.http.get<ClientSummary>(`${this.apiUrl}/clients/${id}`);
  }

  createClient(data: ClientCreate): Observable<ClientSummary> {
    return this.http.post<ClientSummary>(`${this.apiUrl}/clients/`, data);
  }
}


