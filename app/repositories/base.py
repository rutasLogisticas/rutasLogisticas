"""
Repositorio base implementando patrón Repository
Sigue principios SOLID: SRP, OCP, DIP
"""
from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from abc import ABC, abstractmethod

from app.models.base import BaseModel
from app.core.database import db_manager

ModelType = TypeVar('ModelType', bound=BaseModel)


class BaseRepository(Generic[ModelType], ABC):
    """
    Repositorio base abstracto que implementa operaciones CRUD genéricas
    Implementa principio SRP y OCP (Open/Closed Principle)
    """
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def create(self, db: Session, **kwargs) -> ModelType:
        """Crea un nuevo registro"""
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Obtiene un registro por ID"""
        return db.query(self.model).filter(
            and_(
                self.model.id == id,
                self.model.is_active == True
            )
        ).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtiene todos los registros activos con paginación"""
        return db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_count(self, db: Session) -> int:
        """Cuenta registros activos"""
        return db.query(self.model).filter(
            self.model.is_active == True
        ).count()
    
    def update(self, db: Session, db_obj: ModelType, **kwargs) -> ModelType:
        """Actualiza un registro existente"""
        for field, value in kwargs.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        """Eliminación lógica de un registro"""
        db_obj = self.get_by_id(db, id)
        if db_obj:
            db_obj.soft_delete()
            db.add(db_obj)
            db.commit()
            return True
        return False
    
    def hard_delete(self, db: Session, id: int) -> bool:
        """Eliminación física de un registro"""
        db_obj = self.get_by_id(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
    
    def search(self, db: Session, search_term: str, fields: List[str], skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Búsqueda genérica en múltiples campos"""
        search_conditions = []
        for field in fields:
            if hasattr(self.model, field):
                search_conditions.append(
                    getattr(self.model, field).ilike(f"%{search_term}%")
                )
        
        if not search_conditions:
            return []
        
        return db.query(self.model).filter(
            and_(
                self.model.is_active == True,
                or_(*search_conditions)
            )
        ).offset(skip).limit(limit).all()
    
    def filter_by(self, db: Session, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Filtrado genérico por múltiples campos"""
        query = db.query(self.model).filter(self.model.is_active == True)
        
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def exists(self, db: Session, **kwargs) -> bool:
        """Verifica si existe un registro con los criterios dados"""
        query = db.query(self.model).filter(self.model.is_active == True)
        
        for field, value in kwargs.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        
        return query.first() is not None
    
    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[ModelType]:
        """Obtiene un registro por un campo específico"""
        if not hasattr(self.model, field):
            return None
        
        return db.query(self.model).filter(
            and_(
                getattr(self.model, field) == value,
                self.model.is_active == True
            )
        ).first()
    
    def bulk_create(self, db: Session, objects_data: List[Dict[str, Any]]) -> List[ModelType]:
        """Crea múltiples registros en lote"""
        objects = []
        for data in objects_data:
            obj = self.model(**data)
            objects.append(obj)
        
        db.add_all(objects)
        db.commit()
        
        for obj in objects:
            db.refresh(obj)
        
        return objects
    
    def bulk_update(self, db: Session, updates: List[Dict[str, Any]]) -> List[ModelType]:
        """Actualiza múltiples registros en lote"""
        updated_objects = []
        
        for update_data in updates:
            obj_id = update_data.pop('id')
            obj = self.get_by_id(db, obj_id)
            if obj:
                self.update(db, obj, **update_data)
                updated_objects.append(obj)
        
        return updated_objects
