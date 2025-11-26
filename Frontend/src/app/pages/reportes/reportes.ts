import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule, HttpParams } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  selector: 'app-reportes',
  standalone: true, 
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './reportes.html',
  styleUrls: ['./reportes.css']
})
export class ReportesComponent {
  tipoReporte: string = '';
  datosReporte: any[] = [];
  tituloReporte: string = '';
  loading = false;
  error: string | null = null;

  filtros: any = {
    fechaInicio: '',
    fechaFin: '',
    estado: '',
    estadoPedido: '',
    tipoVehiculo: '',
    disponibilidad: '',
    clienteId: '',
    conductorId: '',
    nombreConductor: '',
    tipoLicencia: '',
    estadoConductor: '',
    ciudadOrigen: '',
    ciudadDestino: '',
    nombreCliente: '',
    tipoCliente: ''
  };

  estadisticasResumen: any[] = [];

  // Gráficos para pedidos
  graficoEstados: any = null;
  graficoCiudades: any = null;

  // Gráficos para clientes
  graficoTipoCliente: any = null;
  graficoEstadoCliente: any = null;

  // Gráficos para vehículos
  
  private apiUrl = 'http://localhost:8000/api/v1';


  constructor(private http: HttpClient) {}

  seleccionarReporte(tipo: string) {
    this.tipoReporte = tipo;
    this.datosReporte = [];
    this.error = null;
    this.estadisticasResumen = [];
    this.tituloReporte = `Reporte de ${tipo.charAt(0).toUpperCase() + tipo.slice(1)}`;
  }
  generarReporte() {
    this.error = null;
    this.loading = true;
    let url = '';
    let params = new HttpParams();

    // PEDIDOS
    if (this.tipoReporte === 'pedidos') {
      if (this.filtros.fechaInicio && this.filtros.fechaFin) {
        url = `${this.apiUrl}/reports/orders-by-date`;
        params = params
          .set('start_date', this.filtros.fechaInicio)
          .set('end_date', this.filtros.fechaFin);
      } else if (this.filtros.clienteId) {
        url = `${this.apiUrl}/reports/orders-by-client/${this.filtros.clienteId}`;
      } else {
        url = `${this.apiUrl}/orders`;
      }
    } 
    // CLIENTES
    else if (this.tipoReporte === 'clientes') {
      url = `${this.apiUrl}/clients`;
    } 
    // VEHÍCULOS
    else if (this.tipoReporte === 'vehiculos') {
      url = `${this.apiUrl}/vehicles`;
    } 
    // CONDUCTORES
    else if (this.tipoReporte === 'conductores') {
      url = `${this.apiUrl}/drivers`;
    }

    console.log('🔍 Consultando URL:', url);

    this.http.get<any[]>(url, { params })
      .pipe(
        catchError(err => {
          console.error('❌ Error completo:', err);
          console.error('📍 URL solicitada:', url);
          console.error('📍 Status:', err.status);
          
          let mensajeError = 'Error al generar el reporte.';
          
          if (err.status === 0) {
            mensajeError = '🔴 No se puede conectar al servidor. Verifica que esté corriendo en http://localhost:8000';
          } else if (err.status === 404) {
            mensajeError = 'Endpoint no encontrado. Verifica la configuración del backend.';
          } else if (err.status === 500) {
            mensajeError = 'Error interno del servidor: ' + (err.error?.detail || 'Error desconocido');
          } else {
            mensajeError = err.error?.detail || err.message || mensajeError;
          }
          
          this.error = mensajeError;
          this.loading = false;
          return of([]);
        })
      )
      .subscribe((data) => {
        this.loading = false;
        console.log('✅ Datos recibidos:', data);
        console.log('📊 Total registros:', data?.length || 0);
        
        let datosFiltrados = data || [];
        
        // Filtrar por nombre de cliente
        if (this.tipoReporte === 'clientes' && this.filtros.nombreCliente?.trim()) {
          const nombre = this.filtros.nombreCliente.toLowerCase();
          datosFiltrados = datosFiltrados.filter(item => 
            item.name?.toLowerCase().includes(nombre) ||
            item.company?.toLowerCase().includes(nombre)
          );
        }

        // Filtrar por tipo de cliente
        if (this.tipoReporte === 'clientes' && this.filtros.tipoCliente) {
          datosFiltrados = datosFiltrados.filter(item => 
            item.client_type?.toLowerCase() === this.filtros.tipoCliente.toLowerCase()
          );
        }
        
        // Filtrar por estado de pedido (mapeo de estados en español/inglés)
        if (this.tipoReporte === 'pedidos' && this.filtros.estadoPedido) {
          const estadoMap: any = {
            'en_proceso': ['en_proceso', 'asignado', 'in_transit'],
            'pendiente': ['pendiente', 'pending'],
            'completado': ['completado', 'entregado', 'delivered'],
            'cancelado': ['cancelado', 'cancelled']
          };
          
          const estadosBuscar = estadoMap[this.filtros.estadoPedido.toLowerCase()] || [this.filtros.estadoPedido.toLowerCase()];
          
          datosFiltrados = datosFiltrados.filter(item => 
            estadosBuscar.includes(item.status?.toLowerCase())
          );
        }

        // Filtrar por ciudad origen
        if (this.tipoReporte === 'pedidos' && this.filtros.ciudadOrigen?.trim()) {
          const ciudad = this.filtros.ciudadOrigen.toLowerCase();
          datosFiltrados = datosFiltrados.filter(item => 
            item.origin_city?.toLowerCase().includes(ciudad)
          );
        }

        // Filtrar por ciudad destino
        if (this.tipoReporte === 'pedidos' && this.filtros.ciudadDestino?.trim()) {
          const ciudad = this.filtros.ciudadDestino.toLowerCase();
          datosFiltrados = datosFiltrados.filter(item => 
            item.destination_city?.toLowerCase().includes(ciudad)
          );
        }
        
        // Filtrar por tipo de vehículo
        if (this.tipoReporte === 'vehiculos' && this.filtros.tipoVehiculo) {
          datosFiltrados = datosFiltrados.filter(item => 
            item.vehicle_type?.toLowerCase() === this.filtros.tipoVehiculo.toLowerCase()
          );
        }

        // Filtrar por disponibilidad de vehículos
        if (this.tipoReporte === 'vehiculos' && this.filtros.disponibilidad) {
          const isAvailable = this.filtros.disponibilidad === 'disponible';
          datosFiltrados = datosFiltrados.filter(item => 
            item.is_available === isAvailable
          );
        }

        // Filtrar conductores
        if (this.tipoReporte === 'conductores') {
          // Filtrar por nombre
          if (this.filtros.nombreConductor?.trim()) {
            const nombre = this.filtros.nombreConductor.toLowerCase();
            datosFiltrados = datosFiltrados.filter(item => {
              const fullName = `${item.first_name || ''} ${item.last_name || ''}`.toLowerCase();
              return fullName.includes(nombre) || 
                     item.first_name?.toLowerCase().includes(nombre) ||
                     item.last_name?.toLowerCase().includes(nombre);
            });
          }

          // Filtrar por tipo de licencia
          if (this.filtros.tipoLicencia) {
            datosFiltrados = datosFiltrados.filter(item => 
              item.license_type?.toUpperCase() === this.filtros.tipoLicencia.toUpperCase()
            );
          }

          // Filtrar por estado
          if (this.filtros.estadoConductor) {
            datosFiltrados = datosFiltrados.filter(item => 
              item.status?.toLowerCase() === this.filtros.estadoConductor.toLowerCase()
            );
          }
        }
        
        this.datosReporte = datosFiltrados;
        this.calcularEstadisticas();
        
        if (this.datosReporte.length === 0 && data.length > 0) {
          this.error = 'No hay resultados con los filtros aplicados';
          setTimeout(() => this.error = null, 3000);
        }
      });
  }

