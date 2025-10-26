import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, timeout } from 'rxjs/operators';
import { isPlatformBrowser } from '@angular/common';

export interface GeocodeResult {
  address: string;
  latitude: number;
  longitude: number;
}

export interface GeocodeRequest {
  address: string;
}

@Injectable({
  providedIn: 'root'
})
export class GeocodingService {
  private apiUrl: string;
  
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.apiUrl = isPlatformBrowser(this.platformId) 
      ? 'http://localhost:8000/api/v1'
      : 'http://app:8000/api/v1';
  }

  geocodeAddress(address: string): Observable<GeocodeResult> {
    const body: GeocodeRequest = { address };
    
    return this.http.post<GeocodeResult>(
      `${this.apiUrl}/geocoding/`, 
      body,
      this.httpOptions
    ).pipe(
      timeout(10000), // Timeout de 10 segundos
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Ocurrió un error desconocido';
    
    if (error.error instanceof ErrorEvent) {
      // Error del lado del cliente
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Error del lado del servidor
      if (error.status === 0) {
        errorMessage = 'No se pudo conectar con el servidor. Verifica que el backend esté corriendo en http://localhost:5000';
      } else if (error.status === 404) {
        errorMessage = 'No se encontraron coordenadas para esa dirección';
      } else if (error.status === 400) {
        errorMessage = error.error?.error || 'Solicitud inválida';
      } else {
        errorMessage = `Error ${error.status}: ${error.error?.error || error.message}`;
      }
    }
    
    console.error('Error en geocoding:', errorMessage);
    return throwError(() => ({ error: { error: errorMessage } }));
  }
}