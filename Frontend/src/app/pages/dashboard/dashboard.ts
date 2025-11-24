import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuditService } from '../../services/audit';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
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

  constructor(
    private auditService: AuditService,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}
  showUserMenu = false;
  userRole: string | null = null;
  isAdmin: boolean = false;
  isOperador: boolean = false;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    // 🔥 Evita error en SSR
    if (isPlatformBrowser(this.platformId)) {
      this.username = localStorage.getItem('username');
      this.userId = Number(localStorage.getItem('userId'));   // <-- AHORA SÍ la clave correcta
      this.userRole = this.authService.getCurrentRole();
      this.isAdmin = this.authService.isAdmin();
      this.isOperador = this.authService.isOperador();
    } catch {
      this.username = null;
      this.userRole = null;
    }
  }

  toggleUserMenu() {
    this.showUserMenu = !this.showUserMenu;
  }

  closeUserMenu() {
    this.showUserMenu = false;
  }

  logout() {
    console.log("🟦 actorId enviado al backend:", this.userId);

    this.auditService.registrarLogout(this.userId).subscribe({
      next: () => {
        if (isPlatformBrowser(this.platformId)) {
          localStorage.clear();
        }
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error("Error registrando logout:", err);
        if (isPlatformBrowser(this.platformId)) {
          localStorage.clear();
        }
        this.router.navigate(['/login']);
      }
    });
    this.authService.logout();
    location.assign('/login');
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
