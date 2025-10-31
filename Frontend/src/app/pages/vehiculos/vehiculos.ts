import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VehiclesService, VehicleSummary, VehicleCreate, VehicleUpdate } from '../../services/vehicles';

@Component({
  selector: 'app-vehiculos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './vehiculos.html',
  styleUrls: ['./vehiculos.css']
})
export class VehiculosComponent implements OnInit {
  vehicles: VehicleSummary[] = [];
  isLoading = false;
  errorMessage: string = '';
  successMessage: string = '';
  editingVehicle: VehicleSummary | null = null;
  isEditing = false;
  showModal = false;

  form: VehicleCreate = {
    license_plate: '',
    brand: '',
    model: '',
    year: new Date().getFullYear(),
    vehicle_type: 'camioneta',
    status: 'disponible',
    is_available: true
  };

  constructor(private vehiclesService: VehiclesService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.vehiclesService.getVehicles().subscribe({
      next: (data) => {
        this.vehicles = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'No se pudieron cargar los vehículos';
        this.isLoading = false;
      }
    });
  }

  validateForm(): boolean {
    this.errorMessage = '';

    if (!this.form.license_plate || this.form.license_plate.trim().length < 3) {
      this.errorMessage = 'La placa debe tener al menos 3 caracteres';
      return false;
    }
    if (!this.form.brand || this.form.brand.trim().length < 2) {
      this.errorMessage = 'La marca debe tener al menos 2 caracteres';
      return false;
    }
    if (!this.form.model || this.form.model.trim().length < 1) {
      this.errorMessage = 'El modelo es obligatorio';
      return false;
    }
    if (!this.form.year || this.form.year < 1900 || this.form.year > 2100) {
      this.errorMessage = 'El año debe estar entre 1900 y 2100';
      return false;
    }
    return true;
  }

  submit(): void {
    if (!this.validateForm()) return;

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.vehiclesService.createVehicle(this.form).subscribe({
      next: (created) => {
        this.vehicles = [created, ...this.vehicles];
        this.resetForm();
        this.showModal = false;
        this.isLoading = false;
        this.successMessage = 'Vehículo creado exitosamente';
        setTimeout(() => (this.successMessage = ''), 3000);
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail || 'No se pudo crear el vehículo';
        this.isLoading = false;
      }
    });
  }

  showCreateForm(): void {
    this.editingVehicle = null;
    this.isEditing = false;
    this.resetForm();
    this.showModal = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  showEditForm(vehicle: VehicleSummary): void {
    this.editingVehicle = vehicle;
    this.isEditing = true;
    this.form = {
      license_plate: vehicle.license_plate,
      brand: vehicle.brand,
      model: vehicle.model,
      year: vehicle.year,
      vehicle_type: vehicle.vehicle_type,
      status: vehicle.status,
      is_available: vehicle.is_available
    };
    this.showModal = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  cancelForm(): void {
    this.showModal = false;
    this.editingVehicle = null;
    this.isEditing = false;
    this.resetForm();
    this.errorMessage = '';
    this.successMessage = '';
    this.isLoading = false;
  }

  resetForm(): void {
    this.form = {
      license_plate: '',
      brand: '',
      model: '',
      year: new Date().getFullYear(),
      vehicle_type: 'camioneta',
      status: 'disponible',
      is_available: true
    };
  }

  updateVehicle(): void {
    if (!this.editingVehicle || !this.validateForm()) return;

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const updateData: VehicleUpdate = {
      brand: this.form.brand,
      model: this.form.model,
      year: this.form.year,
      vehicle_type: this.form.vehicle_type,
      status: this.form.status
    };

    this.vehiclesService.updateVehicle(this.editingVehicle.id, updateData).subscribe({
      next: (updated) => {
        const index = this.vehicles.findIndex((v) => v.id === updated.id);
        if (index !== -1) {
          this.vehicles[index] = updated;
        }
        this.resetForm();
        this.showModal = false;
        this.isLoading = false;
        this.successMessage = 'Vehículo actualizado exitosamente';
        setTimeout(() => (this.successMessage = ''), 3000);
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail || 'No se pudo actualizar el vehículo';
        this.isLoading = false;
      }
    });
  }

  deleteVehicle(vehicle: VehicleSummary): void {
    if (confirm(`¿Estás seguro de que quieres eliminar el vehículo ${vehicle.license_plate}?`)) {
      this.vehiclesService.deleteVehicle(vehicle.id).subscribe({
        next: () => {
          this.vehicles = this.vehicles.filter((v) => v.id !== vehicle.id);
          this.successMessage = 'Vehículo eliminado exitosamente';
          setTimeout(() => (this.successMessage = ''), 3000);
        },
        error: (err) => {
          this.errorMessage = err?.error?.detail || 'No se pudo eliminar el vehículo';
        }
      });
    }
  }

  trackByVehicle(index: number, vehicle: VehicleSummary): number {
    return vehicle.id;
  }

  formatStatus(status: string): string {
    if (!status) return '';
    const spaced = status.replace(/_/g, ' ');
    return spaced
      .toLowerCase()
      .split(' ')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
}
