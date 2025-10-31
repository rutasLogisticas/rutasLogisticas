import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GeocodingService, GeocodeResult } from '../../services/geocoding.service';
import { ApiService } from '../../services/api';
import { SanitizeUrlPipe } from '../../pipes/sanitize-url.pipe';
import { Subscription } from 'rxjs';

interface HistoryItem extends GeocodeResult {
  timestamp: number;
}

interface OrderRoute {
  order: any;
  route: {
    origin: string;
    destination: string;
    distance_text: string;
    duration_text: string;
    steps: any[];
  };
  estimated_delivery_time: string;
  route_distance: string;
  route_duration: string;
  polyline: string;
}

interface Order {
  id: number;
  order_number: string;
  origin_address: string;
  destination_address: string;
  origin_city: string;
  destination_city: string;
  status: string;
  priority: string;
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
  
  // Nuevas propiedades para rutas de pedidos
  orders: Order[] = [];
  selectedOrderId: number | null = null;
  orderRoute: OrderRoute | null = null;
  routeLoading = false;
  showRouteMode = false;
  routeMode: string = 'driving';
  useGoogleMaps: boolean = true; // Usar Google Maps para rutas
  
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

  constructor(
    private geocodingService: GeocodingService,
    private apiService: ApiService
  ) {}