  limpiarFiltros() {
    this.filtros = {
      fechaInicio: '',
      fechaFin: '',
      estado: '',
      estadoPedido: '',
      tipoVehiculo: '',
      clienteId: '',
      conductorId: ''
    };
    this.datosReporte = [];
    this.estadisticasResumen = [];
  }

  calcularEstadisticas() {
    if (this.tipoReporte === 'pedidos') {
      const total = this.datosReporte.length;
      const completados = this.datosReporte.filter(p => 
        ['completado', 'entregado', 'delivered'].includes(p.status?.toLowerCase())
      ).length;
      const pendientes = this.datosReporte.filter(p => 
        ['pendiente', 'pending'].includes(p.status?.toLowerCase())
      ).length;
      const enProceso = this.datosReporte.filter(p => 
        ['asignado', 'en_proceso', 'in_transit'].includes(p.status?.toLowerCase())
      ).length;
      
      this.estadisticasResumen = [
        { label: 'Total', value: total },
        { label: 'Completados', value: completados },
        { label: 'En Proceso', value: enProceso },
        { label: 'Pendientes', value: pendientes }
      ];
    } else if (this.tipoReporte === 'clientes') {
      const total = this.datosReporte.length;
      const activos = this.datosReporte.filter(c => 
        c.status?.toLowerCase() === 'activo'
      ).length;
      
      this.estadisticasResumen = [
        { label: 'Total', value: total },
        { label: 'Activos', value: activos },
        { label: 'Inactivos', value: total - activos }
      ];
    } else if (this.tipoReporte === 'vehiculos') {
      const total = this.datosReporte.length;
      const disponibles = this.datosReporte.filter(v => 
        v.status?.toLowerCase() === 'disponible'
      ).length;
      
      this.estadisticasResumen = [
        { label: 'Total', value: total },
        { label: 'Disponibles', value: disponibles },
        { label: 'No Disponibles', value: total - disponibles }
      ];
    } else if (this.tipoReporte === 'conductores') {
      const total = this.datosReporte.length;
      
      this.estadisticasResumen = [
        { label: 'Rutas Completadas', value: total }
      ];
    }

    // Generar gráficos según el tipo de reporte
    if (this.tipoReporte === 'pedidos') {
      this.generarGraficosPedidos();
    } else if (this.tipoReporte === 'clientes') {
      this.generarGraficosClientes();
    } else {
      this.graficoEstados = null;
      this.graficoCiudades = null;
      this.graficoTipoCliente = null;
      this.graficoEstadoCliente = null;
    }
  }

