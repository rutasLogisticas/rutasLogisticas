"""
Configuración de la aplicación
"""
import os


class Config:
    """Configuración simple y clara"""
    
    # Base de datos
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'rutas_logisticas')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')
    
    # Aplicación
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    API_HOST = os.getenv('API_HOST', '127.0.0.1')
    API_PORT = int(os.getenv('API_PORT', 8000))
    
    # Google Maps API
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyDfIIPbFtxFmsLEeoe-msMMReXOCPVPBKU')
    
    @classmethod
    def get_database_url(cls) -> str:
        """URL de conexión a la base de datos"""
        return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}?charset=utf8mb4&use_unicode=1"


# Instancia global
config = Config()
