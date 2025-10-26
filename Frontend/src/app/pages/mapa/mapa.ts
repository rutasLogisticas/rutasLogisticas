import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GeocodingService, GeocodeResult } from '../../services/geocoding.service';
import { SanitizeUrlPipe } from '../../pipes/sanitize-url.pipe';
import { Subscription } from 'rxjs';

interface HistoryItem extends GeocodeResult {
  timestamp: number;
}

@Component({
  selector: 'app-mapa',
  standalone: true,
  imports: [CommonModule, FormsModule, SanitizeUrlPipe],
  templateUrl: './mapa.html',
  styleUrls: ['./mapa.css']
})
export class MapaComponent implements OnInit, OnDestroy {
  address = '';
  result: GeocodeResult | null = null;
  loading = false;
  locationLoading = false;
  error: string | null = null;
  mapUrl = '';
  currentZoom = 11;
  isFullscreen = false;
  searchHistory: HistoryItem[] = [];
  
  // Propiedades públicas para el template
  readonly minZoom = 5;
  readonly maxZoom = 18;
  
  private subscription?: Subscription;

  // Configuración del mapa
  private readonly DEFAULT_LAT = 4.6097;
  private readonly DEFAULT_LNG = -74.0817;
  private readonly DEFAULT_ZOOM = 11;
  private readonly HISTORY_KEY = 'mapa_search_history';
  private readonly MAX_HISTORY = 10;

  constructor(private geocodingService: GeocodingService) {}

  ngOnInit() {
    this.loadSearchHistory();
    this.updateMapUrl(this.DEFAULT_LAT, this.DEFAULT_LNG, this.DEFAULT_ZOOM);
  }

  ngOnDestroy() {
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

    if (this.subscription) {
      this.subscription.unsubscribe();
    }

    this.subscription = this.geocodingService.geocodeAddress(this.address).subscribe({
      next: (data: any) => {
        this.result = data;
        this.updateMapUrl(data.latitude, data.longitude, 15);
        this.addToHistory(data);
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
        this.addToHistory(this.result);
        this.locationLoading = false;
      },
      (error) => {
        this.locationLoading = false;
        switch (error.code) {
          case error.PERMISSION_DENIED:
            this.error = 'Permiso de ubicación denegado. Por favor, permite el acceso a tu ubicación.';
            break;
          case error.POSITION_UNAVAILABLE:
            this.error = 'Ubicación no disponible. Verifica tu conexión a internet.';
            break;
          case error.TIMEOUT:
            this.error = 'Tiempo de espera agotado. Intenta nuevamente.';
            break;
          default:
            this.error = 'Error desconocido al obtener la ubicación';
            break;
        }
      }
    );
  }

  updateMapUrl(lat: number, lng: number, zoom: number) {
    this.currentZoom = zoom;
    const bbox = this.calculateBBox(lat, lng, zoom);
    this.mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${lat},${lng}`;
  }

  private calculateBBox(lat: number, lng: number, zoom: number): string {
    const offset = 0.01 / (zoom / 11);
    return `${lng - offset},${lat - offset},${lng + offset},${lat + offset}`;
  }

  zoomIn() {
    if (this.currentZoom < this.maxZoom) {
      const lat = this.result?.latitude || this.DEFAULT_LAT;
      const lng = this.result?.longitude || this.DEFAULT_LNG;
      this.updateMapUrl(lat, lng, this.currentZoom + 1);
    }
  }

  zoomOut() {
    if (this.currentZoom > this.minZoom) {
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

  toggleFullscreen() {
    this.isFullscreen = !this.isFullscreen;
  }

  clear() {
    this.address = '';
    this.result = null;
    this.error = null;
    this.updateMapUrl(this.DEFAULT_LAT, this.DEFAULT_LNG, this.DEFAULT_ZOOM);
  }

  // Funciones del historial
  addToHistory(item: GeocodeResult) {
    const historyItem: HistoryItem = {
      ...item,
      timestamp: Date.now()
    };
    
    this.searchHistory.unshift(historyItem);
    this.searchHistory = this.searchHistory.slice(0, this.MAX_HISTORY);
    this.saveSearchHistory();
  }

  selectFromHistory(item: HistoryItem) {
    this.address = item.address;
    this.result = item;
    this.updateMapUrl(item.latitude, item.longitude, 15);
  }

  clearHistory() {
    this.searchHistory = [];
    this.saveSearchHistory();
  }

  trackByHistory(index: number, item: HistoryItem): number {
    return item.timestamp;
  }

  private loadSearchHistory() {
    try {
      const saved = localStorage.getItem(this.HISTORY_KEY);
      if (saved) {
        this.searchHistory = JSON.parse(saved);
      }
    } catch (error) {
      console.error('Error loading search history:', error);
    }
  }

  private saveSearchHistory() {
    try {
      localStorage.setItem(this.HISTORY_KEY, JSON.stringify(this.searchHistory));
    } catch (error) {
      console.error('Error saving search history:', error);
    }
  }

  // Funciones adicionales
  exportLocation() {
    if (!this.result) return;
    
    const text = `${this.result.address}\nCoordenadas: ${this.result.latitude}, ${this.result.longitude}`;
    
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        // Mostrar mensaje de éxito
        this.showMessage('Coordenadas copiadas al portapapeles');
      }).catch(() => {
        this.fallbackCopyToClipboard(text);
      });
    } else {
      this.fallbackCopyToClipboard(text);
    }
  }

  private fallbackCopyToClipboard(text: string) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
      document.execCommand('copy');
      this.showMessage('Coordenadas copiadas al portapapeles');
    } catch (err) {
      this.error = 'No se pudo copiar al portapapeles';
    }
    
    document.body.removeChild(textArea);
  }

  shareLocation() {
    if (!this.result) return;
    
    const url = `https://www.openstreetmap.org/?mlat=${this.result.latitude}&mlon=${this.result.longitude}&zoom=15`;
    
    if (navigator.share) {
      navigator.share({
        title: 'Ubicación compartida',
        text: this.result.address,
        url: url
      }).catch(() => {
        this.fallbackShareLocation(url);
      });
    } else {
      this.fallbackShareLocation(url);
    }
  }

  private fallbackShareLocation(url: string) {
    this.exportLocation();
    this.showMessage('URL copiada al portapapeles');
  }

  calculateDistance() {
    if (!this.result) return;
    
    // Función básica para calcular distancia desde Bogotá
    const bogotaLat = 4.6097;
    const bogotaLng = -74.0817;
    
    const distance = this.getDistanceFromLatLonInKm(
      bogotaLat, bogotaLng,
      this.result.latitude, this.result.longitude
    );
    
    this.showMessage(`Distancia desde Bogotá: ${distance.toFixed(2)} km`);
  }

  private getDistanceFromLatLonInKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
    const R = 6371; // Radio de la tierra en km
    const dLat = this.deg2rad(lat2 - lat1);
    const dLon = this.deg2rad(lon2 - lon1);
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) * 
      Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }

  private deg2rad(deg: number): number {
    return deg * (Math.PI/180);
  }

  private showMessage(message: string) {
    // Crear un mensaje temporal
    const messageDiv = document.createElement('div');
    messageDiv.className = 'temp-message';
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #28a745;
      color: white;
      padding: 10px 20px;
      border-radius: 5px;
      z-index: 1000;
      font-weight: bold;
    `;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
      if (document.body.contains(messageDiv)) {
        document.body.removeChild(messageDiv);
      }
    }, 3000);
  }
}
