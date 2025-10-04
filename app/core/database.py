"""
Gestión de base de datos usando patrón Singleton
Implementa conexión centralizada y pool de conexiones
"""
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import logging

from .config import config

logger = logging.getLogger(__name__)

# Base para modelos SQLAlchemy
Base = declarative_base()

# Metadata para gestión de esquemas
metadata = MetaData()


class DatabaseManager:
    """
    Singleton para gestión de conexiones a base de datos
    Implementa patrón Singleton y principio SRP
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_database()
            self._initialized = True
    
    def _initialize_database(self):
        """Inicializa la conexión a la base de datos"""
        try:
            database_url = config.get_database_url()
            
            self.engine = create_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=config.database.pool_size,
                max_overflow=config.database.max_overflow,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=config.app.debug
            )
            
            # Factory para sesiones
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info("Base de datos inicializada correctamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar base de datos: {e}")
            raise
    
    def create_tables(self):
        """Crea todas las tablas definidas en los modelos"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Tablas creadas exitosamente")
        except Exception as e:
            logger.error(f"Error al crear tablas: {e}")
            raise
    
    def drop_tables(self):
        """Elimina todas las tablas (usar solo para testing)"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Tablas eliminadas exitosamente")
        except Exception as e:
            logger.error(f"Error al eliminar tablas: {e}")
            raise
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager para obtener sesión de base de datos
        Maneja automáticamente commit/rollback
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error en sesión de base de datos: {e}")
            raise
        finally:
            session.close()
    
    def get_session_dependency(self) -> Generator[Session, None, None]:
        """Dependency para FastAPI"""
        with self.get_session() as session:
            yield session
    
    def health_check(self) -> bool:
        """Verifica conectividad con la base de datos"""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Health check fallido: {e}")
            return False


# Instancia global del DatabaseManager
db_manager = DatabaseManager()
