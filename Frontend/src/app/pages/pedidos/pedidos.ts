import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TitleCasePipe, DatePipe } from '@angular/common';
import { OrdersService, Order, OrderCreate, OrderUpdate } from '../../services/orders';
import { ClientsService } from '../../services/clients';
import { DriversService } from '../../services/drivers';
import { VehiclesService } from '../../services/vehicles';
import { ExportService } from '../../services/export.service';

@Component({
  selector: 'app-orders',
  templateUrl: './pedidos.html',
  styleUrls: ['./pedidos.css'],
  imports: [CommonModule, FormsModule, TitleCasePipe, DatePipe]
})
export class OrdersComponent implements OnInit {
  orders: Order[] = [];
  clients: any[] = [];
  drivers: any[] = [];
  vehicles: any[] = [];
  
  // Formulario
  newOrder: OrderCreate = {
    client_id: 0,
    driver_id: undefined,
    vehicle_id: undefined,
    origin_address: '',
    destination_address: '',
    origin_city: '',
    destination_city: '',
    description: '',
    weight: undefined,
    volume: undefined,
    value: undefined,
    priority: 'media',
    delivery_date: undefined,
    notes: ''
  };
  
  editingOrder: Order | null = null;
  showModal = false;
  isLoading = false;
  errorMessage = '';
  successMessage = '';
  updatingStatus: Set<number> = new Set();
  
  // Opciones
  statuses: string[] = [];
  priorities: string[] = [];
  
    constructor(
    private ordersService: OrdersService,
    private clientsService: ClientsService,
    private driversService: DriversService,
    private vehiclesService: VehiclesService,
    private cdr: ChangeDetectorRef,
    private exportService: ExportService 
  ) {
    this.statuses = this.ordersService.getOrderStatuses();
    this.priorities = this.ordersService.getOrderPriorities();
  }


  ngOnInit(): void {
    this.loadOrders();
    this.loadClients();
    this.loadDrivers();
    this.loadVehicles();
  }

  loadOrders(): void {
    this.ordersService.getOrders().subscribe({
      next: (orders) => {
        this.orders = orders;
      },
      error: (error) => {
        console.error('Error cargando pedidos:', error);
      }
    });
  }

  loadClients(): void {
    this.clientsService.getClients().subscribe({
      next: (clients) => {
        this.clients = clients;
      },
      error: (error) => {
        console.error('Error cargando clientes:', error);
      }
    });
  }

  loadDrivers(): void {
    this.driversService.getDrivers().subscribe({
      next: (drivers) => {
        this.drivers = drivers;
      },
      error: (error) => {
        console.error('Error cargando conductores:', error);
      }
    });
  }

  loadVehicles(): void {
    this.vehiclesService.getVehicles().subscribe({
      next: (vehicles) => {
        this.vehicles = vehicles;
      },
      error: (error) => {
        console.error('Error cargando vehículos:', error);
      }
    });
  }

  showCreateForm(): void {
    this.editingOrder = null;
    this.resetForm();
    this.showModal = true;
    this.errorMessage = '';
  }

  showEditForm(order: Order): void {
    this.editingOrder = order;
    this.newOrder = {
      client_id: order.client_id,
      driver_id: order.driver_id,
      vehicle_id: order.vehicle_id,
      origin_address: order.origin_address,
      destination_address: order.destination_address,
      origin_city: order.origin_city,
      destination_city: order.destination_city,
      description: order.description,
      weight: order.weight,
      volume: order.volume,
      value: order.value,
      priority: order.priority,
      delivery_date: order.delivery_date,
      notes: order.notes
    };
    this.showModal = true;
    this.errorMessage = '';
  }

  saveOrder(): void {
    // Validar datos antes de enviar
    if (!this.validateForm()) {
      return;
    }

    if (this.editingOrder) {
      this.updateOrder();
    } else {
      this.createOrder();
    }
  }

