"""
Servicio para gestión de roles y permisos
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.users import User
from app.schemas.role_schemas import RoleCreate, RoleUpdate, RoleSummary
import logging

logger = logging.getLogger(__name__)


class RoleService:
    """Servicio para gestión de roles"""
    
    def get_all_roles(self, db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
        """Obtiene todos los roles con sus permisos"""
        return db.query(Role).options(
            joinedload(Role.role_permissions).joinedload(RolePermission.permission)
        ).filter(Role.is_active == True).offset(skip).limit(limit).all()
    
    def get_roles_summary(self, db: Session, skip: int = 0, limit: int = 100) -> List[RoleSummary]:
        """Obtiene resumen de roles"""
        roles = db.query(Role).filter(Role.is_active == True).offset(skip).limit(limit).all()
        result = []
        for role in roles:
            permissions_count = db.query(RolePermission).filter(
                RolePermission.role_id == role.id
            ).count()
            result.append(RoleSummary(
                id=role.id,
                name=role.name,
                description=role.description,
                is_active=role.is_active,
                permissions_count=permissions_count
            ))
        return result
    
    def get_role_by_id(self, db: Session, role_id: int) -> Optional[Role]:
        """Obtiene un rol por ID con sus permisos"""
        return db.query(Role).options(
            joinedload(Role.role_permissions).joinedload(RolePermission.permission)
        ).filter(and_(Role.id == role_id, Role.is_active == True)).first()
    
    def get_role_by_name(self, db: Session, name: str) -> Optional[Role]:
        """Obtiene un rol por nombre"""
        return db.query(Role).filter(and_(Role.name == name, Role.is_active == True)).first()
    
    def create_role(self, db: Session, role_data: RoleCreate) -> Role:
        """Crea un nuevo rol"""
        # Verificar que el nombre no exista
        existing_role = db.query(Role).filter(Role.name == role_data.name).first()
        if existing_role:
            raise ValueError(f"Ya existe un rol con el nombre '{role_data.name}'")
        
        # Crear el rol
        db_role = Role(
            name=role_data.name,
            description=role_data.description
        )
        db.add(db_role)
        db.flush()  # Para obtener el ID
        
        # Asignar permisos si se proporcionaron
        if role_data.permission_ids:
            for permission_id in role_data.permission_ids:
                # Verificar que el permiso existe
                permission = db.query(Permission).filter(Permission.id == permission_id).first()
                if permission:
                    role_permission = RolePermission(
                        role_id=db_role.id,
                        permission_id=permission_id
                    )
                    db.add(role_permission)
        
        db.commit()
        db.refresh(db_role)
        logger.info(f"Rol '{role_data.name}' creado con ID {db_role.id}")
        return db_role
    
    def update_role(self, db: Session, role_id: int, role_data: RoleUpdate) -> Optional[Role]:
        """Actualiza un rol"""
        db_role = self.get_role_by_id(db, role_id)
        if not db_role:
            return None
        
        # Actualizar campos básicos
        if role_data.name is not None:
            # Verificar que el nuevo nombre no exista
            existing_role = db.query(Role).filter(
                and_(Role.name == role_data.name, Role.id != role_id)
            ).first()
            if existing_role:
                raise ValueError(f"Ya existe un rol con el nombre '{role_data.name}'")
            db_role.name = role_data.name
        
        if role_data.description is not None:
            db_role.description = role_data.description
        
        if role_data.is_active is not None:
            db_role.is_active = role_data.is_active
        
        # Actualizar permisos si se proporcionaron
        if role_data.permission_ids is not None:
            # Eliminar permisos actuales
            db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
            
            # Agregar nuevos permisos
            for permission_id in role_data.permission_ids:
                permission = db.query(Permission).filter(Permission.id == permission_id).first()
                if permission:
                    role_permission = RolePermission(
                        role_id=role_id,
                        permission_id=permission_id
                    )
                    db.add(role_permission)
        
        db.commit()
        db.refresh(db_role)
        logger.info(f"Rol ID {role_id} actualizado")
        return db_role
    
    def delete_role(self, db: Session, role_id: int) -> bool:
        """Elimina un rol (soft delete)"""
        db_role = self.get_role_by_id(db, role_id)
        if not db_role:
            return False
        
        # Verificar que no hay usuarios con este rol
        users_count = db.query(User).filter(User.role_id == role_id).count()
        if users_count > 0:
            raise ValueError(f"No se puede eliminar el rol porque tiene {users_count} usuarios asignados")
        
        db_role.is_active = False
        db.commit()
        logger.info(f"Rol ID {role_id} eliminado")
        return True
    
    def get_user_permissions(self, db: Session, user_id: int) -> List[Permission]:
        """Obtiene todos los permisos de un usuario a través de su rol"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.role_id:
            return []
        
        permissions = db.query(Permission).join(
            RolePermission, Permission.id == RolePermission.permission_id
        ).filter(
            and_(
                RolePermission.role_id == user.role_id,
                Permission.is_active == True
            )
        ).all()
        
        return permissions


