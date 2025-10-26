import { Component } from '@angular/core';
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
export class VehiculosComponent {
  vehicles: VehicleSummary[] = [];
  selected: VehicleSummary | null = null;
  loading = false;
  error: string | null = null;
  editingVehicle: VehicleSummary | null = null;
  isEditing = false;

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

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    this.error = null;
    this.vehiclesService.getVehicles().subscribe({
      next: (data) => {
        this.vehicles = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudieron cargar los vehículos';
        this.loading = false;
      }
    });
  }

  select(vehicle: VehicleSummary) {
    this.selected = vehicle;
  }

  submit() {
    if (!this.form.license_plate || !this.form.brand || !this.form.model) {
      this.error = 'Completa los campos obligatorios';
      return;
    }
    this.error = null;
    this.vehiclesService.createVehicle(this.form).subscribe({
      next: (created) => {
        this.vehicles = [created, ...this.vehicles];
        this.resetForm();
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo crear el vehículo';
      }
    });
  }

  resetForm() {
    this.form = {
      license_plate: '',
      brand: '',
      model: '',
      year: new Date().getFullYear(),
      vehicle_type: 'camioneta',
      status: 'disponible',
      is_available: true
    };
    this.isEditing = false;
    this.editingVehicle = null;
  }

  editVehicle(vehicle: VehicleSummary) {
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
  }

  updateVehicle() {
    if (!this.editingVehicle || !this.form.brand || !this.form.model) {
      this.error = 'Completa los campos obligatorios';
      return;
    }
    
    this.error = null;
    const updateData: VehicleUpdate = {
      brand: this.form.brand,
      model: this.form.model,
      year: this.form.year,
      vehicle_type: this.form.vehicle_type,
      status: this.form.status
    };

    this.vehiclesService.updateVehicle(this.editingVehicle.id, updateData).subscribe({
      next: (updated) => {
        const index = this.vehicles.findIndex(v => v.id === updated.id);
        if (index !== -1) {
          this.vehicles[index] = updated;
        }
        this.resetForm();
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo actualizar el vehículo';
      }
    });
  }

  deleteVehicle(vehicle: VehicleSummary) {
    if (confirm(`¿Estás seguro de que quieres eliminar el vehículo ${vehicle.license_plate}?`)) {
      this.vehiclesService.deleteVehicle(vehicle.id).subscribe({
        next: () => {
          this.vehicles = this.vehicles.filter(v => v.id !== vehicle.id);
          if (this.selected?.id === vehicle.id) {
            this.selected = null;
          }
        },
        error: (err) => {
          this.error = err?.error?.detail || 'No se pudo eliminar el vehículo';
        }
      });
    }
  }
}
