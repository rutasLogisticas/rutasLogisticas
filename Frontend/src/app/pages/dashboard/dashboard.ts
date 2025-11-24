import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuditService } from '../../services/audit';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent {
  username: string | null = null;
  userId: number | null = null;

  constructor(
    private auditService: AuditService,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    // 🔥 Evita error en SSR
    if (isPlatformBrowser(this.platformId)) {
      this.username = localStorage.getItem('username');
      this.userId = Number(localStorage.getItem('userId'));   // <-- AHORA SÍ la clave correcta
    }
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
  }
}
