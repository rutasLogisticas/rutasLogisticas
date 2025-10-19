import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ClientsService, ClientSummary, ClientCreate, ClientUpdate } from '../../services/clients';

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
  editingClient: ClientSummary | null = null;
  isEditing = false;

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
    this.isEditing = false;
    this.editingClient = null;
  }

  editClient(client: ClientSummary) {
    this.editingClient = client;
    this.isEditing = true;
    this.form = {
      name: client.name,
      email: client.email,
      phone: client.phone,
      company: client.company || '',
      client_type: client.client_type,
      status: client.status,
      is_active: client.is_active
    };
  }

  updateClient() {
    if (!this.editingClient || !this.form.name || !this.form.email || !this.form.phone) {
      this.error = 'Completa los campos obligatorios';
      return;
    }
    
    this.error = null;
    const updateData: ClientUpdate = {
      name: this.form.name,
      email: this.form.email,
      phone: this.form.phone,
      company: this.form.company,
      client_type: this.form.client_type,
      status: this.form.status
    };

    this.clientsService.updateClient(this.editingClient.id, updateData).subscribe({
      next: (updated) => {
        const index = this.clients.findIndex(c => c.id === updated.id);
        if (index !== -1) {
          this.clients[index] = updated;
        }
        this.resetForm();
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo actualizar el cliente';
      }
    });
  }

  deleteClient(client: ClientSummary) {
    if (confirm(`¿Estás seguro de que quieres eliminar al cliente ${client.name}?`)) {
      this.clientsService.deleteClient(client.id).subscribe({
        next: () => {
          this.clients = this.clients.filter(c => c.id !== client.id);
          if (this.selected?.id === client.id) {
            this.selected = null;
          }
        },
        error: (err) => {
          this.error = err?.error?.detail || 'No se pudo eliminar el cliente';
        }
      });
    }
  }
}


