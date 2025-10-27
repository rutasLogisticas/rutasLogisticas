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
  answer1 = '';
  answer2 = '';
  newPassword = '';
  confirmPassword = '';
  loading = false;
  tempToken = '';

  constructor(private auth: AuthService, private router: Router) {}

  /** 🔹 Paso 1: Validar que el usuario exista */
  startRecovery() {
    if (!this.username.trim()) {
      alert('Por favor, ingresa tu nombre de usuario.');
      return;
    }

    this.loading = true;
    this.auth.recoveryStart(this.username).subscribe({
      next: () => {
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
    if (!this.answer1 || !this.answer2) {
      alert('Por favor, responde ambas preguntas.');
      return;
    }

    this.loading = true;
    this.auth.recoveryVerify(this.username, { a1: this.answer1, a2: this.answer2 }).subscribe({
      next: (res) => {
        console.log('✅ Respuesta backend:', res);
        this.tempToken = res.temp_token; // guardamos token del backend
        this.step = 3; // pasa a nueva contraseña
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        alert('Las respuestas no coinciden.');
        this.loading = false;
      }
    });
  }

  /** 🔹 Paso 3: Resetear contraseña */
  resetPassword() {
    if (this.newPassword !== this.confirmPassword) {
      alert('Las contraseñas no coinciden');
      return;
    }

    this.loading = true;
    this.auth.recoveryReset('token-fijo', this.newPassword).subscribe({
      next: () => {
        alert('Contraseña actualizada correctamente');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error(err);
        alert('Error al actualizar la contraseña');
        this.loading = false;
      }
    });
  }
}
