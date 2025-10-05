# 🚚 Sistema de Rutas Logísticas

Un sistema de gestión logística simple y eficiente desarrollado con FastAPI, diseñado para la administración de vehículos, conductores, clientes y direcciones.

## 🎯 Características

- **API REST completa** con FastAPI
- **Base de datos MySQL** con SQLAlchemy ORM
- **Arquitectura limpia** con separación de responsabilidades
- **Dockerizado** para fácil despliegue
- **Documentación automática** con Swagger/OpenAPI
- **Validación de datos** con Pydantic
- **Código simplificado** y fácil de mantener

## 📋 Módulos del Sistema

### 🚛 Vehículos
- Gestión de flota vehicular
- Tipos: camioneta, furgón, motocicleta, etc.
- Estados: disponible, en ruta, mantenimiento
- Información básica: placa, marca, modelo, año

### 👨‍💼 Conductores
- Gestión de personal conductor
- Información personal y profesional
- Tipos de licencia (A, B, C)
- Estados de disponibilidad

### 🏢 Clientes
- Gestión de clientes individuales y empresas
- Información de contacto
- Clasificación por tipo
- Estados de actividad

### 📍 Direcciones
- Gestión de direcciones de clientes
- Relación con clientes
- Tipos: principal, entrega, oficina
- Información geográfica completa

## 🚀 Instalación y Uso

### Requisitos Previos
- Docker y Docker Compose
- Git

### Instalación Rápida

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd rutasLogisticas
   ```

2. **Ejecutar con Docker**
   ```bash
   docker-compose up -d
   ```

3. **Verificar que funciona**
   ```bash
   curl http://localhost:8000/health
   ```

### Acceso a la Aplicación

- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Base de datos**: localhost:3307 (usuario: root, contraseña: 1234)

## 📚 API Endpoints

### Health Check
- `GET /health` - Estado de la aplicación
- `GET /` - Información básica de la API

### Vehículos
- `GET /api/v1/vehicles` - Listar vehículos
- `POST /api/v1/vehicles` - Crear vehículo
- `GET /api/v1/vehicles/{id}` - Obtener vehículo

### Conductores
- `GET /api/v1/drivers` - Listar conductores
- `POST /api/v1/drivers` - Crear conductor
- `GET /api/v1/drivers/{id}` - Obtener conductor
- `GET /api/v1/drivers/available/` - Conductores disponibles

### Clientes
- `GET /api/v1/clients` - Listar clientes
- `POST /api/v1/clients` - Crear cliente
- `GET /api/v1/clients/{id}` - Obtener cliente
- `GET /api/v1/clients/company/{company}` - Clientes por empresa

### Direcciones
- `GET /api/v1/addresses` - Listar direcciones
- `POST /api/v1/addresses` - Crear dirección
- `GET /api/v1/addresses/{id}` - Obtener dirección
- `GET /api/v1/addresses/client/{client_id}` - Direcciones por cliente
- `GET /api/v1/addresses/city/{city}` - Direcciones por ciudad

## 🧪 Testing con Postman

El proyecto incluye una colección de Postman completa en la carpeta `postman/`:

1. Importar `Rutas_Logisticas_API.postman_collection.json`
2. Importar `Rutas_Logisticas_Environment.postman_environment.json`
3. Ejecutar los tests de flujo completo

## 🏗️ Arquitectura

```
app/
├── api/                 # Capa de API REST
│   ├── dependencies.py  # Dependencias de FastAPI
│   └── routes/         # Rutas de endpoints
├── core/               # Configuración central
│   ├── base.py         # Base de SQLAlchemy
│   ├── config.py       # Configuración de la app
│   └── database.py     # Gestión de base de datos
├── models/             # Modelos de datos (SQLAlchemy)
├── repositories/       # Capa de acceso a datos
├── schemas/            # Esquemas de validación (Pydantic)
├── services/           # Lógica de negocio
└── main.py            # Punto de entrada de la aplicación
```

## 🔧 Configuración

### Variables de Entorno

Copia `env.example` a `.env` y ajusta según tu entorno:

```env
# Base de datos
DB_HOST=mysql
DB_PORT=3306
DB_NAME=rutas_logisticas
DB_USER=root
DB_PASSWORD=1234

# Aplicación
DEBUG=True
LOG_LEVEL=INFO
```

### Docker Compose

El archivo `docker-compose.yml` incluye:
- **app**: Aplicación FastAPI
- **mysql**: Base de datos MySQL
- **redis**: Cache (opcional)

## 📊 Datos de Ejemplo

El sistema incluye datos de ejemplo:
- 3 vehículos (Toyota Hilux, Ford Transit, Honda CB250)
- 3 conductores (Juan Pérez, María García, Carlos López)
- 3 clientes (Empresa ABC, Ana Martínez, Distribuidora XYZ)
- 3 direcciones (Bogotá, Medellín, Cali)

## 🛠️ Desarrollo

### Estructura del Proyecto

- **Modelos**: Definen la estructura de datos
- **Repositorios**: Acceso a la base de datos
- **Servicios**: Lógica de negocio
- **Schemas**: Validación de entrada/salida
- **Rutas**: Endpoints de la API

### Principios Aplicados

- **SRP**: Single Responsibility Principle
- **DRY**: Don't Repeat Yourself
- **Separación de capas**: API, Servicios, Repositorios, Modelos
- **Código limpio**: Simple y mantenible

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto, contacta al equipo de desarrollo.

---

**Desarrollado con ❤️ para la gestión logística eficiente**