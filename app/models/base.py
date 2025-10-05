"""
Modelo base con funcionalidades comunes
Implementa principio DRY (Don't Repeat Yourself) y SRP
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr
from app.core.base import Base


class BaseModel(Base):
    """
    Modelo base abstracto con campos comunes
    Implementa principio SRP y OCP
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    @declared_attr
    def __tablename__(cls):
        """Genera nombre de tabla automáticamente basado en el nombre de la clase"""
        return cls.__name__.lower() + 's'
    
    def __repr__(self):
        """Representación string del modelo"""
        return f"<{self.__class__.__name__}(id={self.id})>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data: dict):
        """Actualiza el modelo desde un diccionario"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
    
    def soft_delete(self):
        """Eliminación lógica del registro"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def restore(self):
        """Restaura un registro eliminado lógicamente"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
