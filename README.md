# Rutas Logísticas

Sistema completo de gestión logística construido con Python, FastAPI y MySQL. Implementa CRUD completo para vehículos, conductores, clientes y direcciones siguiendo principios SOLID y patrones de diseño.

## Características Principales

- **CRUD completo** para vehículos, conductores, clientes y direcciones
- **API REST** con FastAPI y documentación automática (Swagger/ReDoc)
- **Base de datos MySQL** con migraciones automáticas
- **Arquitectura limpia** siguiendo principios SOLID y SMART
- **Patrones de diseño** Singleton, Repository, Service Layer
- **Validaciones robustas** con Pydantic
- **Búsqueda y filtrado** avanzado
- **Estadísticas y reportes** en tiempo real
- **Docker support** para desarrollo y producción
- **Documentación completa** técnica y de API

## Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Services      │
│   (React/Vue)   │◄──►│   (FastAPI)     │◄──►│   Layer         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Repository    │
                       │     Layer       │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     MySQL       │
                       │   Database      │
                       └─────────────────┘
```

## Inicio Rápido

### Con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd rutas-logisticas

# 2. Configurar entorno
cp env.example .env
# Editar .env con tus configuraciones

# 3. Iniciar servicios
docker-compose up -d

# 4. Verificar instalación
curl http://localhost:8000/health
```

### Instalación Manual

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar base de datos
createdb rutas_logisticas
psql -d rutas_logisticas -f database/init.sql

# 4. Ejecutar migraciones
alembic upgrade head

# 5. Iniciar servidor
uvicorn app.main:app --reload
```

### Script de Configuración Automática

```bash
# Configuración completa automática
python scripts/setup.py
```

## Documentación

- **[Documentación Técnica](docs/README.md)** - Arquitectura, principios y guía de desarrollo
- **[API Documentation](docs/API.md)** - Referencia completa de endpoints
- **[Guía de Despliegue](docs/DEPLOYMENT.md)** - Instalación en desarrollo y producción
- **[Documentación Interactiva](http://localhost:8000/docs)** - Swagger UI (cuando el servidor esté ejecutándose)

## Principios de Diseño

### Principios SOLID Implementados

- **S** - **Single Responsibility**: Cada clase tiene una sola responsabilidad
- **O** - **Open/Closed**: Abierto para extensión, cerrado para modificación
- **L** - **Liskov Substitution**: Objetos derivados sustituibles por objetos base
- **I** - **Interface Segregation**: Interfaces específicas mejor que generales
- **D** - **Dependency Inversion**: Depender de abstracciones, no de concreciones

### Patrones de Diseño

- **Singleton**: Configuración y gestión de base de datos
- **Repository**: Acceso a datos con abstracción
- **Service Layer**: Lógica de negocio encapsulada
- **Factory**: Creación de objetos complejos
- **Observer**: Eventos del sistema

## Tecnologías Utilizadas

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Base de Datos**: MySQL 8.0+
- **Validación**: Pydantic
- **Migraciones**: Alembic
- **Contenedores**: Docker, Docker Compose
- **Servidor Web**: Nginx (producción)
- **Documentación**: Sphinx, Swagger/OpenAPI

## Estructura del Proyecto

```
rutas-logisticas/
├── app/                    # Aplicación principal
│   ├── api/               # Endpoints REST
│   ├── core/              # Configuración central
│   ├── models/            # Modelos de datos
│   ├── repositories/      # Capa de repositorio
│   ├── services/          # Lógica de negocio
│   └── schemas/           # Esquemas de validación
├── database/              # Scripts de BD
├── docs/                  # Documentación
├── migrations/            # Migraciones de BD
├── scripts/               # Scripts de utilidad
└── tests/                 # Tests unitarios
```

## API Endpoints Principales

### Vehículos
- `GET /api/v1/vehicles` - Listar vehículos
- `POST /api/v1/vehicles` - Crear vehículo
- `GET /api/v1/vehicles/{id}` - Obtener vehículo
- `PUT /api/v1/vehicles/{id}` - Actualizar vehículo
- `DELETE /api/v1/vehicles/{id}` - Eliminar vehículo

### Conductores
- `GET /api/v1/drivers` - Listar conductores
- `POST /api/v1/drivers` - Crear conductor
- `GET /api/v1/drivers/alerts/license-expiry` - Alertas de licencias

### Clientes
- `GET /api/v1/clients` - Listar clientes
- `POST /api/v1/clients` - Crear cliente
- `GET /api/v1/clients/by-tags/{tag}` - Buscar por tags

### Direcciones
- `GET /api/v1/addresses` - Listar direcciones
- `POST /api/v1/addresses` - Crear dirección
- `GET /api/v1/addresses/client/{id}/primary` - Dirección principal

### Estadísticas
- `GET /api/v1/vehicles/statistics/overview` - Estadísticas de vehículos
- `GET /api/v1/drivers/statistics/overview` - Estadísticas de conductores
- `GET /api/v1/clients/statistics/overview` - Estadísticas de clientes

## Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=app tests/

# Tests específicos
pytest tests/test_vehicles.py -v
```

## Despliegue

### Desarrollo
```bash
docker-compose up -d
```

### Producción
```bash
docker-compose -f docker-compose.prod.yml up -d
```

Ver [Guía de Despliegue](docs/DEPLOYMENT.md) para instrucciones detalladas.

## Características Avanzadas

- **Búsqueda inteligente**: Búsqueda por múltiples campos
- **Filtrado avanzado**: Filtros por capacidad, tipo, estado, etc.
- **Validaciones de negocio**: Reglas específicas por entidad
- **Eliminación lógica**: Soft delete para mantener integridad
- **Auditoría**: Timestamps automáticos de creación y actualización
- **Paginación**: Listados eficientes con paginación
- **Estadísticas**: Reportes en tiempo real
- **Alertas**: Notificaciones automáticas (licencias, mantenimiento)

## Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Roadmap

### v1.1.0
- Autenticación y autorización JWT
- Dashboard web con React/Vue
- Notificaciones en tiempo real
- Integración con mapas (Google Maps/OpenStreetMap)

### v1.2.0
- Optimización automática de rutas
- Tracking en tiempo real
- Integración con sistemas de pago
- Reportes avanzados y analytics

### v2.0.0
- Microservicios con Kubernetes
- Algoritmos para predicción de demanda
- Integración con IoT
- Mobile app nativa

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Soporte

- **Email**: dev@empresa.com
- **Issues**: [GitHub Issues](https://github.com/empresa/rutas-logisticas/issues)
- **Wiki**: [Documentación del Proyecto](https://github.com/empresa/rutas-logisticas/wiki)
- **Discord**: [Servidor de la Comunidad](https://discord.gg/rutas-logisticas)

## Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) por el framework web
- [SQLAlchemy](https://www.sqlalchemy.org/) por el ORM robusto
- [MySQL](https://www.mysql.com/) por la base de datos confiable
- [Pydantic](https://pydantic-docs.helpmanual.io/) por la validación de datos

---

**Desarrollado por el equipo de Rutas Logísticas**