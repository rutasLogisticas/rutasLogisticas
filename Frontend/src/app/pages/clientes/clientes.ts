import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ClientsService, ClientSummary, ClientCreate } from '../../services/clients';

@Component({
  selector: 'app-clientes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './clientes.html',
  styleUrl: './clientes.css'
})
export class ClientesComponent {
  clients: ClientSummary[] = [];
  selected: ClientSummary | null = null;
  loading = false;
  error: string | null = null;
  companyFilter = '';

  form: ClientCreate = {
    name: '',
    email: '',
    phone: '',
    company: '',
    client_type: 'individual',
    status: 'activo',
    is_active: true
  };

  constructor(private clientsService: ClientsService) {}

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    this.error = null;
    this.clientsService.getClients().subscribe({
      next: (data) => {
        this.clients = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudieron cargar los clientes';
        this.loading = false;
      }
    });
  }

  filterByCompany() {
    if (!this.companyFilter) {
      this.load();
      return;
    }
    this.loading = true;
    this.error = null;
    this.clientsService.getClientsByCompany(this.companyFilter).subscribe({
      next: (data) => {
        this.clients = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudieron filtrar los clientes';
        this.loading = false;
      }
    });
  }

  select(client: ClientSummary) {
    this.selected = client;
  }

  submit() {
    if (!this.form.name || !this.form.email || !this.form.phone) {
      this.error = 'Completa los campos obligatorios';
      return;
    }
    this.error = null;
    this.clientsService.createClient(this.form).subscribe({
      next: (created) => {
        this.clients = [created, ...this.clients];
        this.resetForm();
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo crear el cliente';
      }
    });
  }

  resetForm() {
    this.form = {
      name: '',
      email: '',
      phone: '',
      company: '',
      client_type: 'individual',
      status: 'activo',
      is_active: true
    };
  }
}


