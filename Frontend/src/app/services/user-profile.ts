import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';
import { AuthService } from './auth';

export interface SecurityQuestion {
  id: number;
  question: string;
}

export interface SecurityQuestionUpdate {
  question: string;
  answer: string;
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserProfileService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object,
    private authService: AuthService
  ) {
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? 'http://localhost:8000/api/v1/userses'
      : 'http://app:8000/api/v1/userses';
  }

  // Cambiar contraseña
  changePassword(data: ChangePasswordRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/change-password`, data, { 
      headers: this.authService.getAuthHeaders() 
    });
  }

  // Obtener preguntas de seguridad del usuario actual
  getMySecurityQuestions(): Observable<{questions: SecurityQuestion[]}> {
    return this.http.get<{questions: SecurityQuestion[]}>(`${this.apiUrl}/me/security-questions`, { 
      headers: this.authService.getAuthHeaders() 
    });
  }

  // Actualizar preguntas de seguridad
  updateSecurityQuestions(questions: SecurityQuestionUpdate[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/me/security-questions`, { questions }, { 
      headers: this.authService.getAuthHeaders() 
    });
  }
}
