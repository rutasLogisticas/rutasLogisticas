"""
Endpoints API para Roles y Permisos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.role_service import RoleService, PermissionService
from app.schemas.role_schemas import (
    RoleCreate, RoleUpdate, RoleResponse, RoleSummary, 
    PermissionResponse, UserPermissionsResponse
)
from app.api.dependencies import get_current_user
from app.models.users import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/roles", tags=["Roles"])
role_service = RoleService()
permission_service = PermissionService()


@router.get("/", response_model=List[RoleSummary])
def get_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtiene lista de roles"""
    try:
        roles = role_service.get_roles_summary(db, skip=skip, limit=limit)
        return roles
    except Exception as e:
        logger.error(f"Error obteniendo roles: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un rol específico"""
    try:
        role = role_service.get_role_by_id(db, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        # Convertir a response format
        permissions = []
        for rp in role.role_permissions:
            permissions.append(PermissionResponse(
                id=rp.permission.id,
                name=rp.permission.name,
                resource=rp.permission.resource,
                action=rp.permission.action,
                description=rp.permission.description,
                is_active=rp.permission.is_active
            ))
        
        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            permissions=permissions
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo rol {role_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo rol"""
    try:
        role = role_service.create_role(db, role_data)
        
        # Convertir a response format
        permissions = []
        for rp in role.role_permissions:
            permissions.append(PermissionResponse(
                id=rp.permission.id,
                name=rp.permission.name,
                resource=rp.permission.resource,
                action=rp.permission.action,
                description=rp.permission.description,
                is_active=rp.permission.is_active
            ))
        
        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            permissions=permissions
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creando rol: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un rol"""
    try:
        role = role_service.update_role(db, role_id, role_data)
        if not role:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        # Convertir a response format
        permissions = []
        for rp in role.role_permissions:
            permissions.append(PermissionResponse(
                id=rp.permission.id,
                name=rp.permission.name,
                resource=rp.permission.resource,
                action=rp.permission.action,
                description=rp.permission.description,
                is_active=rp.permission.is_active
            ))
        
        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            permissions=permissions
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error actualizando rol {role_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un rol"""
    try:
        success = role_service.delete_role(db, role_id)
        if not success:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return {"message": "Rol eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error eliminando rol {role_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/permissions/all", response_model=List[PermissionResponse])
def get_all_permissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtiene todos los permisos disponibles"""
    try:
        permissions = permission_service.get_all_permissions(db, skip=skip, limit=limit)
        return [PermissionResponse(
            id=p.id,
            name=p.name,
            resource=p.resource,
            action=p.action,
            description=p.description,
            is_active=p.is_active
        ) for p in permissions]
    except Exception as e:
        logger.error(f"Error obteniendo permisos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/permissions/init")
def initialize_permissions(
    db: Session = Depends(get_db)
):
    """Inicializa los permisos por defecto del sistema"""
    try:
        created_permissions = permission_service.create_default_permissions(db)
        return {
            "message": f"Inicialización completada. {len(created_permissions)} permisos creados.",
            "created_count": len(created_permissions)
        }
    except Exception as e:
        logger.error(f"Error inicializando permisos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/users/{user_id}/permissions", response_model=UserPermissionsResponse)
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene los permisos de un usuario específico"""
    try:
        # Obtener usuario
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Obtener permisos
        permissions = role_service.get_user_permissions(db, user_id)
        
        # Obtener nombre del rol
        role_name = None
        if user.role_id:
            role = role_service.get_role_by_id(db, user.role_id)
            if role:
                role_name = role.name
        
        formatted_permissions = [
            PermissionResponse(
                id=p.id,
                name=p.name,
                resource=p.resource,
                action=p.action,
                description=p.description,
                is_active=p.is_active
            ) for p in permissions
        ]
        
        return UserPermissionsResponse(
            user_id=user.id,
            username=user.username,
            role_id=user.role_id,
            role_name=role_name,
            permissions=formatted_permissions,
            total_permissions=len(formatted_permissions)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo permisos del usuario {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
