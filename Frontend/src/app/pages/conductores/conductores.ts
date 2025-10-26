import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DriversService, DriverSummary, DriverCreate, DriverUpdate } from '../../services/drivers';

@Component({
  selector: 'app-conductores',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './conductores.html',
  styleUrl: './conductores.css'
})
export class ConductoresComponent {
  drivers: DriverSummary[] = [];
  selected: DriverSummary | null = null;
  loading = false;
  error: string | null = null;
  onlyAvailable = false;
  editingDriver: DriverSummary | null = null;
  isEditing = false;

  form: DriverCreate = {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    document_number: '',
    license_type: 'B',
    status: 'disponible',
    is_available: true
  };

  constructor(private driversService: DriversService) {}

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    this.error = null;
    const source$ = this.onlyAvailable ? this.driversService.getAvailableDrivers() : this.driversService.getDrivers();
    source$.subscribe({
      next: (data: any) => {
        this.drivers = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudieron cargar los conductores';
        this.loading = false;
      }
    });
  }

  toggleAvailable() {
    this.onlyAvailable = !this.onlyAvailable;
    this.load();
  }

  select(driver: DriverSummary) {
    this.selected = driver;
  }

  submit() {
    if (!this.form.first_name || !this.form.last_name || !this.form.email || !this.form.document_number) {
      this.error = 'Completa los campos obligatorios';
      return;
    }
    this.error = null;
    this.driversService.createDriver(this.form).subscribe({
      next: (created: any) => {
        this.drivers = [created, ...this.drivers];
        this.resetForm();
      },
      error: (err: any) => {
        this.error = err?.error?.detail || 'No se pudo crear el conductor';
      }
    });
  }

  resetForm() {
    this.form = {
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      document_number: '',
      license_type: 'B',
      status: 'disponible',
      is_available: true
    };
    this.isEditing = false;
    this.editingDriver = null;
  }

  editDriver(driver: DriverSummary) {
    this.editingDriver = driver;
    this.isEditing = true;
    this.form = {
      first_name: driver.first_name,
      last_name: driver.last_name,
      email: driver.email,
      phone: driver.phone,
      document_number: driver.document_number,
      license_type: driver.license_type,
      status: driver.status,
      is_available: driver.is_available
    };
  }

  updateDriver() {
    if (!this.editingDriver || !this.form.first_name || !this.form.last_name || !this.form.email) {
      this.error = 'Completa los campos obligatorios';
      return;
    }
    
    this.error = null;
    const updateData: DriverUpdate = {
      first_name: this.form.first_name,
      last_name: this.form.last_name,
      email: this.form.email,
      phone: this.form.phone,
      license_type: this.form.license_type,
      status: this.form.status
    };

    this.driversService.updateDriver(this.editingDriver.id, updateData).subscribe({
      next: (updated: any) => {
        const index = this.drivers.findIndex(d => d.id === updated.id);
        if (index !== -1) {
          this.drivers[index] = updated;
        }
        this.resetForm();
      },
      error: (err: any) => {
        this.error = err?.error?.detail || 'No se pudo actualizar el conductor';
      }
    });
  }

  deleteDriver(driver: DriverSummary) {
    if (confirm(`¿Estás seguro de que quieres eliminar al conductor ${driver.first_name} ${driver.last_name}?`)) {
      this.driversService.deleteDriver(driver.id).subscribe({
        next: () => {
          this.drivers = this.drivers.filter(d => d.id !== driver.id);
          if (this.selected?.id === driver.id) {
            this.selected = null;
          }
        },
        error: (err: any) => {
          this.error = err?.error?.detail || 'No se pudo eliminar el conductor';
        }
      });
    }
  }
}
