import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GeocodingService, GeocodeResult } from '../../services/geocoding.service';
import { SanitizeUrlPipe } from '../../pipes/sanitize-url.pipe';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule, FormsModule, SanitizeUrlPipe],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.css']
})
export class InicioComponent implements OnInit, OnDestroy {
  address = '';
  result: GeocodeResult | null = null;
  loading = false;
  error: string | null = null;
  mapUrl = '';
  private subscription?: Subscription;

  // Coordenadas por defecto de Bogotá
  private readonly DEFAULT_LAT = 4.6097;
  private readonly DEFAULT_LNG = -74.0817;
  private readonly DEFAULT_ZOOM = 11;

  constructor(private geocodingService: GeocodingService) {}

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
      next: (data) => {
        this.result = data;
        this.updateMapUrl(data.latitude, data.longitude, 15);
        this.loading = false;
        this.error = null;
      },
      error: (err) => {
        console.error('Error geocoding:', err);
        this.error = err?.error?.error || 'No se pudo geocodificar la dirección. Verifica que el backend esté corriendo.';
        this.loading = false;
        this.result = null;
      }
    });
  }

  updateMapUrl(lat: number, lng: number, zoom: number) {
    // Usamos OpenStreetMap embed con parámetros más precisos
    const bbox = this.calculateBBox(lat, lng, zoom);
    this.mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${lat},${lng}`;
  }

  private calculateBBox(lat: number, lng: number, zoom: number): string {
    // Calcular bounding box basado en zoom
    const offset = 0.01 / (zoom / 11);
    return `${lng - offset},${lat - offset},${lng + offset},${lat + offset}`;
  }

  clear() {
    this.address = '';
    this.result = null;
    this.error = null;
    this.updateMapUrl(this.DEFAULT_LAT, this.DEFAULT_LNG, this.DEFAULT_ZOOM);
  }
}