  generarGraficosPedidos() {
    // Gráfico de estados
    const estadosMap = new Map<string, number>();
    this.datosReporte.forEach(pedido => {
      const estado = pedido.status?.toLowerCase() || 'desconocido';
      const estadoNormalizado = this.normalizarEstado(estado);
      estadosMap.set(estadoNormalizado, (estadosMap.get(estadoNormalizado) || 0) + 1);
    });

    const coloresEstados: any = {
      'pendiente': '#FFC107',
      'en proceso': '#2196F3',
      'completado': '#4CAF50',
      'cancelado': '#F44336'
    };

    const total = this.datosReporte.length;
    this.graficoEstados = Array.from(estadosMap.entries()).map(([estado, count]) => ({
      label: estado.charAt(0).toUpperCase() + estado.slice(1),
      count: count,
      porcentaje: total > 0 ? (count / total) * 100 : 0,
      color: coloresEstados[estado] || '#9C27B0'
    }));

    // Gráfico de ciudades destino
    const ciudadesMap = new Map<string, number>();
    this.datosReporte.forEach(pedido => {
      const ciudad = pedido.destination_city || 'desconocida';
      ciudadesMap.set(ciudad, (ciudadesMap.get(ciudad) || 0) + 1);
    });

    // Limitar a top 10 ciudades
    const ciudadesOrdenadas = Array.from(ciudadesMap.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);

    const coloresGradiente = [
      '#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#fee140', '#30cfd0', '#330867'
    ];

    const totalCiudades = this.datosReporte.length;
    this.graficoCiudades = ciudadesOrdenadas.map(([ciudad, count], index) => ({
      label: ciudad,
      count: count,
      porcentaje: totalCiudades > 0 ? (count / totalCiudades) * 100 : 0,
      color: coloresGradiente[index % coloresGradiente.length]
    }));
  }

