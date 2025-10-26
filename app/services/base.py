"""
Servicio base simple
"""
from typing import List, Optional, TypeVar, Generic
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository

T = TypeVar('T')


class BaseService(Generic[T]):
    """Servicio base simple"""
    
    def __init__(self):
        self.repository: BaseRepository[T] = None
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtiene todos los registros"""
        return self.repository.get_all(db, skip, limit)
    
    def get_by_id(self, db: Session, record_id: int) -> Optional[T]:
        """Obtiene registro por ID"""
        return self.repository.get_by_id(db, record_id)
    
    def create(self, db: Session, **kwargs) -> T:
        """Crea un nuevo registro"""
        return self.repository.create(db, **kwargs)
    
    def update(self, db: Session, record_id: int, **kwargs) -> Optional[T]:
        """Actualiza un registro"""
        record = self.repository.get_by_id(db, record_id)
        if record:
            return self.repository.update(db, record, **kwargs)
        return None
    
    def delete(self, db: Session, record_id: int) -> bool:
        """Elimina un registro"""
        return self.repository.delete(db, record_id)