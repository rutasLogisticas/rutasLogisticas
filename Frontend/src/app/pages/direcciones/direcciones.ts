import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AddressesService, AddressSummary, AddressCreate } from '../../services/addresses';

@Component({
  selector: 'app-direcciones',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './direcciones.html',
  styleUrls: ['./direcciones.css']
})
export class DireccionesComponent {
  addresses: AddressSummary[] = [];
  selected: AddressSummary | null = null;
  loading = false;
  error: string | null = null;
  clientIdFilter: number | null = null;
  cityFilter = '';

  form: AddressCreate = {
    client_id: 0,
    street: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'Colombia',
    address_type: 'principal',
    is_primary: false
  };

  constructor(private addressesService: AddressesService) {}

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    this.error = null;
    this.addressesService.getAddresses().subscribe({
      next: (data) => {
        this.addresses = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudieron cargar las direcciones';
        this.loading = false;
      }
    });
  }

  filter() {
    if (this.clientIdFilter) {
      this.loading = true;
      this.addressesService.getByClient(this.clientIdFilter).subscribe({
        next: (data) => { this.addresses = data; this.loading = false; },
        error: () => { this.error = 'No se pudieron filtrar las direcciones'; this.loading = false; }
      });
      return;
    }
    if (this.cityFilter) {
      this.loading = true;
      this.addressesService.getByCity(this.cityFilter).subscribe({
        next: (data) => { this.addresses = data; this.loading = false; },
        error: () => { this.error = 'No se pudieron filtrar las direcciones'; this.loading = false; }
      });
      return;
    }
    this.load();
  }

  select(addr: AddressSummary) {
    this.selected = addr;
  }

  submit() {
    if (!this.form.client_id || !this.form.street || !this.form.city || !this.form.state || !this.form.postal_code) {
      this.error = 'Completa los campos obligatorios';
      return;
    }
    this.error = null;
    this.addressesService.createAddress(this.form).subscribe({
      next: (created) => {
        this.addresses = [created, ...this.addresses];
        this.resetForm();
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo crear la dirección';
      }
    });
  }

  resetForm() {
    this.form = {
      client_id: 0,
      street: '',
      city: '',
      state: '',
      postal_code: '',
      country: 'Colombia',
      address_type: 'principal',
      is_primary: false
    };
  }
}


