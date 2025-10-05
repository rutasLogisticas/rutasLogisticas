# 📚 Documentación de la API - Sistema de Rutas Logísticas

Documentación completa de la API REST del sistema de gestión logística.

## 🌐 Base URL

```
http://localhost:8000
```

## 📋 Endpoints Disponibles

### Health Check

#### GET /health
Verifica el estado de la aplicación.

**Respuesta:**
```json
{
  "status": "ok",
  "message": "Aplicación funcionando correctamente"
}
```

#### GET /
Información básica de la API.

**Respuesta:**
```json
{
  "message": "Sistema de Rutas Logísticas API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

## 🚛 Vehículos

### GET /api/v1/vehicles
Lista todos los vehículos.

**Respuesta:**
```json
[
  {
    "id": 1,
    "license_plate": "ABC-123",
    "brand": "Toyota",
    "model": "Hilux",
    "vehicle_type": "camioneta",
    "status": "disponible"
  }
]
```

### POST /api/v1/vehicles
Crea un nuevo vehículo.

**Body:**
```json
{
  "license_plate": "ABC-1234",
  "brand": "Toyota",
  "model": "Hilux",
  "year": 2022,
  "vehicle_type": "camioneta",
  "status": "disponible"
}
```

**Respuesta:**
```json
{
  "id": 4,
  "license_plate": "ABC-1234",
  "brand": "Toyota",
  "model": "Hilux",
  "year": 2022,
  "vehicle_type": "camioneta",
  "status": "disponible",
  "is_available": true
}
```

### GET /api/v1/vehicles/{id}
Obtiene un vehículo por ID.

**Respuesta:**
```json
{
  "id": 1,
  "license_plate": "ABC-123",
  "brand": "Toyota",
  "model": "Hilux",
  "year": 2020,
  "vehicle_type": "camioneta",
  "status": "disponible",
  "is_available": true
}
```

## 👨‍💼 Conductores

### GET /api/v1/drivers
Lista todos los conductores.

**Respuesta:**
```json
[
  {
    "id": 1,
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "juan.perez@email.com",
    "license_type": "B",
    "status": "disponible"
  }
]
```

### POST /api/v1/drivers
Crea un nuevo conductor.

**Body:**
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan.perez@empresa.com",
  "phone": "3001234567",
  "document_number": "12345678",
  "license_type": "B",
  "status": "disponible"
}
```

**Respuesta:**
```json
{
  "id": 4,
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan.perez@empresa.com",
  "phone": "3001234567",
  "document_number": "12345678",
  "license_type": "B",
  "status": "disponible",
  "is_available": true
}
```

### GET /api/v1/drivers/{id}
Obtiene un conductor por ID.

### GET /api/v1/drivers/available/
Lista conductores disponibles.

## 🏢 Clientes

### GET /api/v1/clients
Lista todos los clientes.

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Empresa ABC",
    "email": "contacto@empresaabc.com",
    "phone": "6012345678",
    "client_type": "empresa",
    "status": "activo"
  }
]
```

### POST /api/v1/clients
Crea un nuevo cliente.

**Body:**
```json
{
  "name": "Empresa ABC S.A.",
  "email": "contacto@empresaabc.com",
  "phone": "6012345678",
  "company": "ABC S.A.S.",
  "client_type": "empresa",
  "status": "activo"
}
```

### GET /api/v1/clients/{id}
Obtiene un cliente por ID.

### GET /api/v1/clients/company/{company}
Lista clientes por empresa.

## 📍 Direcciones

### GET /api/v1/addresses
Lista todas las direcciones.

**Respuesta:**
```json
[
  {
    "id": 1,
    "client_id": 1,
    "street": "Calle 100 #15-20",
    "city": "Bogotá",
    "state": "Cundinamarca",
    "address_type": "principal"
  }
]
```

### POST /api/v1/addresses
Crea una nueva dirección.

**Body:**
```json
{
  "client_id": 1,
  "street": "Calle 100 #15-20",
  "city": "Bogotá",
  "state": "Cundinamarca",
  "postal_code": "110111",
  "country": "Colombia",
  "address_type": "principal",
  "is_primary": true
}
```

### GET /api/v1/addresses/{id}
Obtiene una dirección por ID.

### GET /api/v1/addresses/client/{client_id}
Lista direcciones de un cliente.

### GET /api/v1/addresses/city/{city}
Lista direcciones por ciudad.

## 📊 Códigos de Estado HTTP

- **200**: OK - Operación exitosa
- **201**: Created - Recurso creado exitosamente
- **400**: Bad Request - Datos inválidos
- **404**: Not Found - Recurso no encontrado
- **500**: Internal Server Error - Error interno del servidor

## 🔍 Ejemplos de Uso

### Flujo Completo: Crear Cliente y Dirección

```bash
# 1. Crear cliente
curl -X POST "http://localhost:8000/api/v1/clients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Empresa Test",
    "email": "test@empresa.com",
    "phone": "6012345678",
    "client_type": "empresa",
    "status": "activo"
  }'

