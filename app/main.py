"""
Aplicación principal FastAPI
Implementa principio SRP y configuración centralizada
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.config import config
from app.core.database import db_manager
from app.api.routes import vehicles, drivers, clients, addresses


# Configurar logging
logging.basicConfig(
    level=logging.INFO if not config.app.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager para el ciclo de vida de la aplicación
    Maneja inicialización y limpieza de recursos
    """
    # Startup
    logger.info("Iniciando aplicación Rutas Logísticas")
    
    try:
        # Crear tablas de base de datos
        db_manager.create_tables()
        logger.info("Tablas de base de datos creadas/verificadas")
        
        # Verificar conectividad
        if db_manager.health_check():
            logger.info("Conexión a base de datos exitosa")
        else:
            logger.error("Error en conexión a base de datos")
            raise Exception("No se pudo conectar a la base de datos")
        
    except Exception as e:
        logger.error(f"Error durante inicialización: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Cerrando aplicación Rutas Logísticas")


# Crear aplicación FastAPI
app = FastAPI(
    title="Rutas Logísticas API",
    description="API para gestión de vehículos, conductores, clientes y direcciones",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.app.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejadores de excepciones globales
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejador personalizado para excepciones HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": "2024-01-01T00:00:00Z"  # Se puede mejorar con datetime actual
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Manejador para excepciones generales"""
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detail": str(exc) if config.app.debug else None,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    )


# Rutas de la API
app.include_router(vehicles.router, prefix="/api/v1")
app.include_router(drivers.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(addresses.router, prefix="/api/v1")


# Rutas de salud y información
@app.get("/")
async def root():
    """Endpoint raíz con información básica de la API"""
    return {
        "message": "API de Rutas Logísticas",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar el estado de la aplicación"""
    try:
        db_status = db_manager.health_check()
        return {
            "status": "healthy" if db_status else "unhealthy",
            "database": "connected" if db_status else "disconnected",
            "version": "1.0.0",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return {
            "status": "unhealthy",
            "database": "error",
            "version": "1.0.0",
            "error": str(e) if config.app.debug else "Internal error"
        }


@app.get("/api/v1/info")
async def api_info():
    """Información detallada de la API"""
    return {
        "api_name": "Rutas Logísticas API",
        "version": "1.0.0",
        "description": "API para gestión completa de rutas logísticas",
        "endpoints": {
            "vehicles": "/api/v1/vehicles",
            "drivers": "/api/v1/drivers", 
            "clients": "/api/v1/clients",
            "addresses": "/api/v1/addresses"
        },
        "features": [
            "CRUD completo para vehículos",
            "CRUD completo para conductores",
            "CRUD completo para clientes",
            "Gestión de direcciones por cliente",
            "Búsqueda y filtrado avanzado",
            "Estadísticas y reportes",
            "Validaciones de negocio"
        ],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=config.app.api_host,
        port=config.app.api_port,
        reload=config.app.debug,
        log_level="info" if not config.app.debug else "debug"
    )