  ngOnInit() {
    this.loadSearchHistory();
    this.loadOrders();
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

  // Métodos para rutas de pedidos
  loadOrders() {
    this.apiService.getOrders().subscribe({
      next: (orders: any[]) => {
        this.orders = orders.slice(0, 20); // Limitar a 20 pedidos para mejor rendimiento
      },
      error: (err) => {
        console.error('Error cargando pedidos:', err);
        this.error = 'Error cargando pedidos';
      }
    });
  }

  selectOrder(orderId: number) {
    this.selectedOrderId = orderId;
    this.loadOrderRoute(orderId);
  }

  loadOrderRoute(orderId: number) {
    this.routeLoading = true;
    this.error = null;
    this.orderRoute = null;

    this.apiService.getOrderRoute(orderId, this.routeMode).subscribe({
      next: async (route: OrderRoute) => {
        this.orderRoute = route;
        // Usar el nuevo método con geocodificación para mostrar ambos puntos
        await this.showRouteOnMapWithGeocoding(route);
        this.routeLoading = false;
      },
      error: (err) => {
        console.error('Error cargando ruta:', err);
        this.error = 'Error calculando ruta del pedido';
        this.routeLoading = false;
      }
    });
  }

  showRouteOnMap(route: OrderRoute) {
    if (!route.polyline) return;

    // Decodificar polyline para obtener coordenadas
    const coordinates = this.decodePolyline(route.polyline);
    
    if (coordinates.length > 0) {
      // Calcular bounds para centrar el mapa en la ruta
      const bounds = this.calculateBounds(coordinates);
      const centerLat = (bounds.minLat + bounds.maxLat) / 2;
      const centerLng = (bounds.minLng + bounds.maxLng) / 2;
      
      // Actualizar el mapa con la ruta
      this.updateMapUrlWithRoute(centerLat, centerLng, 10, route.polyline);
    }
  }

  async showRouteOnMapWithGeocoding(route: OrderRoute) {
    try {
      // Geocodificar origen y destino para obtener coordenadas precisas
      const originCoords = await this.geocodeAddress(route.route.origin);
      const destCoords = await this.geocodeAddress(route.route.destination);
      
      if (originCoords && destCoords) {
        // Usar Google Maps embebido para mostrar la ruta completa si está habilitado
        if (this.useGoogleMaps) {
          this.updateMapUrlWithGoogleMapsEmbed(
            originCoords.latitude, 
            originCoords.longitude,
            destCoords.latitude, 
            destCoords.longitude,
            route.polyline
          );
        } else {
          // Usar OpenStreetMap con marcadores
          this.updateMapUrlWithRouteMarkers(
            originCoords.latitude, 
            originCoords.longitude,
            destCoords.latitude, 
            destCoords.longitude,
            8
          );
        }
      } else {
        // Fallback: usar el método anterior
        this.showRouteOnMap(route);
      }
    } catch (error) {
      console.error('Error geocodificando direcciones:', error);
      // Fallback: usar el método anterior
      this.showRouteOnMap(route);
    }
  }

  private async geocodeAddress(address: string): Promise<{latitude: number, longitude: number} | null> {
    try {
      const response = await this.geocodingService.geocodeAddress(address).toPromise();
      if (response) {
        return {
          latitude: response.latitude,
          longitude: response.longitude
        };
      }
      return null;
    } catch (error) {
      console.error('Error geocodificando:', error);
      return null;
    }
  }

  updateMapUrlWithRoute(lat: number, lng: number, zoom: number, polyline: string) {
    this.currentZoom = zoom;
    const bbox = this.calculateBBox(lat, lng, zoom);
    
    // Crear URL con polyline para mostrar la ruta
    // Nota: OpenStreetMap no soporta polylines directamente, pero podemos usar marcadores
    this.mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${lat},${lng}`;
  }

  updateMapUrlWithRouteMarkers(originLat: number, originLng: number, destLat: number, destLng: number, zoom: number) {
    this.currentZoom = zoom;
    
    // Calcular bounds para incluir ambos puntos
    const minLat = Math.min(originLat, destLat);
    const maxLat = Math.max(originLat, destLat);
    const minLng = Math.min(originLng, destLng);
    const maxLng = Math.max(originLng, destLng);
    
    // Agregar margen a los bounds
    const latMargin = (maxLat - minLat) * 0.1;
    const lngMargin = (maxLng - minLng) * 0.1;
    
    const bbox = `${minLng - lngMargin},${minLat - latMargin},${maxLng + lngMargin},${maxLat + latMargin}`;
    
    // Crear URL con marcadores para origen y destino
    // Usamos parámetros personalizados para mostrar ambos puntos
    this.mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${originLat},${originLng}&marker=${destLat},${destLng}`;
  }

  updateMapUrlWithCustomRoute(originLat: number, originLng: number, destLat: number, destLng: number, polyline: string) {
    // Usar Google Maps embebido que soporta polylines
    // Calcular el centro entre ambos puntos
    const centerLat = (originLat + destLat) / 2;
    const centerLng = (originLng + destLng) / 2;
    
    // Calcular zoom basado en la distancia
    const distance = this.getDistanceFromLatLonInKm(originLat, originLng, destLat, destLng);
    let zoom = 10;
    if (distance > 1000) zoom = 6;
    else if (distance > 500) zoom = 7;
    else if (distance > 100) zoom = 8;
    else if (distance > 50) zoom = 9;
    else zoom = 10;
    
    this.currentZoom = zoom;
    
    // Crear URL de Google Maps con polyline
    // Usar Google Maps Static API para mostrar la ruta
    const apiKey = 'AIzaSyDfIIPbFtxFmsLEeoe-msMMReXOCPVPBKU'; // Usar la misma API key del backend
    
    // Crear marcadores para origen y destino
    const originMarker = `markers=color:blue|label:O|${originLat},${originLng}`;
    const destMarker = `markers=color:green|label:D|${destLat},${destLng}`;
    
    // Crear polyline para la ruta
    const routePolyline = `path=enc:${polyline}`;
    
    // Construir URL de Google Maps Static API
    this.mapUrl = `https://maps.googleapis.com/maps/api/staticmap?center=${centerLat},${centerLng}&zoom=${zoom}&size=800x600&maptype=roadmap&${originMarker}&${destMarker}&${routePolyline}&key=${apiKey}`;
  }

  updateMapUrlWithGoogleMapsEmbed(originLat: number, originLng: number, destLat: number, destLng: number, polyline: string) {
    // Usar Google Maps embebido interactivo
    const apiKey = 'AIzaSyDfIIPbFtxFmsLEeoe-msMMReXOCPVPBKU';
    
    // Calcular el centro entre ambos puntos
    const centerLat = (originLat + destLat) / 2;
    const centerLng = (originLng + destLng) / 2;
    
    // Calcular zoom basado en la distancia
    const distance = this.getDistanceFromLatLonInKm(originLat, originLng, destLat, destLng);
    let zoom = 10;
    if (distance > 1000) zoom = 6;
    else if (distance > 500) zoom = 7;
    else if (distance > 100) zoom = 8;
    else if (distance > 50) zoom = 9;
    else zoom = 10;
    
    this.currentZoom = zoom;
    
    // Crear URL de Google Maps embebido con JavaScript
    // Usar Google Maps Embed API que soporta polylines
    const embedUrl = `https://www.google.com/maps/embed/v1/directions?key=${apiKey}&origin=${originLat},${originLng}&destination=${destLat},${destLng}&mode=driving`;
    
    this.mapUrl = embedUrl;
  }

  decodePolyline(encoded: string): { lat: number; lng: number }[] {
    const coordinates: { lat: number; lng: number }[] = [];
    let index = 0;
    let lat = 0;
    let lng = 0;

    while (index < encoded.length) {
      let b: number;
      let shift = 0;
      let result = 0;
      
      do {
        b = encoded.charCodeAt(index++) - 63;
        result |= (b & 0x1f) << shift;
        shift += 5;
      } while (b >= 0x20);
      
      const dlat = ((result & 1) ? ~(result >> 1) : (result >> 1));
      lat += dlat;

      shift = 0;
      result = 0;
      
      do {
        b = encoded.charCodeAt(index++) - 63;
        result |= (b & 0x1f) << shift;
        shift += 5;
      } while (b >= 0x20);
      
      const dlng = ((result & 1) ? ~(result >> 1) : (result >> 1));
      lng += dlng;

      coordinates.push({
        lat: lat / 1e5,
        lng: lng / 1e5
      });
    }

    return coordinates;
  }

  calculateBounds(coordinates: { lat: number; lng: number }[]): { minLat: number; maxLat: number; minLng: number; maxLng: number } {
    let minLat = coordinates[0].lat;
    let maxLat = coordinates[0].lat;
    let minLng = coordinates[0].lng;
    let maxLng = coordinates[0].lng;

    coordinates.forEach(coord => {
      minLat = Math.min(minLat, coord.lat);
      maxLat = Math.max(maxLat, coord.lat);
      minLng = Math.min(minLng, coord.lng);
      maxLng = Math.max(maxLng, coord.lng);
    });

    return { minLat, maxLat, minLng, maxLng };
  }

  toggleRouteMode() {
    this.showRouteMode = !this.showRouteMode;
  }

  changeRouteMode() {
    if (this.selectedOrderId) {
      this.loadOrderRoute(this.selectedOrderId);
    }
  }

  clearRoute() {
    this.selectedOrderId = null;
    this.orderRoute = null;
    this.updateMapUrl(this.DEFAULT_LAT, this.DEFAULT_LNG, this.DEFAULT_ZOOM);
  }

  getOrderDisplayText(order: Order): string {
    return `${order.order_number} - ${order.origin_city} → ${order.destination_city}`;
  }

  getStatusColor(status: string): string {
    const colors: { [key: string]: string } = {
      'pendiente': '#ffc107',
      'asignado': '#17a2b8',
      'en_transito': '#007bff',
      'entregado': '#28a745',
      'cancelado': '#dc3545'
    };
    return colors[status] || '#6c757d';
  }

  toggleMapProvider() {
    this.useGoogleMaps = !this.useGoogleMaps;
    
    // Si hay una ruta seleccionada, recargarla con el nuevo proveedor
    if (this.selectedOrderId && this.orderRoute) {
      this.loadOrderRoute(this.selectedOrderId);
    }
  }

  getMapProviderName(): string {
    return this.useGoogleMaps ? 'Google Maps' : 'OpenStreetMap';
  }
}
