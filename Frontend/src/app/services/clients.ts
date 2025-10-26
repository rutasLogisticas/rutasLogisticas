import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api';

export interface Client {
  id: number;
  name: string;
  email: string;
  phone: string;
  company?: string;
  client_type: string;
  status: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export type ClientSummary = Client;
export type ClientCreate = Partial<Client>;
export type ClientUpdate = Partial<Client>;

@Injectable({
  providedIn: 'root'
})
export class ClientsService {
  constructor(private apiService: ApiService) {}

  getClients(): Observable<Client[]> {
    return this.apiService.getClients();
  }

  getClient(id: number): Observable<Client> {
    return this.apiService.getClient(id);
  }

  createClient(client: ClientCreate): Observable<Client> {
    return this.apiService.createClient(client);
  }

  updateClient(id: number, client: ClientUpdate): Observable<Client> {
    return this.apiService.updateClient(id, client);
  }

  deleteClient(id: number): Observable<void> {
    return this.apiService.deleteClient(id);
  }

  getClientsByCompany(company: string): Observable<Client[]> {
    return this.apiService.getClients();
  }
}