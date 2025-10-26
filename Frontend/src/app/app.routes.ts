import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', loadComponent: () => import('./pages/login/login').then(m => m.LoginComponent) },
  { path: 'register', loadComponent: () => import('./pages/register/register').then(m => m.RegisterComponent) },
  {
    path: 'dashboard',
    loadComponent: () => import('./pages/dashboard/dashboard').then(m => m.DashboardComponent),
    children: [
      { path: 'inicio', loadComponent: () => import('./pages/dashboard/inicio').then(m => m.InicioComponent) },
      { path: 'mapa', loadComponent: () => import('./pages/mapa/mapa').then(m => m.MapaComponent) },
      { path: 'vehiculos', loadComponent: () => import('./pages/vehiculos/vehiculos').then(m => m.VehiculosComponent) },
      { path: 'conductores', loadComponent: () => import('./pages/conductores/conductores').then(m => m.ConductoresComponent) },
      { path: 'direcciones', loadComponent: () => import('./pages/direcciones/direcciones').then(m => m.DireccionesComponent) },
      { path: 'clientes', loadComponent: () => import('./pages/clientes/clientes').then(m => m.ClientesComponent) },
      { path: 'reportes', loadComponent: () => import('./pages/reportes/reportes').then(m => m.ReportesComponent) }
    ]
  }
];
