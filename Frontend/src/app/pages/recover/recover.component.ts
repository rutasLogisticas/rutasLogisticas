import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-recover',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './recover.component.html',
  styleUrls: ['./recover.component.css']
})
export class RecoverComponent {
  step = 1;
  username = '';
  questions: string[] = [];
  answers: string[] = [];
  newPassword = '';
  confirmPassword = '';
  loading = false;
  tempToken: string = '';
  token: string = 'token-fijo';
  readonly passwordPolicyMessage =
    'La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, una letra minúscula y un carácter especial.';

  constructor(private auth: AuthService, private router: Router) {}

  /** 🔹 Paso 1: Validar que el usuario exista */
  startRecovery() {
    if (!this.username.trim()) {
      alert('Por favor, ingresa tu nombre de usuario.');
      return;
    }

    this.loading = true;
    this.auth.recoveryStart(this.username).subscribe({
      next: (res) => {
        this.questions = res?.questions ?? [];
        this.answers = this.questions.map(() => '');
        if (this.questions.length === 0) {
          this.loading = false;
          alert('Este usuario no tiene preguntas de seguridad configuradas.');
          return;
        }
        this.loading = false;
        this.step = 2; // pasa a preguntas
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
        alert('Usuario no encontrado');
      }
    });
  }

  /** 🔹 Paso 2: Validar respuestas */
  verifyAnswers() {
    const trimmedAnswers = this.answers.map(a => a?.trim()).filter((a): a is string => !!a);
    if (trimmedAnswers.length !== this.questions.length) {
      alert('Por favor, responde todas las preguntas.');
      return;
    }

    this.loading = true;
    this.auth.recoveryVerify(this.username, trimmedAnswers).subscribe({
      next: (res) => {
        console.log('✅ Respuesta backend:', res);
        this.tempToken = res.reset_token;
        this.token = this.tempToken || this.token;
        this.step = 3; // pasa a nueva contraseña
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        const message = err?.error?.detail ?? 'Las respuestas no coinciden.';
        alert(message);
        this.loading = false;
      }
    });
  }

  /** 🔹 Paso 3: Resetear contraseña */
  resetPassword() {
    if (!this.isPasswordValid(this.newPassword)) {
      alert(this.passwordPolicyMessage);
      return;
    }

    if (this.newPassword !== this.confirmPassword) {
      alert('Las contraseñas no coinciden');
      return;
    }

    this.loading = true;
    const tokenToUse = this.tempToken || this.token;
    this.auth.recoveryReset(tokenToUse, this.newPassword, this.username).subscribe({
      next: () => {
        alert('Contraseña actualizada correctamente');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error(err);
        const message = err?.error?.detail ?? 'Error al actualizar la contraseña';
        alert(message);
        this.loading = false;
      }
    });
  }

  private isPasswordValid(password: string): boolean {
    const policyRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9\s])[^\s]{8,}$/;
    return policyRegex.test(password);
  }
}
