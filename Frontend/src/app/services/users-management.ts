import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';
import { AuthService } from './auth';

export interface User {
  id: number;
  username: string;
  role_id?: number;
  is_active: boolean;
  role?: {
    id: number;
    name: string;
  };
}

export interface UserCreate {
  username: string;
  password: string;
  security_question1?: string;
  security_answer1?: string;
  security_question2?: string;
  security_answer2?: string;
  role_id?: number;
  is_active?: boolean;
}

export interface UserUpdate {
  username?: string;
  role_id?: number;
  is_active?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class UsersManagementService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? 'http://localhost:8000/api/v1/userses'
      : 'http://app:8000/api/v1/userses';
  }

  private getAuthHeaders(): HttpHeaders {
    return this.authService.getAuthHeaders();
  }

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/`, { headers: this.getAuthHeaders() });
  }

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}`, { headers: this.getAuthHeaders() });
  }

  createUser(user: UserCreate): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/`, user, { headers: this.getAuthHeaders() });
  }

  updateUser(id: number, user: UserUpdate): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/${id}`, user, { headers: this.getAuthHeaders() });
  }

  deleteUser(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`, { headers: this.getAuthHeaders() });
  }

  getCurrentUserPermissions(): Observable<any> {
    return this.http.get(`${this.apiUrl}/me/permissions`, { headers: this.getAuthHeaders() });
  }
}