  validateForm(): boolean {
    this.errorMessage = '';

    // Validar cliente
    if (!this.newOrder.client_id || this.newOrder.client_id === 0) {
      this.errorMessage = 'Debe seleccionar un cliente';
      return false;
    }

    // Validar direcciones
    if (!this.newOrder.origin_address || this.newOrder.origin_address.trim().length < 5) {
      this.errorMessage = 'La dirección de origen debe tener al menos 5 caracteres';
      return false;
    }

    if (!this.newOrder.destination_address || this.newOrder.destination_address.trim().length < 5) {
      this.errorMessage = 'La dirección de destino debe tener al menos 5 caracteres';
      return false;
    }

    // Validar ciudades
    if (!this.newOrder.origin_city || this.newOrder.origin_city.trim().length < 2) {
      this.errorMessage = 'La ciudad de origen debe tener al menos 2 caracteres';
      return false;
    }

    if (!this.newOrder.destination_city || this.newOrder.destination_city.trim().length < 2) {
      this.errorMessage = 'La ciudad de destino debe tener al menos 2 caracteres';
      return false;
    }

    // Validar descripción
    if (!this.newOrder.description || this.newOrder.description.trim().length < 10) {
      this.errorMessage = 'La descripción debe tener al menos 10 caracteres';
      return false;
    }

    // Validar peso si se proporciona
    if (this.newOrder.weight !== undefined && this.newOrder.weight !== null) {
      if (this.newOrder.weight < 0 || this.newOrder.weight > 10000) {
        this.errorMessage = 'El peso debe estar entre 0 y 10,000 kg';
        return false;
      }
    }

    // Validar volumen si se proporciona
    if (this.newOrder.volume !== undefined && this.newOrder.volume !== null) {
      if (this.newOrder.volume < 0 || this.newOrder.volume > 1000) {
        this.errorMessage = 'El volumen debe estar entre 0 y 1,000 m³';
        return false;
      }
    }

    // Validar valor si se proporciona
    if (this.newOrder.value !== undefined && this.newOrder.value !== null) {
      if (this.newOrder.value < 0 || this.newOrder.value > 10000000) {
        this.errorMessage = 'El valor debe estar entre $0 y $10,000,000';
        return false;
      }
    }

    // Validar que origen y destino sean diferentes
    if (this.newOrder.origin_address.toLowerCase() === this.newOrder.destination_address.toLowerCase()) {
      this.errorMessage = 'La dirección de origen y destino deben ser diferentes';
      return false;
    }

    return true;
  }

  createOrder(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';
    
    this.ordersService.createOrder(this.newOrder).subscribe({
      next: (order) => {
        this.orders.push(order);
        this.resetForm();
        this.showModal = false;
        this.isLoading = false;
        this.successMessage = 'Pedido creado exitosamente';
        setTimeout(() => this.successMessage = '', 3000);
      },
      error: (error) => {
        console.error('Error creando pedido:', error);
        this.errorMessage = error.error?.detail || 'Error al crear el pedido. Verifica los datos.';
        this.isLoading = false;
      }
    });
  }

  updateOrder(): void {
    if (!this.editingOrder) return;
    
    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';
    
    const updateData: OrderUpdate = {
      driver_id: this.newOrder.driver_id,
      vehicle_id: this.newOrder.vehicle_id,
      origin_address: this.newOrder.origin_address,
      destination_address: this.newOrder.destination_address,
      origin_city: this.newOrder.origin_city,
      destination_city: this.newOrder.destination_city,
      description: this.newOrder.description,
      weight: this.newOrder.weight,
      volume: this.newOrder.volume,
      value: this.newOrder.value,
      priority: this.newOrder.priority,
      delivery_date: this.newOrder.delivery_date,
      notes: this.newOrder.notes
    };

    this.ordersService.updateOrder(this.editingOrder.id, updateData).subscribe({
      next: (updatedOrder) => {
        const index = this.orders.findIndex(o => o.id === updatedOrder.id);
        if (index !== -1) {
          this.orders[index] = updatedOrder;
        }
        this.resetForm();
        this.showModal = false;
        this.isLoading = false;
        this.successMessage = 'Pedido actualizado exitosamente';
        setTimeout(() => this.successMessage = '', 3000);
      },
      error: (error) => {
        console.error('Error actualizando pedido:', error);
        this.errorMessage = error.error?.detail || 'Error al actualizar el pedido. Verifica los datos.';
        this.isLoading = false;
      }
    });
  }