# 2. Crear dirección para el cliente (ID: 4)
curl -X POST "http://localhost:8000/api/v1/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 4,
    "street": "Av. Test 123",
    "city": "Bogotá",
    "state": "Cundinamarca",
    "postal_code": "110111",
    "country": "Colombia",
    "address_type": "principal",
    "is_primary": true
  }'
```

### Consultar Recursos Disponibles

```bash
# Vehículos disponibles
curl "http://localhost:8000/api/v1/vehicles"

# Conductores disponibles
curl "http://localhost:8000/api/v1/drivers/available/"

# Direcciones de un cliente
curl "http://localhost:8000/api/v1/addresses/client/1"
```

## 🛠️ Validaciones

### Vehículos
- **license_plate**: Requerido, único, máximo 20 caracteres
- **brand**: Requerido, máximo 100 caracteres
- **model**: Requerido, máximo 100 caracteres
- **year**: Requerido, número entero
- **vehicle_type**: Requerido, máximo 20 caracteres
- **status**: Opcional, por defecto "disponible"

### Conductores
- **first_name**: Requerido, máximo 100 caracteres
- **last_name**: Requerido, máximo 100 caracteres
- **email**: Requerido, único, máximo 255 caracteres
- **phone**: Requerido, máximo 20 caracteres
- **document_number**: Requerido, único, máximo 20 caracteres
- **license_type**: Requerido, máximo 10 caracteres

### Clientes
- **name**: Requerido, máximo 200 caracteres
- **email**: Requerido, único, máximo 255 caracteres
- **phone**: Requerido, máximo 20 caracteres
- **company**: Opcional, máximo 200 caracteres
- **client_type**: Opcional, por defecto "individual"

### Direcciones
- **client_id**: Requerido, debe existir en la tabla clients
- **street**: Requerido, máximo 200 caracteres
- **city**: Requerido, máximo 100 caracteres
- **state**: Requerido, máximo 100 caracteres
- **postal_code**: Requerido, máximo 20 caracteres
- **country**: Opcional, por defecto "Colombia"
- **address_type**: Opcional, por defecto "principal"
- **is_primary**: Opcional, por defecto false

## 📖 Documentación Interactiva

La API incluye documentación interactiva disponible en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Con Postman
Importa la colección desde `postman/Rutas_Logisticas_API.postman_collection.json` para pruebas completas.

### Con cURL
Ejemplos básicos incluidos en esta documentación.

### Con Python
```python
import requests

# Listar vehículos
response = requests.get("http://localhost:8000/api/v1/vehicles")
vehicles = response.json()

# Crear conductor
data = {
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "juan@test.com",
    "phone": "3001234567",
    "document_number": "12345678",
    "license_type": "B"
}
response = requests.post("http://localhost:8000/api/v1/drivers", json=data)
```

---

**¡API lista para usar! 🚀**