import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VehiclesService, VehicleSummary, VehicleCreate } from '../../services/vehicles';

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
  }
}