  deleteOrder(order: Order): void {
    if (confirm('¿Estás seguro de que quieres eliminar este pedido?')) {
      this.ordersService.deleteOrder(order.id).subscribe({
        next: () => {
          this.orders = this.orders.filter(o => o.id !== order.id);
        },
        error: (error) => {
          console.error('Error eliminando pedido:', error);
        }
      });
    }
  }

  onStatusChange(orderId: number, event: Event): void {
    const target = event.target as HTMLSelectElement;
    const status = target.value;
    console.log('Cambiando estado del pedido:', orderId, 'a:', status);
    
    if (!status) {
      console.log('No se seleccionó ningún estado');
      return;
    }
    
    this.updateOrderStatus(orderId, status, target);
  }

  updateOrderStatus(orderId: number, status: string, selectElement?: HTMLSelectElement): void {
    console.log('Actualizando estado del pedido:', orderId, 'a:', status);
    
    // Agregar el pedido a la lista de actualizaciones en progreso
    this.updatingStatus.add(orderId);
    
    this.ordersService.updateOrderStatus(orderId, status).subscribe({
      next: (updatedOrder) => {
        console.log('Estado actualizado exitosamente:', updatedOrder);
        
        // Opción 1: Actualizar el objeto específico
        const index = this.orders.findIndex(o => o.id === updatedOrder.id);
        if (index !== -1) {
          // Crear un nuevo objeto para forzar la detección de cambios
          this.orders[index] = { ...updatedOrder };
          console.log('Pedido actualizado en la lista:', this.orders[index]);
        }
        
        // Opción 2: Recargar toda la lista para asegurar sincronización
        setTimeout(() => {
          this.loadOrders();
        }, 100);
        
        // Remover de la lista de actualizaciones
        this.updatingStatus.delete(orderId);
        // Forzar la detección de cambios
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error actualizando estado:', error);
        // Revertir el cambio en el select
        const order = this.orders.find(o => o.id === orderId);
        if (order && selectElement) {
          selectElement.value = order.status;
        }
        // Remover de la lista de actualizaciones
        this.updatingStatus.delete(orderId);
        // Mostrar mensaje de error
        this.errorMessage = 'Error al actualizar el estado del pedido';
        setTimeout(() => this.errorMessage = '', 5000);
        // Forzar la detección de cambios
        this.cdr.detectChanges();
      }
    });
  }

  isUpdatingStatus(orderId: number): boolean {
    return this.updatingStatus.has(orderId);
  }

  getClientName(clientId: number): string {
    const client = this.clients.find(c => c.id === clientId);
    return client ? client.name : 'Cliente no encontrado';
  }

  getDriverName(driverId?: number): string {
    if (!driverId) return 'Sin asignar';
    const driver = this.drivers.find(d => d.id === driverId);
    return driver ? `${driver.first_name} ${driver.last_name}` : 'Conductor no encontrado';
  }

  getVehicleName(vehicleId?: number): string {
    if (!vehicleId) return 'Sin asignar';
    const vehicle = this.vehicles.find(v => v.id === vehicleId);
    return vehicle ? `${vehicle.brand} ${vehicle.model} (${vehicle.license_plate})` : 'Vehículo no encontrado';
  }

  getDeliveryDateInfo(order: Order): { label: string; date: string; showDate: boolean } {
    if (order.status === 'entregado' && order.delivered_date) {
      return {
        label: 'Entregado',
        date: order.delivered_date,
        showDate: true
      };
    } else if (order.delivery_date) {
      return {
        label: 'Programado',
        date: order.delivery_date,
        showDate: true
      };
    } else {
      return {
        label: 'Sin fecha programada',
        date: '',
        showDate: false
      };
    }
  }

