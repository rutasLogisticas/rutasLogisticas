import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class RegisterComponent {
  username = '';
  password = '';
  confirmPassword = '';
  security_answer1 = '';
  security_answer2 = '';
  loading = false;
  readonly passwordPolicyMessage =
    'La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, una letra minúscula y un carácter especial.';

  constructor(public router: Router, private auth: AuthService) {}

  onSubmit() {
    if (!this.isPasswordValid(this.password)) {
      alert(this.passwordPolicyMessage);
      return;
    }

    if (this.password !== this.confirmPassword) {
      alert('Las contraseñas no coinciden');
      return;
    }

    this.loading = true;

    // Las preguntas son fijas
    this.auth.register({
      username: this.username,
      password: this.password,
      security_question1: '¿Cuál es el nombre de tu primera mascota?',
      security_answer1: this.security_answer1,
      security_question2: '¿En qué ciudad naciste?',
      security_answer2: this.security_answer2
    }).subscribe({
      next: () => {
        alert('Usuario registrado con éxito');
        this.router.navigate(['/login']);
      },
      error: (err: any) => {
        console.error(err);
        const message = err?.error?.detail ?? 'Error al registrar el usuario';
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
