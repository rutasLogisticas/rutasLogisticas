import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuditService } from '../../services/audit';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {
  username: string | null = null;
  userId: number | null = null;
  showUserMenu = false;
  userRole: string | null = null;
  isAdmin: boolean = false;
  isOperador: boolean = false;

  constructor(
    private auditService: AuditService,
    private authService: AuthService,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    this.username = this.authService.getCurrentUsername();
    // Mantener funcionalidad de roles para visibilidad del menú
    if (isPlatformBrowser(this.platformId)) {
      this.userId = Number(localStorage.getItem('userId') || localStorage.getItem('user_id'));
      this.userRole = this.authService.getCurrentRole();
      this.isAdmin = this.authService.isAdmin();
      this.isOperador = this.authService.isOperador();
    }
  }

  toggleUserMenu() {
    this.showUserMenu = !this.showUserMenu;
  }

  closeUserMenu() {
    this.showUserMenu = false;
  }

  logout() {
    // Registrar logout en auditoría si hay userId
    if (this.userId) {
      this.auditService.registrarLogout(this.userId).subscribe({
        next: () => {
          this.authService.clearSession();
          this.router.navigate(['/login']);
        },
        error: (err) => {
          console.error("Error registrando logout:", err);
          this.authService.clearSession();
          this.router.navigate(['/login']);
        }
      });
    } else {
      this.authService.clearSession();
      this.router.navigate(['/login']);
    }
  }

  // Métodos para controlar visibilidad de elementos del menú
  canViewInicio(): boolean {
    return true; // Todos pueden ver inicio
  }

  canViewMapa(): boolean {
    return this.isAdmin; // Solo admin puede ver mapa
  }

  canViewClientes(): boolean {
    return this.isAdmin || this.isOperador;
  }

  canViewPedidos(): boolean {
    return this.isAdmin || this.isOperador;
  }

  canViewVehiculos(): boolean {
    return this.isAdmin || this.isOperador;
  }

  canViewConductores(): boolean {
    return this.isAdmin || this.isOperador;
  }

  canViewReportes(): boolean {
    return this.isAdmin; // Solo admin puede ver reportes
  }

  canViewRoles(): boolean {
    return this.isAdmin; // Solo admin puede ver roles
  }

  canViewUsuarios(): boolean {
    return this.isAdmin; // Solo admin puede ver usuarios
  }
}
