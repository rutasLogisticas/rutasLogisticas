# 📚 Documentación Técnica - Sistema de Rutas Logísticas

Documentación técnica completa del sistema de gestión logística simplificado.

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [API Documentation](#api-documentation)
6. [Base de Datos](#base-de-datos)
7. [Despliegue](#despliegue)
8. [Guía de Desarrollo](#guía-de-desarrollo)

## 🎯 Introducción

**Sistema de Rutas Logísticas** es una aplicación REST simple y eficiente para la gestión de flotas vehiculares, conductores, clientes y direcciones. Diseñada con principios de código limpio y arquitectura simple.

### Características Principales

- ✅ **API REST completa** con FastAPI
- ✅ **Base de datos MySQL** con SQLAlchemy ORM
- ✅ **Arquitectura limpia** con separación de responsabilidades
- ✅ **Dockerizado** para fácil despliegue
- ✅ **Documentación automática** con Swagger/OpenAPI
- ✅ **Código simplificado** y fácil de mantener

## 🏗️ Arquitectura del Sistema

### Patrón de Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Routes    │────│   Services      │────│  Repositories   │
│   (FastAPI)     │    │   (Business)    │    │   (Data Access) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Schemas       │    │   Models        │    │   Database      │
│   (Validation)  │    │   (SQLAlchemy)  │    │   (MySQL)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Capas del Sistema

1. **Capa de API** (`app/api/routes/`)
   - Endpoints REST
   - Validación de entrada
   - Manejo de errores

2. **Capa de Servicios** (`app/services/`)
   - Lógica de negocio
   - Validaciones de reglas
   - Orquestación de operaciones

3. **Capa de Repositorios** (`app/repositories/`)
   - Acceso a datos
   - Consultas de base de datos
   - Operaciones CRUD

4. **Capa de Modelos** (`app/models/`)
   - Entidades de dominio
   - Mapeo ORM
   - Relaciones entre entidades

5. **Capa de Esquemas** (`app/schemas/`)
   - Validación de datos
   - Serialización
   - Documentación automática

## 🚀 Instalación y Configuración

### Método Rápido (Docker)

```bash
# 1. Clonar repositorio
git clone <url-del-repositorio>
cd rutasLogisticas

# 2. Ejecutar con Docker
docker-compose up -d

# 3. Verificar funcionamiento
curl http://localhost:8000/health
```

### Método Local

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar base de datos
mysql -u root -p < database/init_mysql.sql

# 3. Configurar variables de entorno
cp env.example .env

# 4. Ejecutar aplicación
uvicorn app.main:app --reload
```

## 📁 Estructura del Proyecto

```
rutasLogisticas/
├── app/                    # Código fuente de la aplicación
│   ├── api/               # Capa de API REST
│   │   ├── routes/        # Endpoints de la API
│   │   └── dependencies.py # Dependencias de FastAPI
│   ├── core/              # Configuración central
│   │   ├── base.py        # Base de SQLAlchemy
│   │   ├── config.py      # Configuración de la app
│   │   └── database.py    # Gestión de base de datos
│   ├── models/            # Modelos de datos (SQLAlchemy)
│   ├── repositories/      # Capa de acceso a datos
│   ├── schemas/           # Esquemas de validación (Pydantic)
│   ├── services/          # Lógica de negocio
│   └── main.py           # Punto de entrada de la aplicación
├── database/              # Scripts de base de datos
│   └── init_mysql.sql    # Inicialización de MySQL
├── docs/                 # Documentación
│   ├── API.md           # Documentación de la API
│   ├── DEPLOYMENT.md    # Guía de despliegue
│   └── README.md        # Este archivo
├── postman/             # Colección de Postman
│   └── Rutas_Logisticas_API.postman_collection.json
├── docker-compose.yml   # Configuración de Docker
├── Dockerfile          # Imagen de la aplicación
├── requirements.txt    # Dependencias de Python
├── README.md          # Documentación principal
└── DOCKER.md         # Guía de Docker
```

## 📖 API Documentation

### Endpoints Principales

#### Health Check
- `GET /health` - Estado de la aplicación
- `GET /` - Información básica de la API

#### Vehículos
- `GET /api/v1/vehicles` - Listar vehículos
- `POST /api/v1/vehicles` - Crear vehículo
- `GET /api/v1/vehicles/{id}` - Obtener vehículo

#### Conductores
- `GET /api/v1/drivers` - Listar conductores
- `POST /api/v1/drivers` - Crear conductor
- `GET /api/v1/drivers/{id}` - Obtener conductor
- `GET /api/v1/drivers/available/` - Conductores disponibles

#### Clientes
- `GET /api/v1/clients` - Listar clientes
- `POST /api/v1/clients` - Crear cliente
- `GET /api/v1/clients/{id}` - Obtener cliente
- `GET /api/v1/clients/company/{company}` - Clientes por empresa

#### Direcciones
- `GET /api/v1/addresses` - Listar direcciones
- `POST /api/v1/addresses` - Crear dirección
- `GET /api/v1/addresses/{id}` - Obtener dirección
- `GET /api/v1/addresses/client/{client_id}` - Direcciones por cliente
- `GET /api/v1/addresses/city/{city}` - Direcciones por ciudad

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Para más detalles, consulta [API.md](API.md).

## 🗄️ Base de Datos

### Estructura de Datos

El sistema utiliza MySQL 8.0+ con las siguientes tablas:

#### vehicles
```sql
CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    vehicle_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'disponible',
    is_available BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### drivers
```sql
CREATE TABLE drivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    document_number VARCHAR(20) UNIQUE NOT NULL,
    license_type VARCHAR(10) NOT NULL,
    status VARCHAR(20) DEFAULT 'disponible',
    is_available BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### clients
```sql
CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    company VARCHAR(200),
    client_type VARCHAR(20) DEFAULT 'individual',
    status VARCHAR(20) DEFAULT 'activo',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### addresses
```sql
CREATE TABLE addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    street VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) DEFAULT 'Colombia',
    address_type VARCHAR(20) DEFAULT 'principal',
    is_primary BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

### Relaciones

- **Clientes ↔ Direcciones**: Una dirección pertenece a un cliente
- **Integridad Referencial**: Claves foráneas con restricciones
- **Índices**: Optimizados para consultas frecuentes

### Datos de Ejemplo

El sistema incluye datos de prueba:
- 3 vehículos (Toyota Hilux, Ford Transit, Honda CB250)
- 3 conductores (Juan Pérez, María García, Carlos López)
- 3 clientes (Empresa ABC, Ana Martínez, Distribuidora XYZ)
- 3 direcciones (Bogotá, Medellín, Cali)

## 🚀 Despliegue

### Docker (Recomendado)

```bash
# Desarrollo
docker-compose up -d

# Producción
docker-compose -f docker-compose.yml up -d
```

### Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
mysql -u root -p < database/init_mysql.sql

# Ejecutar aplicación
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Para más detalles, consulta [DEPLOYMENT.md](DEPLOYMENT.md).

## 🛠️ Guía de Desarrollo

### Principios Aplicados

- **SRP**: Single Responsibility Principle
- **DRY**: Don't Repeat Yourself
- **Separación de capas**: API, Servicios, Repositorios, Modelos
- **Código limpio**: Simple y mantenible

### Estructura de Archivos

#### Modelos
```python
# app/models/vehicle.py
class Vehicle(BaseModel):
    """Modelo de Vehículo"""
    __tablename__ = "vehicles"
    
    license_plate = Column(String(20), unique=True, nullable=False)
    brand = Column(String(100), nullable=False)
    # ... más campos
```

#### Servicios
```python
# app/services/vehicle_service.py
class VehicleService(BaseService):
    """Servicio para vehículos"""
    
    def get_available_vehicles(self, db: Session) -> List[Vehicle]:
        return self.repository.get_available_vehicles(db)
```

#### Repositorios
```python
# app/repositories/vehicle_repository.py
class VehicleRepository(BaseRepository[Vehicle]):
    """Repositorio para vehículos"""
    
    def get_by_license_plate(self, db: Session, plate: str) -> Optional[Vehicle]:
        return db.query(Vehicle).filter(Vehicle.license_plate == plate).first()
```

#### Rutas
```python
# app/api/routes/vehicles.py
@router.get("/", response_model=List[VehicleSummary])
async def get_vehicles(
    db: Session = Depends(get_db),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    return vehicle_service.get_all(db)
```

### Agregar Nuevos Endpoints

1. **Crear modelo** en `app/models/`
2. **Crear schema** en `app/schemas/`
3. **Crear repositorio** en `app/repositories/`
4. **Crear servicio** en `app/services/`
5. **Crear rutas** en `app/api/routes/`
6. **Registrar rutas** en `app/main.py`

### Testing

```bash
# Con Postman
# Importar colección desde postman/Rutas_Logisticas_API.postman_collection.json

# Con cURL
curl http://localhost:8000/api/v1/vehicles

# Con Python
import requests
response = requests.get("http://localhost:8000/api/v1/vehicles")
```

## 📊 Monitoreo

### Logs

```bash
# Docker
docker-compose logs -f app

# Local
tail -f logs/app.log
```

### Health Checks

```bash
# Aplicación
curl http://localhost:8000/health

# Base de datos
docker-compose exec mysql mysqladmin ping -h localhost -u root -p1234
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto:

1. Consulta la documentación
2. Revisa los logs de la aplicación
3. Contacta al equipo de desarrollo

---

**¡Sistema listo para desarrollo y producción! 🚀**