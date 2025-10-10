import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class RegisterComponent {
  username = '';
  password = '';
  confirmPassword = '';
  loading = false;
  error: string | null = null;

  constructor(
    private router: Router,
    private auth: AuthService
  ) {}

  onSubmit() {
    // Validaciones
    if (!this.username || !this.password) {
      this.error = 'Por favor completa todos los campos';
      alert(this.error);
      return;
    }

    if (this.password.length < 4) {
      this.error = 'La contraseña debe tener al menos 4 caracteres';
      alert(this.error);
      return;
    }

    if (this.confirmPassword && this.password !== this.confirmPassword) {
      this.error = 'Las contraseñas no coinciden';
      alert(this.error);
      return;
    }

    this.loading = true;
    this.error = null;

    this.auth.register({ username: this.username, password: this.password }).subscribe({
      next: (response) => {
        this.loading = false;
        alert('Usuario creado exitosamente!');
        // Auto-login después del registro
        localStorage.setItem('username', this.username);
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.detail || 'Error al crear el usuario';
        alert(this.error);
      }
    });
  }
}
