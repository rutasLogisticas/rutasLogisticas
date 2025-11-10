import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ClientsService, ClientSummary, ClientCreate, ClientUpdate } from '../../services/clients';

@Component({
  selector: 'app-clientes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './clientes.html',
  styleUrls: ['./clientes.css']
})
export class ClientesComponent implements OnInit {
  clients: ClientSummary[] = [];
  selected: ClientSummary | null = null;

  // Estados
  isLoading = false;
  errorMessage: string = '';
  successMessage: string = '';

  // Modal
  showModal = false;
  isEditing = false;
  editingClient: ClientSummary | null = null;

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

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.clientsService.getClients().subscribe({
      next: (data) => {
        this.clients = data;
        console.log('Clientes cargados:', this.clients);
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'No se pudieron cargar los clientes';
        this.isLoading = false;
      }
    });
  }

  // --- Modal ---
  showCreateForm(): void {
    this.isEditing = false;
    this.editingClient = null;
    this.resetForm();
    this.showModal = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  showEditForm(client: ClientSummary): void {
    this.isEditing = true;
    this.editingClient = client;
    this.form = {
      name: client.name,
      email: client.email,
      phone: client.phone,
      company: client.company || '',
      client_type: client.client_type,
      status: client.status,
      is_active: client.is_active
    };
    this.showModal = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  cancelForm(): void {
    this.showModal = false;
    this.isEditing = false;
    this.editingClient = null;
    this.resetForm();
    this.errorMessage = '';
    this.successMessage = '';
    this.isLoading = false;
  }

  resetForm(): void {
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

  // --- CRUD ---
  submit(): void {
    if (!this.form.name || !this.form.email || !this.form.phone) {
      this.errorMessage = 'Completa los campos obligatorios';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.clientsService.createClient(this.form).subscribe({
      next: (created) => {
        this.clients = [created, ...this.clients];
        this.resetForm();
        this.showModal = false;
        this.isLoading = false;
        this.successMessage = 'Cliente creado exitosamente';
        setTimeout(() => (this.successMessage = ''), 3000);
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail || 'No se pudo crear el cliente';
        this.isLoading = false;
      }
    });
  }

  updateClient(): void {
    if (!this.editingClient || !this.form.name || !this.form.email || !this.form.phone) {
      this.errorMessage = 'Completa los campos obligatorios';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const updateData: ClientUpdate = {
      name: this.form.name,
      email: this.form.email,
      phone: this.form.phone,
      company: this.form.company,
      client_type: this.form.client_type,
      status: this.form.status,
      is_active: this.form.is_active
    };

    this.clientsService.updateClient(this.editingClient.id, updateData).subscribe({
      next: (updated) => {
        const index = this.clients.findIndex(c => c.id === updated.id);
        if (index !== -1) {
          this.clients[index] = updated;
        }
        this.resetForm();
        this.showModal = false;
        this.isLoading = false;
        this.successMessage = 'Cliente actualizado exitosamente';
        setTimeout(() => (this.successMessage = ''), 3000);
      },
      error: (err) => {
        this.errorMessage = err?.error?.detail || 'No se pudo actualizar el cliente';
        this.isLoading = false;
      }
    });
  }

  deleteClient(client: ClientSummary): void {
    if (confirm(`¿Estás seguro de que quieres eliminar al cliente ${client.name}?`)) {
      this.clientsService.deleteClient(client.id).subscribe({
        next: () => {
          this.clients = this.clients.filter(c => c.id !== client.id);
          if (this.selected?.id === client.id) {
            this.selected = null;
          }
          this.successMessage = 'Cliente eliminado exitosamente';
          setTimeout(() => (this.successMessage = ''), 3000);
        },
        error: (err) => {
          this.errorMessage = err?.error?.detail || 'No se pudo eliminar el cliente';
        }
      });
    }
  }
}
