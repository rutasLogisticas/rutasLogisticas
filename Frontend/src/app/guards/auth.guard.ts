import { CanActivateChildFn, CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth';

const buildRedirect = (router: Router, redirectUrl: string) =>
  router.createUrlTree(['/restricted'], {
    queryParams: { redirect: redirectUrl || undefined }
  });

export const authGuard: CanActivateFn = (_route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  if (authService.isAuthenticated()) {
    return true;
  }
  
  return buildRedirect(router, state.url);
};

export const authChildGuard: CanActivateChildFn = (route, state) => authGuard(route, state);

