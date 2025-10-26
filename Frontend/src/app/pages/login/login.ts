import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class LoginComponent {
  username = '';
  password = '';
  loading = false;
  error: string | null = null;

  constructor(private router: Router, private auth: AuthService) {}

  onSubmit() {
    if (!this.username || !this.password) return;
    this.loading = true;
    this.error = null;
    this.auth.login({ username: this.username, password: this.password }).subscribe({
      next: () => {
        this.loading = false;
        try {
          localStorage.setItem('username', this.username);
        } catch {}
        this.router.navigate(['/dashboard/inicio']);
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.detail || 'Credenciales incorrectas';
        alert(this.error);
      }
    });
  }
}
