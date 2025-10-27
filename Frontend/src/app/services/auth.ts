import { HttpClient } from '@angular/common/http';
import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { Observable } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl: string;

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
    return this.http.post(`${this.apiUrl}/userses/login`, data);
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
    return this.http.post(`${this.apiUrl}/userses`, data);
  }

  // 🔹 Paso 1: Solicitar recuperación (envía usuario)
  recoveryStart(username: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/userses/recovery/start`, { username });
  }

  // 🔹 Paso 2: Validar respuestas de seguridad
  recoveryVerify(username: string, answers: { a1: string; a2: string }): Observable<any> {
  const body = {
    username,
    answers: [answers.a1, answers.a2], // ✅ ahora se envía como lista
  };
  console.log('📤 Body enviado a FastAPI:', body);
  return this.http.post(`${this.apiUrl}/userses/recovery/verify`, body);
}

  // 🔹 Paso 3: Restablecer contraseña con token temporal
  recoveryReset(token: string, newPassword: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/userses/recovery/reset`, {
      token,
      new_password: newPassword,
    });
  }
  // 🔹 Método simplificado para compatibilidad
  recoverPassword(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/userses/recovery`, data);
  }

}

