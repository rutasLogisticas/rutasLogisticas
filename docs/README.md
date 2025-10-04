# Rutas Logísticas - Documentación Técnica

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Principios de Diseño](#principios-de-diseño)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [API Documentation](#api-documentation)
7. [Base de Datos](#base-de-datos)
8. [Patrones de Diseño Implementados](#patrones-de-diseño-implementados)
9. [Guía de Desarrollo](#guía-de-desarrollo)
10. [Testing](#testing)
11. [Despliegue](#despliegue)

## Introducción

**Rutas Logísticas** es un sistema completo de gestión logística que permite la administración de vehículos, conductores, clientes y direcciones. El sistema está diseñado siguiendo los principios SOLID, SMART y patrones de diseño como Singleton y Repository.

### Características Principales

- **CRUD completo** para vehículos, conductores, clientes y direcciones
- **API REST** con FastAPI y documentación automática
- **Base de datos MySQL** con migraciones
- **Arquitectura limpia** siguiendo principios SOLID
- **Validaciones de negocio** robustas
- **Búsqueda y filtrado** avanzado
- **Estadísticas y reportes**
- **Docker support** para desarrollo y producción

## Arquitectura del Sistema

### Diagrama de Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Microservices │
│   (React/Vue)   │◄──►│   (FastAPI)     │◄──►│   (Modules)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │     (MySQL)     │
                       └─────────────────┘
```

### Capas de la Aplicación

1. **Capa de Presentación (API)**: Endpoints REST con FastAPI
2. **Capa de Servicios**: Lógica de negocio
3. **Capa de Repositorio**: Acceso a datos
4. **Capa de Modelos**: Entidades de dominio
5. **Capa de Base de Datos**: Persistencia con MySQL

## Principios de Diseño

### Principios SOLID

- **S** - **Single Responsibility Principle (SRP)**: Cada clase tiene una sola responsabilidad
- **O** - **Open/Closed Principle (OCP)**: Abierto para extensión, cerrado para modificación
- **L** - **Liskov Substitution Principle (LSP)**: Los objetos derivados deben ser sustituibles por sus objetos base
- **I** - **Interface Segregation Principle (ISP)**: Muchas interfaces específicas son mejores que una general
- **D** - **Dependency Inversion Principle (DIP)**: Depender de abstracciones, no de concreciones

### Principios SMART

- **S** - **Specific**: Específico y claro
- **M** - **Measurable**: Medible y cuantificable
- **A** - **Achievable**: Alcanzable y realista
- **R** - **Relevant**: Relevante para el negocio
- **T** - **Time-bound**: Con límite de tiempo

### Patrones de Diseño

1. **Singleton**: Para configuración y gestión de base de datos
2. **Repository**: Para acceso a datos
3. **Service Layer**: Para lógica de negocio
4. **Factory**: Para creación de objetos
5. **Observer**: Para eventos del sistema

## Instalación y Configuración

### Requisitos Previos

- Python 3.11+
- MySQL 8.0+
- Docker (opcional)
- Git

### Instalación Rápida

```bash
# Clonar el repositorio
git clone <repository-url>
cd rutas-logisticas

# Configurar entorno
python scripts/setup.py

# Iniciar con Docker
docker-compose up -d
```

### Instalación Manual

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp env.example .env
# Editar .env con tus configuraciones

# 4. Configurar base de datos
createdb rutas_logisticas
psql -d rutas_logisticas -f database/init.sql

# 5. Ejecutar migraciones
alembic upgrade head

# 6. Iniciar servidor
uvicorn app.main:app --reload
```

## Estructura del Proyecto

```
rutas-logisticas/
├── app/                          # Aplicación principal
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada de FastAPI
│   ├── api/                      # Capa de API REST
│   │   ├── __init__.py
│   │   ├── dependencies.py       # Dependencias de la API
│   │   └── routes/               # Endpoints
│   │       ├── vehicles.py
│   │       ├── drivers.py
│   │       ├── clients.py
│   │       └── addresses.py
│   ├── core/                     # Configuración central
│   │   ├── __init__.py
│   │   ├── config.py            # Configuración con Singleton
│   │   └── database.py          # Gestión de BD con Singleton
│   ├── models/                   # Modelos de datos
│   │   ├── __init__.py
│   │   ├── base.py              # Modelo base
│   │   ├── vehicle.py
│   │   ├── driver.py
│   │   ├── client.py
│   │   └── address.py
│   ├── repositories/             # Capa de repositorio
│   │   ├── __init__.py
│   │   ├── base.py              # Repositorio base
│   │   ├── vehicle_repository.py
│   │   ├── driver_repository.py
│   │   ├── client_repository.py
│   │   └── address_repository.py
│   ├── services/                 # Capa de servicios
│   │   ├── __init__.py
│   │   ├── base.py              # Servicio base
│   │   ├── vehicle_service.py
│   │   ├── driver_service.py
│   │   ├── client_service.py
│   │   └── address_service.py
│   └── schemas/                  # Esquemas Pydantic
│       ├── __init__.py
│       ├── base_schemas.py
│       ├── vehicle_schemas.py
│       ├── driver_schemas.py
│       ├── client_schemas.py
│       └── address_schemas.py
├── database/                     # Scripts de base de datos
│   └── init.sql                 # Script de inicialización
├── docs/                        # Documentación
│   ├── README.md
│   ├── api.md
│   └── deployment.md
├── migrations/                  # Migraciones de Alembic
│   ├── env.py
│   └── script.py.mako
├── scripts/                     # Scripts de utilidad
│   └── setup.py
├── tests/                       # Tests
├── requirements.txt             # Dependencias
├── pyproject.toml              # Configuración del proyecto
├── alembic.ini                 # Configuración de Alembic
├── docker-compose.yml          # Docker Compose
├── Dockerfile                  # Imagen Docker
└── README.md                   # Documentación principal
```

## API Documentation

### Endpoints Principales

#### Vehículos
- `GET /api/v1/vehicles` - Listar vehículos
- `POST /api/v1/vehicles` - Crear vehículo
- `GET /api/v1/vehicles/{id}` - Obtener vehículo
- `PUT /api/v1/vehicles/{id}` - Actualizar vehículo
- `DELETE /api/v1/vehicles/{id}` - Eliminar vehículo

#### Conductores
- `GET /api/v1/drivers` - Listar conductores
- `POST /api/v1/drivers` - Crear conductor
- `GET /api/v1/drivers/{id}` - Obtener conductor
- `PUT /api/v1/drivers/{id}` - Actualizar conductor
- `DELETE /api/v1/drivers/{id}` - Eliminar conductor

#### Clientes
- `GET /api/v1/clients` - Listar clientes
- `POST /api/v1/clients` - Crear cliente
- `GET /api/v1/clients/{id}` - Obtener cliente
- `PUT /api/v1/clients/{id}` - Actualizar cliente
- `DELETE /api/v1/clients/{id}` - Eliminar cliente

#### Direcciones
- `GET /api/v1/addresses` - Listar direcciones
- `POST /api/v1/addresses` - Crear dirección
- `GET /api/v1/addresses/{id}` - Obtener dirección
- `PUT /api/v1/addresses/{id}` - Actualizar dirección
- `DELETE /api/v1/addresses/{id}` - Eliminar dirección

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Base de Datos

### Esquema de Base de Datos

```sql
-- Tabla de vehículos
vehicles (id, license_plate, brand, model, year, vehicle_type, status, ...)

-- Tabla de conductores
drivers (id, first_name, last_name, email, license_type, license_number, ...)

-- Tabla de clientes
clients (id, name, client_type, status, email, phone, ...)

-- Tabla de direcciones
addresses (id, client_id, address_type, address_line1, city, state, ...)
```

### Relaciones

- Un cliente puede tener múltiples direcciones (1:N)
- Un vehículo puede estar en múltiples rutas (1:N)
- Un conductor puede manejar múltiples vehículos (N:M)

### Migraciones

```bash
# Crear nueva migración
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir migración
alembic downgrade -1
```

## Patrones de Diseño Implementados

### 1. Singleton

```python
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
```

### 2. Repository Pattern

```python
class BaseRepository(Generic[ModelType]):
    def create(self, db: Session, **kwargs) -> ModelType:
        # Implementación genérica
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        # Implementación genérica
```

### 3. Service Layer

```python
class VehicleService(BaseService[Vehicle, VehicleRepository]):
    def create_vehicle(self, db: Session, **kwargs) -> Vehicle:
        self._validate_create(kwargs)
        return self.repository.create(db, **kwargs)
```

## Guía de Desarrollo

### Agregar Nueva Entidad

1. **Crear modelo** en `app/models/`
2. **Crear repositorio** en `app/repositories/`
3. **Crear servicio** en `app/services/`
4. **Crear esquemas** en `app/schemas/`
5. **Crear endpoints** en `app/api/routes/`
6. **Crear migración** con Alembic

### Convenciones de Código

- **Nombres de archivos**: snake_case
- **Nombres de clases**: PascalCase
- **Nombres de funciones**: snake_case
- **Constantes**: UPPER_CASE
- **Tipos de datos**: Usar type hints

### Estructura de Commits

```
feat: agregar nueva funcionalidad
fix: corregir bug
docs: actualizar documentación
style: cambios de formato
refactor: refactorizar código
test: agregar o modificar tests
```

## Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_vehicles.py

# Con cobertura
pytest --cov=app tests/
```

### Tipos de Tests

1. **Unit Tests**: Testear funciones individuales
2. **Integration Tests**: Testear integración entre componentes
3. **API Tests**: Testear endpoints de la API
4. **Database Tests**: Testear operaciones de base de datos

## Despliegue

### Desarrollo

```bash
# Con Docker
docker-compose up -d

# Manual
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción

```bash
# Con Docker
docker-compose -f docker-compose.prod.yml up -d

# Manual
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Variables de Entorno de Producción

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
DB_HOST=your-db-host
DB_PASSWORD=your-secure-password
```

## Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas:
- 📧 Email: dev@empresa.com
- 🐛 Issues: [GitHub Issues](https://github.com/empresa/rutas-logisticas/issues)
- 📖 Documentación: [Wiki del Proyecto](https://github.com/empresa/rutas-logisticas/wiki)
