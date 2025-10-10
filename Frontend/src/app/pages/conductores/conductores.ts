import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DriversService, DriverSummary, DriverCreate } from '../../services/drivers';

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
      next: (data) => {
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
      next: (created) => {
        this.drivers = [created, ...this.drivers];
        this.resetForm();
      },
      error: (err) => {
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
  }
}
