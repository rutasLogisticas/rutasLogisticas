// Servicio de Auditoría del frontend
// ----------------------------------
// Intermediario entre componentes Angular y el backend de auditoría.

import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api';

// Modelo de un registro de auditoría según backend
export interface AuditLog {
  id: number;
  actor_id?: number | null;
  event_type: string;
  description: string;
  ip_address?: string | null;
  extra_data?: any;
  created_at: string; // ISO timestamp
  username?: string | null;
}

// Filtros de auditoría
export interface AuditLogFilter {
  event_type?: string;
  actor_id?: number;
  start_date?: string;
  end_date?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuditService {

  constructor(private apiService: ApiService) {}

  /**
   * Obtiene logs desde el backend usando ApiService
   */
  getLogs(filter: AuditLogFilter = {}): Observable<AuditLog[]> {
    return this.apiService.getAuditLogs(filter);
  }

  /**
   * Registrar logout de un usuario
   */
  registrarLogout(actorId: number | null) {
    return this.apiService.post('/userses/logout', {
      actor_id: actorId
    });
  }


}
