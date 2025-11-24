import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UsersManagementService, User, UserCreate, UserUpdate } from '../../services/users-management';
import { RolesService, RoleSummary } from '../../services/roles';
import { SECURITY_QUESTIONS } from '../../shared/security-questions';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-usuarios',
  standalone: true,
  imports: [CommonModule, FormsModule, DatePipe],
  templateUrl: './usuarios.html',
  styleUrls: ['./usuarios.css']
})
export class UsuariosComponent implements OnInit, OnDestroy {
  users: User[] = [];
  roles: RoleSummary[] = [];
  availableQuestions = SECURITY_QUESTIONS;
  loading = false;
  error: string | null = null;

  // Modal states
  showCreateModal = false;
  showEditModal = false;
  showDeleteModal = false;
  selectedUser: User | null = null;
  
  // Debug variable
  debugMessage = '';

  private subscriptions: Subscription[] = [];

  // Form data
  userForm: UserCreate = {
    username: '',
    password: '',
    security_question1: '',
    security_answer1: '',
    security_question2: '',
    security_answer2: '',
    role_id: undefined,
    is_active: true
  };

  constructor(
    private usersService: UsersManagementService,
    private rolesService: RolesService
  ) {}

  ngOnInit(): void {
    this.loadUsers();
    this.loadRoles();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  loadUsers(): void {
    this.loading = true;
    this.error = null;
    const sub = this.usersService.getUsers().subscribe({
      next: (data) => {
        this.users = data;
        this.loading = false;
        console.log('Usuarios cargados:', this.users);
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error cargando usuarios';
        this.loading = false;
        console.error('Error cargando usuarios:', err);
      }
    });
    this.subscriptions.push(sub);
  }

  loadRoles(): void {
    const sub = this.rolesService.getRoles().subscribe({
      next: (data) => {
        this.roles = data.filter(r => r.is_active);
        console.log('Roles cargados:', this.roles);
      },
      error: (err) => {
        console.error('Error cargando roles:', err);
      }
    });
    this.subscriptions.push(sub);
  }

  // Modal management
  showCreateForm(): void {
    console.log('showCreateForm called');
    this.debugMessage = 'showCreateForm called at ' + new Date().toLocaleTimeString();
    this.userForm = {
      username: '',
      password: '',
      security_question1: this.availableQuestions[0], // "¿Cuál es el nombre de tu primera mascota?"
      security_answer1: '',
      security_question2: this.availableQuestions[1], // "¿En qué ciudad naciste?"
      security_answer2: '',
      role_id: undefined,
      is_active: true
    };
    this.showCreateModal = true;
    console.log('showCreateModal set to:', this.showCreateModal);
  }

  showEditForm(user: User): void {
    console.log('showEditForm called for user:', user);
    this.selectedUser = user;
    this.userForm = {
      username: user.username,
      password: '', // No mostramos la contraseña actual
      role_id: user.role_id,
      is_active: user.is_active
    };
    this.showEditModal = true;
    console.log('showEditModal set to:', this.showEditModal);
  }

  showDeleteForm(user: User): void {
    this.selectedUser = user;
    this.showDeleteModal = true;
  }

  closeModals(): void {
    this.showCreateModal = false;
    this.showEditModal = false;
    this.showDeleteModal = false;
    this.selectedUser = null;
    this.error = null;
  }

  // CRUD operations
  createUser(): void {
    if (!this.userForm.username.trim() || !this.userForm.password.trim()) {
      this.error = 'El nombre de usuario y contraseña son requeridos';
      return;
    }

    this.loading = true;
    this.error = null;
    const sub = this.usersService.createUser(this.userForm).subscribe({
      next: () => {
        this.loadUsers();
        this.closeModals();
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error creando usuario';
        this.loading = false;
        console.error('Error creando usuario:', err);
      }
    });
    this.subscriptions.push(sub);
  }

  updateUser(): void {
    if (!this.selectedUser || !this.userForm.username.trim()) {
      this.error = 'El nombre de usuario es requerido';
      return;
    }

    this.loading = true;
    this.error = null;
    const updateData: UserUpdate = {
      username: this.userForm.username,
      role_id: this.userForm.role_id,
      is_active: this.userForm.is_active
    };

    const sub = this.usersService.updateUser(this.selectedUser.id, updateData).subscribe({
      next: () => {
        this.loadUsers();
        this.closeModals();
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error actualizando usuario';
        this.loading = false;
        console.error('Error actualizando usuario:', err);
      }
    });
    this.subscriptions.push(sub);
  }

  confirmDeleteUser(user: User): void {
    this.debugMessage = `confirmDeleteUser called for user ID ${user.id} at ${new Date().toLocaleTimeString()}`;
    console.log(this.debugMessage);
    this.selectedUser = user;
    this.showDeleteModal = true;
    console.log('showDeleteModal set to:', this.showDeleteModal);
  }

  deleteUser(): void {
    if (!this.selectedUser?.id) return;
    this.loading = true;
    this.error = null;
    const sub = this.usersService.deleteUser(this.selectedUser.id).subscribe({
      next: () => {
        this.loadUsers();
        this.closeModals();
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error eliminando usuario';
        this.loading = false;
        console.error('Error eliminando usuario:', err);
      }
    });
    this.subscriptions.push(sub);
  }

  // Utility methods
  getRoleName(roleId?: number): string {
    if (!roleId) return 'Sin rol';
    const role = this.roles.find(r => r.id === roleId);
    return role ? role.name : 'Rol desconocido';
  }

  getStatusLabel(isActive: boolean): string {
    return isActive ? 'Activo' : 'Inactivo';
  }

  getStatusClass(isActive: boolean): string {
    return isActive ? 'badge-success' : 'badge-danger';
  }
}