  normalizarEstado(estado: string): string {
    if (['completado', 'entregado', 'delivered'].includes(estado)) return 'completado';
    if (['pendiente', 'pending'].includes(estado)) return 'pendiente';
    if (['asignado', 'en_proceso', 'in_transit'].includes(estado)) return 'en proceso';
    if (['cancelado', 'cancelled'].includes(estado)) return 'cancelado';
    return estado;
  }

  generarGraficosClientes() {
    // Gráfico de tipo de cliente
    const tipoMap = new Map<string, number>();
    this.datosReporte.forEach(cliente => {
      const tipo = cliente.client_type || 'desconocido';
      tipoMap.set(tipo, (tipoMap.get(tipo) || 0) + 1);
    });

    const coloresTipo: any = {
      'persona': '#667eea',
      'empresa': '#764ba2',
      'otro': '#f093fb'
    };

    const totalClientes = this.datosReporte.length;
    this.graficoTipoCliente = Array.from(tipoMap.entries()).map(([tipo, count]) => ({
      label: tipo.charAt(0).toUpperCase() + tipo.slice(1),
      count: count,
      porcentaje: totalClientes > 0 ? (count / totalClientes) * 100 : 0,
      color: coloresTipo[tipo.toLowerCase()] || '#9C27B0'
    }));

    // Gráfico de estado de cliente
    const estadoMap = new Map<string, number>();
    this.datosReporte.forEach(cliente => {
      const estado = cliente.status?.toLowerCase() || 'desconocido';
      estadoMap.set(estado, (estadoMap.get(estado) || 0) + 1);
    });

    const coloresEstado: any = {
      'activo': '#4CAF50',
      'inactivo': '#9E9E9E',
      'suspendido': '#F44336'
    };

    this.graficoEstadoCliente = Array.from(estadoMap.entries()).map(([estado, count]) => ({
      label: estado.charAt(0).toUpperCase() + estado.slice(1),
      count: count,
      porcentaje: totalClientes > 0 ? (count / totalClientes) * 100 : 0,
      color: coloresEstado[estado.toLowerCase()] || '#FF9800'
    }));
  }
  

  // Métodos para la tabla
  getColumnKeys(): string[] {
    if (!this.datosReporte || this.datosReporte.length === 0) return [];
    const allKeys = Object.keys(this.datosReporte[0]);
    // Filtrar las columnas que no queremos mostrar
    const excludedColumns = ['is_active', 'isActive', 'is Active', 'is_available', 'isAvailable', 'is Available'];
    return allKeys.filter(key => !excludedColumns.includes(key));
  }

  formatColumnName(key: string): string {
    const translations: any = {
      'id': 'ID',
      'name': 'Nombre',
      'first_name': 'Nombre',
      'last_name': 'Apellido',
      'email': 'Email',
      'phone': 'Teléfono',
      'company': 'Empresa',
      'client_type': 'Tipo Cliente',
      'status': 'Estado',
      'order_number': 'N° Orden',
      'client_id': 'Cliente',
      'driver_id': 'Conductor',
      'vehicle_id': 'Vehículo',
      'origin_address': 'Origen',
      'destination_address': 'Destino',
      'origin_city': 'Ciudad Origen',
      'destination_city': 'Ciudad Destino',
      'priority': 'Prioridad',
      'value': 'Valor',
      'tracking_code': 'Código Rastreo',
      'license_plate': 'Placa',
      'brand': 'Marca',
      'model': 'Modelo',
      'year': 'Año',
      'vehicle_type': 'Tipo Vehículo',
      'document_number': 'Documento',
      'license_type': 'Tipo Licencia',
      'created_at': 'Fecha Creación',
      'updated_at': 'Última Actualización'
    };
    
    return translations[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }

  getColumnValue(item: any, key: string): any {
    const value = item[key];
    if (value === null || value === undefined) return '-';
    
    // Formatear fechas
    if (key.includes('date') || key.includes('_at')) {
      try {
        return new Date(value).toLocaleString('es-CO', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch {
        return value;
      }
    }
    
    // Formatear estados
    if (key === 'status') {
      const statusMap: any = {
        'pendiente': 'Pendiente',
        'asignado': 'Asignado',
        'entregado': 'Entregado',
        'cancelado': 'Cancelado',
        'activo': 'Activo',
        'inactivo': 'Inactivo',
        'disponible': 'Disponible'
      };
      return statusMap[value?.toLowerCase()] || value;
    }
    
    // Formatear prioridad
    if (key === 'priority') {
      const priorityMap: any = {
        'alta': 'Alta',
        'media': 'Media',
        'baja': 'Baja'
      };
      return priorityMap[value?.toLowerCase()] || value;
    }
    
    // Formatear valores monetarios
    if (key === 'value' && typeof value === 'number') {
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP'
      }).format(value);
    }
    
    if (typeof value === 'object') return JSON.stringify(value);
    return value;
  }

  // Exportar a CSV
  exportarExcel() {
    if (this.datosReporte.length === 0) {
      this.error = 'No hay datos para exportar';
      setTimeout(() => this.error = null, 3000);
      return;
    }

    try {
      const headers = this.getColumnKeys();
      const csvContent = [
        headers.map(h => this.formatColumnName(h)).join(','),
        ...this.datosReporte.map(row => 
          headers.map(h => {
            const val = this.getColumnValue(row, h);
            const strVal = String(val);
            return strVal.includes(',') ? `"${strVal}"` : strVal;
          }).join(',')
        )
      ].join('\n');

      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', `${this.tituloReporte}_${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error al exportar CSV:', error);
      this.error = 'Error al exportar CSV';
      setTimeout(() => this.error = null, 3000);
    }
  }

