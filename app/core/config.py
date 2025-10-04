"""
Configuración central de la aplicación usando patrón Singleton
Sigue el principio SRP (Single Responsibility Principle)
"""
from typing import Dict, Any
import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    host: str = "localhost"
    port: int = 3306
    database: str = "rutas_logisticas"
    username: str = "root"
    password: str = "password"
    pool_size: int = 10
    max_overflow: int = 20
    charset: str = "utf8mb4"
    collation: str = "utf8mb4_unicode_ci"


@dataclass
class AppConfig:
    """Configuración general de la aplicación"""
    debug: bool = True
    secret_key: str = "your-secret-key-here"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    cors_origins: list = None
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]


class ConfigManager:
    """
    Singleton para gestión de configuraciones
    Implementa el patrón Singleton y principio OCP (Open/Closed Principle)
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._load_config()
            self._initialized = True
    
    def _load_config(self):
        """Carga configuración desde variables de entorno o valores por defecto"""
        self.database = DatabaseConfig(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            database=os.getenv('DB_NAME', 'rutas_logisticas'),
            username=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'password'),
            pool_size=int(os.getenv('DB_POOL_SIZE', 10)),
            max_overflow=int(os.getenv('DB_MAX_OVERFLOW', 20)),
            charset=os.getenv('DB_CHARSET', 'utf8mb4'),
            collation=os.getenv('DB_COLLATION', 'utf8mb4_unicode_ci')
        )
        
        self.app = AppConfig(
            debug=os.getenv('DEBUG', 'True').lower() == 'true',
            secret_key=os.getenv('SECRET_KEY', 'your-secret-key-here'),
            api_host=os.getenv('API_HOST', '127.0.0.1'),
            api_port=int(os.getenv('API_PORT', 8000)),
            cors_origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
        )
    
    def get_database_url(self) -> str:
        """Genera URL de conexión a base de datos"""
        return f"mysql+pymysql://{self.database.username}:{self.database.password}@{self.database.host}:{self.database.port}/{self.database.database}?charset={self.database.charset}"
    
    def get_config(self) -> Dict[str, Any]:
        """Retorna configuración completa como diccionario"""
        return {
            'database': {
                'host': self.database.host,
                'port': self.database.port,
                'database': self.database.database,
                'username': self.database.username,
                'password': self.database.password,
                'pool_size': self.database.pool_size,
                'max_overflow': self.database.max_overflow,
                'charset': self.database.charset,
                'collation': self.database.collation
            },
            'app': {
                'debug': self.app.debug,
                'secret_key': self.app.secret_key,
                'api_host': self.app.api_host,
                'api_port': self.app.api_port,
                'cors_origins': self.app.cors_origins
            }
        }


# Instancia global del ConfigManager
config = ConfigManager()
