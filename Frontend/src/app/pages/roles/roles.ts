import { Component, OnInit } from '@angular/core';
import { CommonModule, KeyValuePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RolesService, RoleSummary, Role, RoleCreate, RoleUpdate, Permission } from '../../services/roles';

@Component({
  selector: 'app-roles',
  standalone: true,
  imports: [CommonModule, FormsModule, KeyValuePipe],
  templateUrl: './roles.html',
  styleUrls: ['./roles.css']
})
export class RolesComponent implements OnInit {
  roles: RoleSummary[] = [];
  permissions: Permission[] = [];
  loading = false;
  error: string | null = null;

  // Modal states
  showCreateModal = false;
  showEditModal = false;
  showDeleteModal = false;
  selectedRole: Role | null = null;
  
  // Debug variable
  debugMessage = '';

  // Form data
  roleForm: RoleCreate = {
    name: '',
    description: '',
    permission_ids: []
  };

  // Permissions grouped by resource
  permissionsByResource: { [key: string]: Permission[] } = {};

  constructor(private rolesService: RolesService) {}

  ngOnInit(): void {
    this.loadRoles();
    this.loadPermissions();
  }

  loadRoles(): void {
    this.loading = true;
    this.rolesService.getRoles().subscribe({
      next: (data) => {
        this.roles = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error cargando roles';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  loadPermissions(): void {
    this.rolesService.getAllPermissions().subscribe({
      next: (data) => {
        this.permissions = data;
        this.groupPermissionsByResource();
      },
      error: (err) => {
        console.error('Error cargando permisos:', err);
      }
    });
  }

  groupPermissionsByResource(): void {
    this.permissionsByResource = {};
    this.permissions.forEach(permission => {
      if (!this.permissionsByResource[permission.resource]) {
        this.permissionsByResource[permission.resource] = [];
      }
      this.permissionsByResource[permission.resource].push(permission);
    });
  }

  // Modal management
  showCreateRoleForm(): void {
    console.log('showCreateRoleForm called');
    this.debugMessage = 'showCreateRoleForm called at ' + new Date().toLocaleTimeString();
    this.roleForm = { name: '', description: '', permission_ids: [] };
    this.showCreateModal = true;
    console.log('showCreateModal set to:', this.showCreateModal);
  }

  showEditRoleForm(role: RoleSummary): void {
    this.loading = true;
    this.rolesService.getRole(role.id).subscribe({
      next: (data) => {
        this.selectedRole = data;
        this.roleForm = {
          name: data.name,
          description: data.description,
          permission_ids: data.permissions.map(p => p.id)
        };
        this.showEditModal = true;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error cargando rol';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  showDeleteRoleForm(role: RoleSummary): void {
    this.selectedRole = role as any;
    this.showDeleteModal = true;
  }

  closeModals(): void {
    this.showCreateModal = false;
    this.showEditModal = false;
    this.showDeleteModal = false;
    this.selectedRole = null;
    this.error = null;
  }

  // Permission management
  togglePermission(permissionId: number): void {
    const index = this.roleForm.permission_ids!.indexOf(permissionId);
    if (index > -1) {
      this.roleForm.permission_ids!.splice(index, 1);
    } else {
      this.roleForm.permission_ids!.push(permissionId);
    }
  }

  isPermissionSelected(permissionId: number): boolean {
    return this.roleForm.permission_ids!.includes(permissionId);
  }

  selectAllPermissions(resource: string): void {
    const resourcePermissions = this.permissionsByResource[resource];
    const allSelected = resourcePermissions.every(p => this.isPermissionSelected(p.id));
    
    if (allSelected) {
      // Deselect all
      resourcePermissions.forEach(p => {
        const index = this.roleForm.permission_ids!.indexOf(p.id);
        if (index > -1) {
          this.roleForm.permission_ids!.splice(index, 1);
        }
      });
    } else {
      // Select all
      resourcePermissions.forEach(p => {
        if (!this.isPermissionSelected(p.id)) {
          this.roleForm.permission_ids!.push(p.id);
        }
      });
    }
  }

  isResourceFullySelected(resource: string): boolean {
    const resourcePermissions = this.permissionsByResource[resource];
    return resourcePermissions.every(p => this.isPermissionSelected(p.id));
  }

  // CRUD operations
  createRole(): void {
    if (!this.roleForm.name.trim()) {
      this.error = 'El nombre del rol es requerido';
      return;
    }

    this.loading = true;
    this.rolesService.createRole(this.roleForm).subscribe({
      next: () => {
        this.loadRoles();
        this.closeModals();
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error creando rol';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  updateRole(): void {
    if (!this.selectedRole || !this.roleForm.name.trim()) {
      this.error = 'El nombre del rol es requerido';
      return;
    }

    this.loading = true;
    const updateData: RoleUpdate = {
      name: this.roleForm.name,
      description: this.roleForm.description,
      permission_ids: this.roleForm.permission_ids
    };

    this.rolesService.updateRole(this.selectedRole.id, updateData).subscribe({
      next: () => {
        this.loadRoles();
        this.closeModals();
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error actualizando rol';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  deleteRole(): void {
    if (!this.selectedRole) return;

    this.loading = true;
    this.rolesService.deleteRole(this.selectedRole.id).subscribe({
      next: () => {
        this.loadRoles();
        this.closeModals();
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Error eliminando rol';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  // Utility methods
  getActionLabel(action: string): string {
    const labels: { [key: string]: string } = {
      'create': 'Crear',
      'read': 'Ver',
      'update': 'Actualizar',
      'delete': 'Eliminar'
    };
    return labels[action] || action;
  }

  getResourceLabel(resource: string): string {
    const labels: { [key: string]: string } = {
      'users': 'Usuarios',
      'roles': 'Roles',
      'clients': 'Clientes',
      'vehicles': 'Vehículos',
      'drivers': 'Conductores',
      'orders': 'Pedidos',
      'reports': 'Reportes'
    };
    return labels[resource] || resource;
  }
}
