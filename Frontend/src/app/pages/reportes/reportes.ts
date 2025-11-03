import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportsService, OrdersSummary, VehiclesSummary, DriversSummary, ClientsSummary, SystemOverview } from '../../services/reports';
import { lastValueFrom } from 'rxjs';

@Component({
  selector: 'app-reportes',
  standalone: true,
  templateUrl: './reportes.html',
  styleUrls: ['./reportes.css'],
  imports: [CommonModule]
})
export class ReportesComponent implements OnInit {
  overview: SystemOverview | null = null;
  ordersSummary: OrdersSummary | null = null;
  vehiclesSummary: VehiclesSummary | null = null;
  driversSummary: DriversSummary | null = null;
  clientsSummary: ClientsSummary | null = null;
  
  isLoading = false;
  errorMessage = '';

  // Exponer Object para usar en el template
  Object = Object;

  constructor(private reportsService: ReportsService) {}

  ngOnInit(): void {
    this.loadAllReports();
  }

  async loadAllReports(): Promise<void> {
    this.isLoading = true;
    this.errorMessage = '';
    
    try {
      // Cargar todos los reportes en paralelo
      const [overview, orders, vehicles, drivers, clients] = await Promise.all([
        lastValueFrom(this.reportsService.getOverview()),
        lastValueFrom(this.reportsService.getOrdersSummary()),
        lastValueFrom(this.reportsService.getVehiclesSummary()),
        lastValueFrom(this.reportsService.getDriversSummary()),
        lastValueFrom(this.reportsService.getClientsSummary())
      ]);

      this.overview = overview;
      this.ordersSummary = orders;
      this.vehiclesSummary = vehicles;
      this.driversSummary = drivers;
      this.clientsSummary = clients;
      this.isLoading = false;
    } catch (error) {
      console.error('Error cargando reportes:', error);
      this.errorMessage = 'Error al cargar los reportes. Por favor, intenta nuevamente.';
      this.isLoading = false;
    }
  }

  getStatusColor(status: string): string {
    const colors: { [key: string]: string } = {
      'pendiente': '#ffc107',
      'asignado': '#17a2b8',
      'en_transito': '#007bff',
      'entregado': '#28a745',
      'cancelado': '#dc3545'
    };
    return colors[status] || '#6c757d';
  }

  getPriorityColor(priority: string): string {
    const colors: { [key: string]: string } = {
      'baja': '#28a745',
      'media': '#ffc107',
      'alta': '#fd7e14',
      'urgente': '#dc3545'
    };
    return colors[priority] || '#6c757d';
  }

  formatCurrency(value: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0
    }).format(value);
  }
}
