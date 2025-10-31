import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { GeocodingService, GeocodeResult } from '../../services/geocoding.service';
import { SanitizeUrlPipe } from '../../pipes/sanitize-url.pipe';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.css']
})
export class InicioComponent implements OnInit, OnDestroy {
  address = '';
  result: GeocodeResult | null = null;
  loading = false;
  locationLoading = false;
  error: string | null = null;
  mapUrl = '';
  currentZoom = 11;
  private subscription?: Subscription;

  // Coordenadas por defecto de Bogotá
  private readonly DEFAULT_LAT = 4.6097;
  private readonly DEFAULT_LNG = -74.0817;
  private readonly DEFAULT_ZOOM = 11;
  private readonly MIN_ZOOM = 5;
  private readonly MAX_ZOOM = 18;

  constructor(
    private geocodingService: GeocodingService,
    private router: Router
  ) {}

  ngOnInit() {
    // Inicializar con un mapa centrado en Bogotá
    this.updateMapUrl(this.DEFAULT_LAT, this.DEFAULT_LNG, this.DEFAULT_ZOOM);
  }

  ngOnDestroy() {
    // Limpiar suscripciones
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }

  geocode() {
    if (!this.address.trim()) {
      this.error = 'Por favor ingresa una dirección';
      return;
    }

    this.loading = true;
    this.error = null;
    this.result = null;

    // Cancelar suscripción anterior si existe
    if (this.subscription) {
      this.subscription.unsubscribe();
    }

    this.subscription = this.geocodingService.geocodeAddress(this.address).subscribe({
      next: (data: any) => {
        this.result = data;
        this.updateMapUrl(data.latitude, data.longitude, 15);
        this.loading = false;
        this.error = null;
      },
      error: (err: any) => {
        console.error('Error geocoding:', err);
        this.error = err?.error?.error || 'No se pudo geocodificar la dirección. Verifica que el backend esté corriendo.';
        this.loading = false;
        this.result = null;
      }
    });
  }

  updateMapUrl(lat: number, lng: number, zoom: number) {
    this.currentZoom = zoom;
    // Usamos OpenStreetMap embed con parámetros más precisos
    const bbox = this.calculateBBox(lat, lng, zoom);
    this.mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${lat},${lng}`;
  }

  private calculateBBox(lat: number, lng: number, zoom: number): string {
    // Calcular bounding box basado en zoom
    const offset = 0.01 / (zoom / 11);
    return `${lng - offset},${lat - offset},${lng + offset},${lat + offset}`;
  }

  getCurrentLocation() {
    if (!navigator.geolocation) {
      this.error = 'Geolocalización no soportada por este navegador';
      return;
    }

    this.locationLoading = true;
    this.error = null;

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        
        this.address = `Mi ubicación actual (${lat.toFixed(6)}, ${lng.toFixed(6)})`;
        this.result = {
          address: this.address,
          latitude: lat,
          longitude: lng
        };
        this.updateMapUrl(lat, lng, 15);
        this.locationLoading = false;
      },
      (error) => {
        this.locationLoading = false;
        switch (error.code) {
          case error.PERMISSION_DENIED:
            this.error = 'Permiso de ubicación denegado';
            break;
          case error.POSITION_UNAVAILABLE:
            this.error = 'Ubicación no disponible';
            break;
          case error.TIMEOUT:
            this.error = 'Tiempo de espera agotado';
            break;
          default:
            this.error = 'Error desconocido al obtener la ubicación';
            break;
        }
      }
    );
  }

  zoomIn() {
    if (this.currentZoom < this.MAX_ZOOM) {
      const lat = this.result?.latitude || this.DEFAULT_LAT;
      const lng = this.result?.longitude || this.DEFAULT_LNG;
      this.updateMapUrl(lat, lng, this.currentZoom + 1);
    }
  }

  zoomOut() {
    if (this.currentZoom > this.MIN_ZOOM) {
      const lat = this.result?.latitude || this.DEFAULT_LAT;
      const lng = this.result?.longitude || this.DEFAULT_LNG;
      this.updateMapUrl(lat, lng, this.currentZoom - 1);
    }
  }

  centerMap() {
    const lat = this.result?.latitude || this.DEFAULT_LAT;
    const lng = this.result?.longitude || this.DEFAULT_LNG;
    this.updateMapUrl(lat, lng, this.DEFAULT_ZOOM);
  }

  navigateToClients() {
    this.router.navigate(['/dashboard/clientes']);
  }

  navigateToVehicles() {
    this.router.navigate(['/dashboard/vehiculos']);
  }

  navigateToMap() {
    this.router.navigate(['/dashboard/mapa']);
  }

  clear() {
    this.address = '';
    this.result = null;
    this.error = null;
    this.updateMapUrl(this.DEFAULT_LAT, this.DEFAULT_LNG, this.DEFAULT_ZOOM);
  }
}