class PermissionService:
    """Servicio para gestión de permisos"""
    
    def get_all_permissions(self, db: Session, skip: int = 0, limit: int = 100) -> List[Permission]:
        """Obtiene todos los permisos"""
        return db.query(Permission).filter(Permission.is_active == True).offset(skip).limit(limit).all()
    
    def get_permission_by_id(self, db: Session, permission_id: int) -> Optional[Permission]:
        """Obtiene un permiso por ID"""
        return db.query(Permission).filter(
            and_(Permission.id == permission_id, Permission.is_active == True)
        ).first()
    
    def create_default_permissions(self, db: Session) -> List[Permission]:
        """Crea los permisos por defecto del sistema"""
        default_permissions = [
            # Usuarios
            {"name": "users_create", "resource": "users", "action": "create", "description": "Crear usuarios"},
            {"name": "users_read", "resource": "users", "action": "read", "description": "Ver usuarios"},
            {"name": "users_update", "resource": "users", "action": "update", "description": "Actualizar usuarios"},
            {"name": "users_delete", "resource": "users", "action": "delete", "description": "Eliminar usuarios"},
            
            # Roles
            {"name": "roles_create", "resource": "roles", "action": "create", "description": "Crear roles"},
            {"name": "roles_read", "resource": "roles", "action": "read", "description": "Ver roles"},
            {"name": "roles_update", "resource": "roles", "action": "update", "description": "Actualizar roles"},
            {"name": "roles_delete", "resource": "roles", "action": "delete", "description": "Eliminar roles"},
            
            # Clientes
            {"name": "clients_create", "resource": "clients", "action": "create", "description": "Crear clientes"},
            {"name": "clients_read", "resource": "clients", "action": "read", "description": "Ver clientes"},
            {"name": "clients_update", "resource": "clients", "action": "update", "description": "Actualizar clientes"},
            {"name": "clients_delete", "resource": "clients", "action": "delete", "description": "Eliminar clientes"},
            
            # Vehículos
            {"name": "vehicles_create", "resource": "vehicles", "action": "create", "description": "Crear vehículos"},
            {"name": "vehicles_read", "resource": "vehicles", "action": "read", "description": "Ver vehículos"},
            {"name": "vehicles_update", "resource": "vehicles", "action": "update", "description": "Actualizar vehículos"},
            {"name": "vehicles_delete", "resource": "vehicles", "action": "delete", "description": "Eliminar vehículos"},
            
            # Conductores
            {"name": "drivers_create", "resource": "drivers", "action": "create", "description": "Crear conductores"},
            {"name": "drivers_read", "resource": "drivers", "action": "read", "description": "Ver conductores"},
            {"name": "drivers_update", "resource": "drivers", "action": "update", "description": "Actualizar conductores"},
            {"name": "drivers_delete", "resource": "drivers", "action": "delete", "description": "Eliminar conductores"},
            
            # Pedidos
            {"name": "orders_create", "resource": "orders", "action": "create", "description": "Crear pedidos"},
            {"name": "orders_read", "resource": "orders", "action": "read", "description": "Ver pedidos"},
            {"name": "orders_update", "resource": "orders", "action": "update", "description": "Actualizar pedidos"},
            {"name": "orders_delete", "resource": "orders", "action": "delete", "description": "Eliminar pedidos"},
            
            # Reportes
            {"name": "reports_read", "resource": "reports", "action": "read", "description": "Ver reportes"},
        ]
        
        created_permissions = []
        for perm_data in default_permissions:
            # Verificar si ya existe
            existing = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
            if not existing:
                permission = Permission(**perm_data)
                db.add(permission)
                created_permissions.append(permission)
        
        if created_permissions:
            db.commit()
            logger.info(f"Creados {len(created_permissions)} permisos por defecto")
        
        return created_permissions
