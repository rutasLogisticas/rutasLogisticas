import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AddressesService, AddressSummary, AddressCreate, AddressUpdate } from '../../services/addresses';

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
  editingAddress: AddressSummary | null = null;
  isEditing = false;

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
    this.isEditing = false;
    this.editingAddress = null;
  }

  editAddress(address: AddressSummary) {
    this.editingAddress = address;
    this.isEditing = true;
    this.form = {
      client_id: address.client_id,
      street: address.street,
      city: address.city,
      state: address.state,
      postal_code: address.postal_code,
      country: address.country,
      address_type: address.address_type,
      is_primary: address.is_primary
    };
  }

  updateAddress() {
    if (!this.editingAddress || !this.form.street || !this.form.city || !this.form.state || !this.form.postal_code) {
      this.error = 'Completa los campos obligatorios';
      return;
    }
    
    this.error = null;
    const updateData: AddressUpdate = {
      street: this.form.street,
      city: this.form.city,
      state: this.form.state,
      postal_code: this.form.postal_code,
      country: this.form.country,
      address_type: this.form.address_type,
      is_primary: this.form.is_primary
    };

    this.addressesService.updateAddress(this.editingAddress.id, updateData).subscribe({
      next: (updated) => {
        const index = this.addresses.findIndex(a => a.id === updated.id);
        if (index !== -1) {
          this.addresses[index] = updated;
        }
        this.resetForm();
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo actualizar la dirección';
      }
    });
  }

  deleteAddress(address: AddressSummary) {
    if (confirm(`¿Estás seguro de que quieres eliminar esta dirección en ${address.city}?`)) {
      this.addressesService.deleteAddress(address.id).subscribe({
        next: () => {
          this.addresses = this.addresses.filter(a => a.id !== address.id);
          if (this.selected?.id === address.id) {
            this.selected = null;
          }
        },
        error: (err) => {
          this.error = err?.error?.detail || 'No se pudo eliminar la dirección';
        }
      });
    }
  }
}


