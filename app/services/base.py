"""
Servicio base implementando patrón Service
Sigue principios SOLID: SRP, OCP, DIP
"""
from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
import logging

from app.repositories.base import BaseRepository

ModelType = TypeVar('ModelType')
RepositoryType = TypeVar('RepositoryType', bound=BaseRepository)

logger = logging.getLogger(__name__)


class BaseService(Generic[ModelType, RepositoryType], ABC):
    """
    Servicio base abstracto que implementa lógica de negocio genérica
    Implementa principio SRP y OCP (Open/Closed Principle)
    """
    
    def __init__(self, repository: RepositoryType):
        self.repository = repository
    
    def create(self, db: Session, **kwargs) -> ModelType:
        """Crea un nuevo registro con validaciones de negocio"""
        try:
            # Validaciones específicas antes de crear
            self._validate_create(kwargs)
            
            # Crear el registro
            return self.repository.create(db, **kwargs)
        except Exception as e:
            logger.error(f"Error al crear registro: {e}")
            raise
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Obtiene un registro por ID"""
        try:
            return self.repository.get_by_id(db, id)
        except Exception as e:
            logger.error(f"Error al obtener registro por ID {id}: {e}")
            raise
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtiene todos los registros con paginación"""
        try:
            return self.repository.get_all(db, skip, limit)
        except Exception as e:
            logger.error(f"Error al obtener registros: {e}")
            raise
    
    def get_count(self, db: Session) -> int:
        """Cuenta registros activos"""
        try:
            return self.repository.get_count(db)
        except Exception as e:
            logger.error(f"Error al contar registros: {e}")
            raise
    
    def update(self, db: Session, id: int, **kwargs) -> Optional[ModelType]:
        """Actualiza un registro existente con validaciones"""
        try:
            # Obtener registro existente
            db_obj = self.repository.get_by_id(db, id)
            if not db_obj:
                return None
            
            # Validaciones específicas antes de actualizar
            self._validate_update(db_obj, kwargs)
            
            # Actualizar el registro
            return self.repository.update(db, db_obj, **kwargs)
        except Exception as e:
            logger.error(f"Error al actualizar registro {id}: {e}")
            raise
    
    def delete(self, db: Session, id: int) -> bool:
        """Eliminación lógica de un registro"""
        try:
            # Validaciones antes de eliminar
            self._validate_delete(db, id)
            
            return self.repository.delete(db, id)
        except Exception as e:
            logger.error(f"Error al eliminar registro {id}: {e}")
            raise
    
    def search(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Búsqueda de registros"""
        try:
            if not search_term or len(search_term.strip()) < 2:
                return []
            
            return self.repository.search(db, search_term.strip(), skip, limit)
        except Exception as e:
            logger.error(f"Error en búsqueda '{search_term}': {e}")
            raise
    
    def filter_by(self, db: Session, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Filtrado de registros"""
        try:
            # Limpiar filtros vacíos
            clean_filters = {k: v for k, v in filters.items() if v is not None and v != ""}
            
            return self.repository.filter_by(db, clean_filters, skip, limit)
        except Exception as e:
            logger.error(f"Error al filtrar registros: {e}")
            raise
    
    def exists(self, db: Session, **kwargs) -> bool:
        """Verifica si existe un registro con los criterios dados"""
        try:
            return self.repository.exists(db, **kwargs)
        except Exception as e:
            logger.error(f"Error al verificar existencia: {e}")
            raise
    
    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtiene estadísticas del servicio"""
        try:
            return self.repository.get_statistics(db)
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {e}")
            raise
    
    def _validate_create(self, data: Dict[str, Any]) -> None:
        """
        Validaciones específicas antes de crear
        Debe ser implementado por las clases derivadas
        """
        pass
    
    def _validate_update(self, db_obj: ModelType, data: Dict[str, Any]) -> None:
        """
        Validaciones específicas antes de actualizar
        Debe ser implementado por las clases derivadas
        """
        pass
    
    def _validate_delete(self, db: Session, id: int) -> None:
        """
        Validaciones específicas antes de eliminar
        Debe ser implementado por las clases derivadas
        """
        pass
