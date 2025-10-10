import { bootstrapApplication } from '@angular/platform-browser';
import { importProvidersFrom } from '@angular/core';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app/app';
import { routes } from './app/app.routes';

// 🚀 Bootstrap principal
bootstrapApplication(AppComponent, {
  providers: [
  provideRouter(routes),
    importProvidersFrom(FormsModule),
    provideHttpClient(withFetch())
  ]
}).catch(err => console.error(err));
