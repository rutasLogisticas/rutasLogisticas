// Página de Auditoría
// --------------------
// Esta pantalla permite al usuario (rol auditor) consultar los eventos
// clave registrados en el backend: logins, creación de pedidos, errores, etc.

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuditService, AuditLog, AuditLogFilter } from '../../services/audit';

@Component({
  selector: 'app-auditoria',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auditoria.html',
  styleUrls: ['./auditoria.css']
})
export class AuditoriaComponent implements OnInit {

  // Lista de registros devueltos por el backend
  logs: AuditLog[] = [];

  // Estado de carga y posibles errores
  isLoading = false;
  errorMessage = '';

  // Filtros del formulario
  filter: {
    event_type: string;
    actor_id: number | null;
    start_date: string;
    end_date: string;
  } = {
    event_type: '',
    actor_id: null,
    start_date: '',
    end_date: ''
  };

  constructor(private auditService: AuditService) {}

  /**
   * Al iniciar el componente, cargamos los logs sin filtros
   * (últimos registros disponibles).
   */
  ngOnInit(): void {
    this.loadLogs();
  }

  /**
   * Construye el objeto de filtros y llama al servicio para
   * obtener la lista de auditoría.
   */
  loadLogs(): void {
    this.isLoading = true;
    this.errorMessage = '';

    const filters: AuditLogFilter = {};

    // Solo enviamos filtros que tengan valor
    if (this.filter.event_type.trim()) {
      filters.event_type = this.filter.event_type.trim();
    }
    if (this.filter.actor_id !== null && this.filter.actor_id !== undefined) {
      filters.actor_id = this.filter.actor_id;
    }
    if (this.filter.start_date) {
      filters.start_date = this.filter.start_date;
    }
    if (this.filter.end_date) {
      filters.end_date = this.filter.end_date;
    }

    this.auditService.getLogs(filters).subscribe({
      next: (logs) => {
        this.logs = logs;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error cargando logs de auditoría:', error);
        this.errorMessage = 'Ocurrió un error al cargar los registros de auditoría.';
        this.isLoading = false;
      }
    });
  }

  /**
   * Limpia todos los filtros y recarga la tabla completa.
   */
  clearFilters(): void {
    this.filter = {
      event_type: '',
      actor_id: null,
      start_date: '',
      end_date: ''
    };
    this.loadLogs();
  }

  /**
   * Devuelve un texto amigable para mostrar el nombre del usuario.
   */
  formatActorId(log: AuditLog): string {
    if (log.username) return log.username;
    if (log.actor_id) return `Usuario #${log.actor_id}`;
    return 'Sistema / Anónimo';
  }
  


}