  // Exportar a PDF
  exportarPDF() {
    if (this.datosReporte.length === 0) {
      this.error = 'No hay datos para exportar';
      setTimeout(() => this.error = null, 3000);
      return;
    }

    try {
      const headers = this.getColumnKeys().map(k => this.formatColumnName(k));
      
      let html = `
        <!DOCTYPE html>
        <html>
        <head>
          <title>${this.tituloReporte}</title>
          <meta charset="UTF-8">
          <style>
            body { 
              font-family: Arial, sans-serif; 
              padding: 20px;
              max-width: 1200px;
              margin: 0 auto;
            }
            h1 { 
              color: #ff7a00; 
              margin-bottom: 10px;
              font-size: 24px;
            }
            .fecha {
              color: #666;
              margin-bottom: 20px;
              font-size: 14px;
            }
            table { 
              width: 100%; 
              border-collapse: collapse; 
              margin-top: 20px;
              font-size: 11px;
            }
            th { 
              background: #ff7a00; 
              color: white; 
              padding: 10px 6px; 
              text-align: left;
              font-weight: 600;
            }
            td { 
              padding: 8px 6px; 
              border-bottom: 1px solid #ddd;
            }
            tr:nth-child(even) {
              background: #f9f9f9;
            }
            .print-button {
              background: #ff7a00;
              color: white;
              padding: 10px 20px;
              border: none;
              border-radius: 5px;
              cursor: pointer;
              margin-bottom: 20px;
              font-size: 14px;
            }
            .print-button:hover {
              background: #e66900;
            }
            @media print {
              .print-button { 
                display: none; 
              }
              body {
                padding: 0;
              }
            }
          </style>
        </head>
        <body>
          <button class="print-button" onclick="window.print()">🖨️ Imprimir PDF</button>
          <h1>${this.tituloReporte}</h1>
          <div class="fecha">Generado: ${new Date().toLocaleString('es-CO')}</div>
          <table>
            <thead>
              <tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>
            </thead>
            <tbody>
              ${this.datosReporte.map(row => `
                <tr>${this.getColumnKeys().map(k => `<td>${this.getColumnValue(row, k)}</td>`).join('')}</tr>
              `).join('')}
            </tbody>
          </table>
        </body>
        </html>
      `;

      const printWindow = window.open('', '_blank');
      if (printWindow) {
        printWindow.document.write(html);
        printWindow.document.close();
      } else {
        this.error = 'Por favor permite ventanas emergentes para exportar PDF';
        setTimeout(() => this.error = null, 3000);
      }
    } catch (error) {
      console.error('Error al exportar PDF:', error);
      this.error = 'Error al generar vista de impresión';
      setTimeout(() => this.error = null, 3000);
    }
  }

  imprimirReporte() {
    window.print();
  }
}
