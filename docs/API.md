# API Documentation - Rutas Logísticas

## Introducción

Esta documentación describe la API REST del sistema Rutas Logísticas. La API está construida con FastAPI y proporciona endpoints para la gestión completa de vehículos, conductores, clientes y direcciones.

## Información General

- **Base URL**: `http://localhost:8000/api/v1`
- **Formato**: JSON
- **Autenticación**: No implementada (para futuras versiones)
- **Versión**: 1.0.0

## Endpoints de Vehículos

### Listar Vehículos

```http
GET /api/v1/vehicles
```

**Parámetros de consulta:**
- `page` (int, opcional): Número de página (default: 1)
- `size` (int, opcional): Tamaño de página (default: 10, max: 100)
- `vehicle_type` (string, opcional): Filtrar por tipo de vehículo
- `status` (string, opcional): Filtrar por estado
- `available_only` (boolean, opcional): Solo vehículos disponibles

**Respuesta:**
```json
{
  "items": [
    {
      "id": 1,
      "license_plate": "ABC-1234",
      "brand": "Toyota",
      "model": "Hilux",
      "year": 2022,
      "vehicle_type": "camioneta",
      "status": "disponible",
      "is_available": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

### Crear Vehículo

```http
POST /api/v1/vehicles
```

**Cuerpo de la petición:**
```json
{
  "license_plate": "XYZ-5678",
  "brand": "Mercedes",
  "model": "Sprinter",
  "year": 2021,
  "color": "Azul",
  "vehicle_type": "furgon",
  "capacity_weight": 3500.0,
  "capacity_volume": 12.0,
  "fuel_type": "Diesel",
  "fuel_consumption": 7.2
}
```

**Respuesta (201):**
```json
{
  "id": 2,
  "license_plate": "XYZ-5678",
  "brand": "Mercedes",
  "model": "Sprinter",
  "year": 2021,
  "color": "Azul",
  "vehicle_type": "furgon",
  "status": "disponible",
  "capacity_weight": 3500.0,
  "capacity_volume": 12.0,
  "fuel_type": "Diesel",
  "fuel_consumption": 7.2,
  "is_available": true,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Obtener Vehículo

```http
GET /api/v1/vehicles/{vehicle_id}
```

### Actualizar Vehículo

```http
PUT /api/v1/vehicles/{vehicle_id}
```

### Eliminar Vehículo

```http
DELETE /api/v1/vehicles/{vehicle_id}
```

### Actualizar Estado del Vehículo

```http
PATCH /api/v1/vehicles/{vehicle_id}/status
```

**Cuerpo de la petición:**
```json
{
  "status": "en_ruta"
}
```

### Buscar Vehículos

```http
POST /api/v1/vehicles/search?query=camioneta
```

## Endpoints de Conductores

### Listar Conductores

```http
GET /api/v1/drivers
```

**Parámetros de consulta:**
- `page` (int, opcional): Número de página
- `size` (int, opcional): Tamaño de página
- `license_type` (string, opcional): Tipo de licencia
- `status` (string, opcional): Estado del conductor
- `available_only` (boolean, opcional): Solo conductores disponibles

### Crear Conductor

```http
POST /api/v1/drivers
```

**Cuerpo de la petición:**
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan.perez@empresa.com",
  "phone": "+593991234567",
  "document_type": "DNI",
  "document_number": "1234567890",
  "license_type": "C",
  "license_number": "LIC123456",
  "license_expiry": "2025-12-31"
}
```

### Obtener Conductor

```http
GET /api/v1/drivers/{driver_id}
```

### Actualizar Conductor

```http
PUT /api/v1/drivers/{driver_id}
```

### Eliminar Conductor

```http
DELETE /api/v1/drivers/{driver_id}
```

### Alertas de Licencias

```http
GET /api/v1/drivers/alerts/license-expiry?days_ahead=30
```

## Endpoints de Clientes

### Listar Clientes

```http
GET /api/v1/clients
```

**Parámetros de consulta:**
- `page` (int, opcional): Número de página
- `size` (int, opcional): Tamaño de página
- `client_type` (string, opcional): Tipo de cliente
- `status` (string, opcional): Estado del cliente
- `city` (string, opcional): Ciudad
- `priority_only` (boolean, opcional): Solo clientes prioritarios
- `active_only` (boolean, opcional): Solo clientes activos

### Crear Cliente

```http
POST /api/v1/clients
```

**Cuerpo de la petición:**
```json
{
  "name": "Empresa ABC S.A.",
  "client_type": "empresa",
  "email": "contacto@empresaabc.com",
  "phone": "+593221234567",
  "city": "Quito",
  "state": "Pichincha",
  "contact_person": "Ana López",
  "contact_email": "ana.lopez@empresaabc.com",
  "credit_limit": 10000.0,
  "payment_terms": 30,
  "discount_percentage": 5.0
}
```

### Obtener Cliente

```http
GET /api/v1/clients/{client_id}
```

### Actualizar Cliente

```http
PUT /api/v1/clients/{client_id}
```

### Eliminar Cliente

```http
DELETE /api/v1/clients/{client_id}
```

### Actualizar Prioridad del Cliente

```http
PATCH /api/v1/clients/{client_id}/priority
```

**Cuerpo de la petición:**
```json
{
  "is_priority": true
}
```

### Buscar Clientes por Tags

```http
GET /api/v1/clients/by-tags/{tag}
```

## Endpoints de Direcciones

### Listar Direcciones

```http
GET /api/v1/addresses
```

**Parámetros de consulta:**
- `page` (int, opcional): Número de página
- `size` (int, opcional): Tamaño de página
- `client_id` (int, opcional): ID del cliente
- `address_type` (string, opcional): Tipo de dirección
- `city` (string, opcional): Ciudad
- `delivery_available` (boolean, opcional): Disponible para entrega

### Crear Dirección

```http
POST /api/v1/addresses
```

**Cuerpo de la petición:**
```json
{
  "client_id": 1,
  "address_type": "oficina",
  "address_line1": "Av. Amazonas N12-34",
  "city": "Quito",
  "state": "Pichincha",
  "country": "Ecuador",
  "latitude": -0.2298500,
  "longitude": -78.5249500,
  "contact_name": "Ana López",
  "contact_phone": "+593991234567",
  "is_primary": true
}
```

### Obtener Dirección

```http
GET /api/v1/addresses/{address_id}
```

### Actualizar Dirección

```http
PUT /api/v1/addresses/{address_id}
```

### Eliminar Dirección

```http
DELETE /api/v1/addresses/{address_id}
```

### Establecer Dirección Principal

```http
PATCH /api/v1/addresses/{address_id}/primary
```

### Obtener Dirección Principal del Cliente

```http
GET /api/v1/addresses/client/{client_id}/primary
```

### Obtener Direcciones de Entrega del Cliente

```http
GET /api/v1/addresses/client/{client_id}/delivery
```

### Actualizar Coordenadas

```http
PATCH /api/v1/addresses/{address_id}/coordinates
```

**Cuerpo de la petición:**
```json
{
  "latitude": -0.2298500,
  "longitude": -78.5249500
}
```

## Endpoints de Estadísticas

### Estadísticas de Vehículos

```http
GET /api/v1/vehicles/statistics/overview
```

**Respuesta:**
```json
{
  "total_vehicles": 25,
  "available_vehicles": 20,
  "status_distribution": {
    "disponible": 20,
    "en_ruta": 3,
    "mantenimiento": 2,
    "fuera_servicio": 0
  },
  "type_distribution": {
    "camion": 5,
    "furgon": 8,
    "camioneta": 10,
    "motocicleta": 2
  }
}
```

### Estadísticas de Conductores

```http
GET /api/v1/drivers/statistics/overview
```

### Estadísticas de Clientes

```http
GET /api/v1/clients/statistics/overview
```

### Estadísticas de Direcciones

```http
GET /api/v1/addresses/statistics/overview?client_id=1
```

## Endpoints de Información

### Información de la API

```http
GET /api/v1/info
```

### Estado de Salud

```http
GET /health
```

### Endpoint Raíz

```http
GET /
```

## Códigos de Estado HTTP

- `200 OK`: Petición exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Error en la petición
- `404 Not Found`: Recurso no encontrado
- `422 Unprocessable Entity`: Error de validación
- `500 Internal Server Error`: Error interno del servidor

## Manejo de Errores

### Formato de Error

```json
{
  "error": "Descripción del error",
  "detail": "Detalles adicionales (solo en modo debug)",
  "status_code": 400,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Errores de Validación

```json
{
  "error": "Error de validación",
  "detail": [
    {
      "loc": ["body", "license_plate"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ],
  "status_code": 422
}
```

## Filtros y Búsquedas

### Filtros Avanzados

```http
POST /api/v1/vehicles/filter/capacity
```

**Cuerpo de la petición:**
```json
{
  "min_weight": 1000.0,
  "min_volume": 2.0,
  "vehicle_type": "furgon",
  "page": 1,
  "size": 10
}
```

### Búsquedas por Texto

```http
POST /api/v1/vehicles/search?query=Toyota
```

La búsqueda se realiza en múltiples campos:
- **Vehículos**: placa, marca, modelo, color
- **Conductores**: nombre, apellido, email, documento, licencia
- **Clientes**: nombre, email, documento fiscal, contacto
- **Direcciones**: dirección, ciudad, barrio, código postal

## Paginación

Todos los endpoints de listado soportan paginación:

```json
{
  "items": [...],
  "total": 150,
  "page": 2,
  "size": 10,
  "pages": 15
}
```

## Ordenamiento

Los resultados se ordenan por defecto por fecha de creación descendente. Para ordenamiento personalizado, usar el parámetro `sort`:

```http
GET /api/v1/vehicles?sort=license_plate,asc
GET /api/v1/vehicles?sort=year,desc
```

## Rate Limiting

- **Límite**: 1000 requests por hora por IP
- **Headers de respuesta**:
  - `X-RateLimit-Limit`: Límite total
  - `X-RateLimit-Remaining`: Requests restantes
  - `X-RateLimit-Reset`: Timestamp de reset

## Autenticación (Futuro)

Para futuras versiones se implementará:

- **JWT Tokens** para autenticación
- **OAuth2** para autorización
- **Roles y permisos** para control de acceso

## SDKs y Bibliotecas

### Python

```python
import requests

# Ejemplo de uso
response = requests.get('http://localhost:8000/api/v1/vehicles')
vehicles = response.json()
```

### JavaScript/TypeScript

```typescript
// Ejemplo con fetch
const response = await fetch('http://localhost:8000/api/v1/vehicles');
const vehicles = await response.json();
```

### cURL

```bash
# Ejemplo básico
curl -X GET "http://localhost:8000/api/v1/vehicles" \
     -H "Accept: application/json"

# Con parámetros
curl -X GET "http://localhost:8000/api/v1/vehicles?page=1&size=20" \
     -H "Accept: application/json"
```

## Changelog

### v1.0.0 (2024-01-01)
- ✅ CRUD completo para vehículos
- ✅ CRUD completo para conductores
- ✅ CRUD completo para clientes
- ✅ Gestión de direcciones
- ✅ Búsqueda y filtrado
- ✅ Estadísticas y reportes
- ✅ Documentación automática

### Próximas Versiones
- 🔄 Autenticación y autorización
- 🔄 Notificaciones en tiempo real
- 🔄 Integración con mapas
- 🔄 Optimización de rutas
- 🔄 Dashboard web
