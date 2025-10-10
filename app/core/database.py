"""
Gestión de base de datos
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
import logging

from .config import config
from .base import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gestión simple de la base de datos"""
    
    def __init__(self):
        self._initialize_database()
    
    def _initialize_database(self):
        """Inicializa la conexión a la base de datos"""
        database_url = config.get_database_url()
        
        self.engine = create_engine(
            database_url,
            pool_pre_ping=True,
            echo=config.DEBUG
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def create_tables(self):
        """Crea todas las tablas"""
        Base.metadata.create_all(bind=self.engine)
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Obtiene una sesión de base de datos"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error en base de datos: {e}")
            raise
        finally:
            session.close()
    
    def health_check(self) -> bool:
        """Verifica si la base de datos está funcionando"""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False


# Instancia global
db_manager = DatabaseManager()

def get_db() -> Generator[Session, None, None]:
    """
    Dependencia para obtener una sesión de base de datos en los endpoints de FastAPI
    """
    with db_manager.get_session() as db:
        yield db
# Compatibilidad para código antiguo
SessionLocal = db_manager.SessionLocal

