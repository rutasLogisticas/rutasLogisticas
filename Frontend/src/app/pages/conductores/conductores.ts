import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DriversService, DriverSummary, DriverCreate, DriverUpdate } from '../../services/drivers';

@Component({
  selector: 'app-conductores',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './conductores.html',
  styleUrls: ['./conductores.css']
})
export class ConductoresComponent implements OnInit {
  drivers: DriverSummary[] = [];
  selected: DriverSummary | null = null;

  isLoading = false;
  errorMessage: string = '';
  successMessage: string = '';

  showModal = false;
  isEditing = false;
  editingDriver: DriverSummary | null = null;

  onlyAvailable = false;

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

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.isLoading = true;
    this.errorMessage = '';
    const source$ = this.onlyAvailable
      ? this.driversService.getAvailableDrivers()
      : this.driversService.getDrivers();

    source$.subscribe({
      next: (data) => {
        this.drivers = data;
        console.log('Conductores cargados:', this.drivers);
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'No se pudieron cargar los conductores';
        this.isLoading = false;
      }
    });
  }

  toggleAvailable(): void {
    this.onlyAvailable = !this.onlyAvailable;
    this.load();
  }

  showCreateForm(): void {
    this.isEditing = false;
    this.editingDriver = null;
    this.resetForm();
    this.showModal = true;
  }

  showEditForm(driver: DriverSummary): void {
    this.isEditing = true;
    this.editingDriver = driver;
    this.form = { ...driver };
    this.showModal = true;
  }

  cancelForm(): void {
    this.showModal = false;
    this.isEditing = false;
    this.editingDriver = null;
    this.resetForm();
  }

  resetForm(): void {
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
  }

  submit(): void {
    if (!this.form.first_name || !this.form.last_name || !this.form.email || !this.form.document_number) {
      this.errorMessage = 'Completa los campos obligatorios';
      return;
    }
    this.isLoading = true;
    this.driversService.createDriver(this.form).subscribe({
      next: (created) => {
        this.drivers = [created, ...this.drivers];
        this.showModal = false;
        this.resetForm();
        this.isLoading = false;
        this.successMessage = 'Conductor creado exitosamente';
        setTimeout(() => (this.successMessage = ''), 3000);
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail || 'No se pudo crear el conductor';
        this.isLoading = false;
      }
    });
  }

  updateDriver(): void {
    if (!this.editingDriver) return;
    this.isLoading = true;
    const updateData: DriverUpdate = {
      first_name: this.form.first_name,
      last_name: this.form.last_name,
      email: this.form.email,
      phone: this.form.phone,
      document_number: this.form.document_number,
      license_type: this.form.license_type,
      status: this.form.status,
      is_available: this.form.is_available
    };
    this.driversService.updateDriver(this.editingDriver.id, updateData).subscribe({
      next: (updated) => {
        const index = this.drivers.findIndex(d => d.id === updated.id);
        if (index !== -1) this.drivers[index] = updated;
        this.showModal = false;
        this.resetForm();
        this.isLoading = false;
        this.successMessage = 'Conductor actualizado exitosamente';
        setTimeout(() => (this.successMessage = ''), 3000);
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail || 'No se pudo actualizar el conductor';
        this.isLoading = false;
      }
    });
  }

  deleteDriver(driver: DriverSummary): void {
    if (confirm(`¿Eliminar al conductor ${driver.first_name} ${driver.last_name}?`)) {
      this.driversService.deleteDriver(driver.id).subscribe({
        next: () => {
          this.drivers = this.drivers.filter(d => d.id !== driver.id);
          this.successMessage = 'Conductor eliminado exitosamente';
          setTimeout(() => (this.successMessage = ''), 3000);
        },
        error: (err) => {
          this.errorMessage = err?.error?.detail || 'No se pudo eliminar el conductor';
        }
      });
    }
  }
}