  resetForm(): void {
    this.newOrder = {
      client_id: 0,
      driver_id: undefined,
      vehicle_id: undefined,
      origin_address: '',
      destination_address: '',
      origin_city: '',
      destination_city: '',
      description: '',
      weight: undefined,
      volume: undefined,
      value: undefined,
      priority: 'media',
      delivery_date: undefined,
      notes: ''
    };
  }

  cancelForm(): void {
    this.showModal = false;
    this.editingOrder = null;
    this.resetForm();
    this.errorMessage = '';
    this.successMessage = '';
    this.isLoading = false;
  }
    exportOrdersCSV(): void {
    if (!this.orders || this.orders.length === 0) {
      console.warn('No hay pedidos para exportar');
      return;
    }

    const headers = [
      'Número',
      'Cliente',
      'Origen',
      'Destino',
      'Conductor',
      'Vehículo',
      'Estado',
      'Prioridad',
      'Fecha Entrega'
    ];

    const rows = this.orders.map((order) => {
      const cliente = this.getClientName(order.client_id);
      const conductor = this.getDriverName(order.driver_id);
      const vehiculo = this.getVehicleName(order.vehicle_id);
      const origen = `${order.origin_city} - ${order.origin_address}`;
      const destino = `${order.destination_city} - ${order.destination_address}`;
      const fechaEntrega = order.delivery_date || '';

      return [
        order.order_number,
        cliente,
        origen,
        destino,
        conductor,
        vehiculo,
        order.status,
        order.priority,
        fechaEntrega
      ];
    });

    this.exportService.downloadCSV('pedidos', headers, rows);
  }

  exportOrdersExcel(): void {
    if (!this.orders || this.orders.length === 0) {
      console.warn('No hay pedidos para exportar');
      return;
    }

    const headers = [
      'Número',
      'Cliente',
      'Origen',
      'Destino',
      'Conductor',
      'Vehículo',
      'Estado',
      'Prioridad',
      'Fecha Entrega'
    ];

    const rows = this.orders.map((order) => {
      const cliente = this.getClientName(order.client_id);
      const conductor = this.getDriverName(order.driver_id);
      const vehiculo = this.getVehicleName(order.vehicle_id);
      const origen = `${order.origin_city} - ${order.origin_address}`;
      const destino = `${order.destination_city} - ${order.destination_address}`;
      const fechaEntrega = order.delivery_date || '';

      return [
        order.order_number,
        cliente,
        origen,
        destino,
        conductor,
        vehiculo,
        order.status,
        order.priority,
        fechaEntrega
      ];
    });

    this.exportService.downloadExcel('pedidos', headers, rows);
  }

  exportOrdersPDF(): void {
    if (!this.orders || this.orders.length === 0) {
      console.warn('No hay pedidos para exportar');
      return;
    }

    const headers = [
      'Número',
      'Cliente',
      'Origen',
      'Destino',
      'Conductor',
      'Vehículo',
      'Estado',
      'Prioridad',
      'Fecha Entrega'
    ];

    const rows = this.orders.map((order) => {
      const cliente = this.getClientName(order.client_id);
      const conductor = this.getDriverName(order.driver_id);
      const vehiculo = this.getVehicleName(order.vehicle_id);
      const origen = `${order.origin_city} - ${order.origin_address}`;
      const destino = `${order.destination_city} - ${order.destination_address}`;
      const fechaEntrega = order.delivery_date || '';

      return [
        order.order_number,
        cliente,
        origen,
        destino,
        conductor,
        vehiculo,
        order.status,
        order.priority,
        fechaEntrega
      ];
    });

    this.exportService.downloadPdf('pedidos', 'Reporte de Pedidos', headers, rows);
  }

}
