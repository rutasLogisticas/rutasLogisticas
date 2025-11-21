import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';
import { AuthService } from './auth';

export interface Permission {
  id: number;
  name: string;
  resource: string;
  action: string;
  description?: string;
  is_active: boolean;
}

export interface Role {
  id: number;
  name: string;
  description?: string;
  is_active: boolean;
  permissions: Permission[];
}

export interface RoleSummary {
  id: number;
  name: string;
  description?: string;
  is_active: boolean;
  permissions_count: number;
}

export interface RoleCreate {
  name: string;
  description?: string;
  permission_ids?: number[];
}

export interface RoleUpdate {
  name?: string;
  description?: string;
  permission_ids?: number[];
  is_active?: boolean;
}

export interface UserPermissions {
  user_id: number;
  username: string;
  role_id?: number;
  role_name?: string;
  permissions: Permission[];
  total_permissions: number;
}

@Injectable({
  providedIn: 'root'
})
export class RolesService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? 'http://localhost:8000/api/v1/roles'
      : 'http://app:8000/api/v1/roles';
  }

  private getAuthHeaders(): HttpHeaders {
    return this.authService.getAuthHeaders();
  }

  // Roles
  getRoles(): Observable<RoleSummary[]> {
    return this.http.get<RoleSummary[]>(`${this.apiUrl}/`, { headers: this.getAuthHeaders() });
  }

  getRole(id: number): Observable<Role> {
    return this.http.get<Role>(`${this.apiUrl}/${id}`, { headers: this.getAuthHeaders() });
  }

  createRole(role: RoleCreate): Observable<Role> {
    return this.http.post<Role>(`${this.apiUrl}/`, role, { headers: this.getAuthHeaders() });
  }

  updateRole(id: number, role: RoleUpdate): Observable<Role> {
    return this.http.put<Role>(`${this.apiUrl}/${id}`, role, { headers: this.getAuthHeaders() });
  }

  deleteRole(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`, { headers: this.getAuthHeaders() });
  }

  // Permisos
  getAllPermissions(): Observable<Permission[]> {
    return this.http.get<Permission[]>(`${this.apiUrl}/permissions/all`, { headers: this.getAuthHeaders() });
  }

  // Permisos de usuario
  getUserPermissions(userId: number): Observable<UserPermissions> {
    return this.http.get<UserPermissions>(`${this.apiUrl}/users/${userId}/permissions`, { headers: this.getAuthHeaders() });
  }
}
