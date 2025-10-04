# Colección Postman - Rutas Logísticas

Esta colección de Postman contiene todos los endpoints necesarios para probar la API del sistema Rutas Logísticas.

## Contenido de la Colección

### Health & Info
- **Health Check**: Verificar estado del servidor
- **API Info**: Información detallada de la API
- **Root Endpoint**: Endpoint raíz del sistema

### Vehículos
- **Crear Vehículo**: Crear un nuevo vehículo
- **Listar Vehículos**: Obtener lista paginada de vehículos
- **Obtener Vehículo**: Obtener vehículo por ID
- **Actualizar Vehículo**: Actualizar información del vehículo
- **Actualizar Estado**: Cambiar estado del vehículo
- **Buscar Vehículos**: Búsqueda por múltiples campos
- **Estadísticas**: Estadísticas de vehículos

### Conductores
- **Crear Conductor**: Crear un nuevo conductor
- **Listar Conductores**: Obtener lista paginada de conductores
- **Obtener Conductor**: Obtener conductor por ID
- **Actualizar Conductor**: Actualizar información del conductor
- **Alertas Licencias**: Conductores con licencias próximas a expirar
- **Estadísticas**: Estadísticas de conductores

### Clientes
- **Crear Cliente**: Crear un nuevo cliente
- **Listar Clientes**: Obtener lista paginada de clientes
- **Obtener Cliente**: Obtener cliente por ID
- **Actualizar Cliente**: Actualizar información del cliente
- **Actualizar Prioridad**: Cambiar prioridad del cliente
- **Estadísticas**: Estadísticas de clientes

### Direcciones
- **Crear Dirección**: Crear una nueva dirección
- **Listar Direcciones**: Obtener lista paginada de direcciones
- **Obtener Dirección**: Obtener dirección por ID
- **Dirección Principal**: Obtener dirección principal del cliente
- **Direcciones de Entrega**: Obtener direcciones disponibles para entrega
- **Actualizar Coordenadas**: Actualizar coordenadas geográficas
- **Estadísticas**: Estadísticas de direcciones

### Tests de Flujo Completo
- **Flujo Completo - Crear Todo**: Crear cliente, dirección, vehículo y conductor
- **Flujo Completo - Consultar Todo**: Consultar todos los recursos creados

## Cómo Usar la Colección

### 1. Importar en Postman

1. Abre Postman
2. Haz clic en "Import" en la esquina superior izquierda
3. Selecciona los archivos:
   - `Rutas_Logisticas_API.postman_collection.json`
   - `Rutas_Logisticas_Environment.postman_environment.json`
4. Haz clic en "Import"

### 2. Configurar Variables de Entorno

1. En Postman, ve a la pestaña "Environments"
2. Selecciona "Rutas Logísticas Environment"
3. Verifica que `baseUrl` esté configurado como `http://localhost:8000`
4. Si tu servidor está en otro puerto, actualiza la variable `baseUrl`

### 3. Iniciar el Servidor

```bash
# Con Docker
docker-compose up -d

# Manual
uvicorn app.main:app --reload
```

### 4. Ejecutar Tests

#### Test Individual
1. Selecciona cualquier endpoint de la colección
2. Haz clic en "Send"
3. Verifica la respuesta

#### Test de Flujo Completo
1. Ve a la carpeta "Tests de Flujo Completo"
2. Selecciona "Flujo Completo - Crear Todo"
3. Haz clic en "Run" en la carpeta para ejecutar todos los tests
4. Verifica que todos los tests pasen

## Variables Automáticas

La colección usa variables que se actualizan automáticamente:

- **`vehicleId`**: Se actualiza al crear un vehículo
- **`driverId`**: Se actualiza al crear un conductor
- **`clientId`**: Se actualiza al crear un cliente
- **`addressId`**: Se actualiza al crear una dirección

Estas variables permiten que los tests posteriores usen los IDs correctos automáticamente.

## Configuraciones Adicionales

### Cambiar URL Base

Si tu servidor está en otra dirección:

1. Ve a "Environments" → "Rutas Logísticas Environment"
2. Cambia el valor de `baseUrl` a tu URL (ej: `http://192.168.1.100:8000`)

### Headers Personalizados

Para agregar headers personalizados:

1. Selecciona un endpoint
2. Ve a la pestaña "Headers"
3. Agrega tus headers personalizados

### Autenticación

Si en el futuro se implementa autenticación:

1. Ve a la pestaña "Authorization"
2. Selecciona el tipo de autenticación
3. Configura las credenciales

## Ejemplos de Uso

### Crear un Vehículo Completo

```json
{
  "license_plate": "ABC-1234",
  "brand": "Toyota",
  "model": "Hilux",
  "year": 2022,
  "color": "Blanco",
  "vehicle_type": "camioneta",
  "capacity_weight": 1000.0,
  "capacity_volume": 2.5,
  "fuel_type": "Diesel",
  "fuel_consumption": 8.5,
  "notes": "Vehículo en excelente estado"
}
```

### Crear un Cliente con Información Completa

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
  "discount_percentage": 5.0,
  "is_priority": true
}
```

### Crear una Dirección con Coordenadas

```json
{
  "client_id": 1,
  "address_type": "oficina",
  "address_line1": "Av. Amazonas N12-34",
  "address_line2": "Edificio Plaza Central",
  "neighborhood": "Centro",
  "city": "Quito",
  "state": "Pichincha",
  "country": "Ecuador",
  "postal_code": "170150",
  "latitude": -0.2298500,
  "longitude": -78.5249500,
  "contact_name": "Ana López",
  "contact_phone": "+593991234567",
  "is_primary": true
}
```

## Tests Automáticos

La colección incluye tests automáticos que verifican:

- **Códigos de estado HTTP** correctos
- **Estructura de respuestas** JSON
- **Variables automáticas** se actualizan correctamente
- **Validaciones** de campos requeridos

### Ver Tests Automáticos

1. Selecciona cualquier endpoint
2. Ve a la pestaña "Tests"
3. Verás los tests automáticos configurados

## Troubleshooting

### Error de Conexión

```
Error: connect ECONNREFUSED 127.0.0.1:8000
```

**Solución**: Verifica que el servidor esté ejecutándose en `http://localhost:8000`

### Error 404

```
404 Not Found
```

**Solución**: Verifica que la URL base esté configurada correctamente

### Error de Validación

```
422 Unprocessable Entity
```

**Solución**: Revisa los datos enviados en el body de la petición

### Variables No Actualizadas

Si las variables no se actualizan automáticamente:

1. Verifica que los tests estén habilitados
2. Revisa la consola de Postman para errores
3. Ejecuta los endpoints en orden

## Recursos Adicionales

- [Documentación de la API](http://localhost:8000/docs)
- [Documentación Técnica](../docs/README.md)
- [Guía de Despliegue](../docs/DEPLOYMENT.md)

## Contribución

Para agregar nuevos endpoints:

1. Agrega el endpoint en la colección
2. Configura los tests automáticos
3. Actualiza esta documentación
4. Haz commit de los cambios

---

**Disfruta probando la API de Rutas Logísticas!**
