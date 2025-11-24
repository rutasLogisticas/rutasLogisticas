import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl: string;
  private readonly storageKey = 'username';

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    // En el navegador usa localhost, en SSR usa el nombre del servicio Docker
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? 'http://localhost:8000/api/v1'
      : 'http://app:8000/api/v1';
  }

  // 🔹 Inicio de sesión
  login(data: { username: string; password: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/userses/login`, data).pipe(
      tap((response: any) => {
        if (response.access_token) {
          this.saveToken(response.access_token);
          if (isPlatformBrowser(this.platformId)) {
            localStorage.setItem('username', response.username);
            localStorage.setItem('user_id', response.user_id);
            if (response.role) {
              localStorage.setItem('role_id', response.role.id);
              localStorage.setItem('role_name', response.role.name);
            }
          }
        }
      })
    );
  }

  // 🔹 Guardar token
  saveToken(token: string): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem('token', token);
    }
  }

  // 🔹 Obtener token
  getToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem('token');
    }
    return null;
  }

  // 🔹 Verificar si está autenticado
  isAuthenticated(): boolean {
    if (!this.canUseBrowserStorage()) {
      return false;
    }
    try {
      return !!localStorage.getItem('token') && !!localStorage.getItem(this.storageKey);
    } catch {
      return false;
    }
  }

  // 🔹 Obtener headers con autorización
  getAuthHeaders(): HttpHeaders {
    const token = this.getToken();
    if (token) {
      return new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      });
    }
    return new HttpHeaders({ 'Content-Type': 'application/json' });
  }

  // 🔹 Registro (incluye preguntas de seguridad)
  register(data: {
    username: string;
    password: string;
    security_question1?: string;
    security_answer1?: string;
    security_question2?: string;
    security_answer2?: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}/userses/register`, data);
  }

  // 🔹 Paso 1: Solicitar recuperación (envía usuario)
  recoveryStart(username: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/userses/recovery/start`, { username });
  }

  // 🔹 Paso 2: Validar respuestas de seguridad
  recoveryVerify(username: string, answers: string[]): Observable<any> {
    const body = {
      username,
      answers,
    };
    console.log('📤 Body enviado a FastAPI:', body);
    return this.http.post(`${this.apiUrl}/userses/recovery/verify`, body);
  }

  // 🔹 Paso 3: Restablecer contraseña con token temporal
  recoveryReset(token: string, newPassword: string, username: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/userses/recovery/reset`, {
      token,
      username,           // ✅ <-- Este campo es obligatorio
      new_password: newPassword
    });
  }
  // 🔹 Método simplificado para compatibilidad
  recoverPassword(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/userses/recovery`, data);
  }

  // 🔹 Establecer sesión
  setSession(username: string): void {
    if (!this.canUseBrowserStorage()) {
      return;
    }
    try {
      localStorage.setItem(this.storageKey, username);
    } catch {
      // ignored
    }
  }

  // 🔹 Limpiar sesión
  clearSession(): void {
    if (!this.canUseBrowserStorage()) {
      return;
    }
    try {
      localStorage.removeItem('token');
      localStorage.removeItem(this.storageKey);
      localStorage.removeItem('user_id');
      localStorage.removeItem('userId');
      localStorage.removeItem('role_id');
      localStorage.removeItem('role_name');
    } catch {
      // ignored
    }
  }

  // 🔹 Cerrar sesión (con llamada al backend)
  logout(): Observable<any> {
    const storedUserId = localStorage.getItem("userId") || localStorage.getItem("user_id");
    const storedUsername = localStorage.getItem("username");

    return this.http.post(
      `${this.apiUrl}/userses/logout`,
      {},
      {
        headers: {
          "X-User-Id": storedUserId ?? "",
          "X-Username": storedUsername ?? ""
        }
      }
    );
  }

  // 🔹 Obtener nombre de usuario actual
  getCurrentUsername(): string | null {
    if (!this.canUseBrowserStorage()) {
      return null;
    }
    try {
      return localStorage.getItem(this.storageKey);
    } catch {
      return null;
    }
  }

  // 🔹 Obtener rol del usuario actual
  getCurrentRole(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem('role_name');
    }
    return null;
  }

  // 🔹 Verificar si el usuario es admin
  isAdmin(): boolean {
    const role = this.getCurrentRole();
    return role?.toLowerCase() === 'admin';
  }

  // 🔹 Verificar si el usuario es operador (acepta operador, operadores, o user)
  isOperador(): boolean {
    const role = this.getCurrentRole()?.toLowerCase();
    return role === 'operador' || role === 'operadores' || role === 'user';
  }

  // 🔹 Verificar si se puede usar almacenamiento del navegador
  private canUseBrowserStorage(): boolean {
    return isPlatformBrowser(this.platformId);
  }

}

