"""
Tests unitarios para schemas de usuarios
"""
import pytest
from pydantic import ValidationError

from app.schemas.users_schemas import (
    UserBase, UserCreate, UserUpdate, UserLogin,
    RoleInfo, UserOut, RecoveryStartIn, VerifyAnswersIn, ResetPasswordIn
)


class TestUserBase:
    """Tests para UserBase schema"""
    
    def test_user_base_valid(self):
        """Debe crear user base válido"""
        user = UserBase(username="testuser")
        assert user.username == "testuser"
    
    def test_user_base_missing_username(self):
        """Debe fallar sin username"""
        with pytest.raises(ValidationError):
            UserBase()


class TestUserCreate:
    """Tests para UserCreate schema"""
    
    def test_create_valid_user(self):
        """Debe crear usuario con datos válidos"""
        user = UserCreate(
            username="testuser",
            password="TestPass123!"
        )
        assert user.username == "testuser"
        assert user.is_active is True  # default
    
    def test_create_user_with_security_questions(self):
        """Debe crear usuario con preguntas de seguridad"""
        user = UserCreate(
            username="testuser",
            password="TestPass123!",
            security_question1="¿Nombre de tu mascota?",
            security_answer1="Firulais",
            security_question2="¿Ciudad de nacimiento?",
            security_answer2="Bogotá"
        )
        assert user.security_question1 == "¿Nombre de tu mascota?"
        assert user.security_answer1 == "Firulais"
    
    def test_create_user_with_role(self):
        """Debe crear usuario con rol"""
        user = UserCreate(
            username="testuser",
            password="TestPass123!",
            role_id=2
        )
        assert user.role_id == 2
    
    def test_create_user_weak_password(self):
        """Debe fallar con contraseña débil"""
        with pytest.raises(ValidationError):
            UserCreate(
                username="testuser",
                password="weak"
            )
    
    def test_create_user_password_no_uppercase(self):
        """Debe fallar sin mayúsculas"""
        with pytest.raises(ValidationError):
            UserCreate(
                username="testuser",
                password="testpass123!"
            )
    
    def test_create_user_password_no_special(self):
        """Debe fallar sin carácter especial"""
        with pytest.raises(ValidationError):
            UserCreate(
                username="testuser",
                password="TestPass123"
            )


class TestUserUpdate:
    """Tests para UserUpdate schema"""
    
    def test_update_all_fields_optional(self):
        """Todos los campos deben ser opcionales"""
        update = UserUpdate()
        assert update.username is None
        assert update.role_id is None
        assert update.is_active is None
    
    def test_update_partial_fields(self):
        """Debe permitir actualización parcial"""
        update = UserUpdate(username="newname")
        assert update.username == "newname"
        assert update.role_id is None
    
    def test_update_role_and_status(self):
        """Debe actualizar rol y estado"""
        update = UserUpdate(role_id=3, is_active=False)
        assert update.role_id == 3
        assert update.is_active is False


class TestUserLogin:
    """Tests para UserLogin schema"""
    
    def test_login_valid(self):
        """Debe crear login válido"""
        login = UserLogin(username="testuser", password="TestPass123!")
        assert login.username == "testuser"
        assert login.password == "TestPass123!"
    
    def test_login_missing_username(self):
        """Debe fallar sin username"""
        with pytest.raises(ValidationError):
            UserLogin(password="TestPass123!")
    
    def test_login_missing_password(self):
        """Debe fallar sin password"""
        with pytest.raises(ValidationError):
            UserLogin(username="testuser")


class TestRoleInfo:
    """Tests para RoleInfo schema"""
    
    def test_role_info_valid(self):
        """Debe crear role info válido"""
        role = RoleInfo(id=1, name="admin")
        assert role.id == 1
        assert role.name == "admin"


class TestUserOut:
    """Tests para UserOut schema"""
    
    def test_user_out_from_dict(self):
        """Debe crear user out desde diccionario"""
        data = {
            "id": 1,
            "username": "testuser",
            "role_id": 2,
            "is_active": True,
            "role": None
        }
        user = UserOut(**data)
        assert user.id == 1
        assert user.username == "testuser"
    
    def test_user_out_with_role(self):
        """Debe crear user out con rol"""
        data = {
            "id": 1,
            "username": "testuser",
            "role_id": 2,
            "is_active": True,
            "role": {"id": 2, "name": "operador"}
        }
        user = UserOut(**data)
        assert user.role.name == "operador"


class TestRecoverySchemas:
    """Tests para schemas de recuperación"""
    
    def test_recovery_start_valid(self):
        """Debe crear recovery start válido"""
        recovery = RecoveryStartIn(username="testuser")
        assert recovery.username == "testuser"
    
    def test_verify_answers_valid(self):
        """Debe crear verify answers válido"""
        verify = VerifyAnswersIn(
            username="testuser",
            answers=["respuesta1", "respuesta2"]
        )
        assert verify.username == "testuser"
        assert len(verify.answers) == 2
    
    def test_reset_password_valid(self):
        """Debe crear reset password válido"""
        reset = ResetPasswordIn(
            token="some-token",
            username="testuser",
            new_password="NewPass123!"
        )
        assert reset.token == "some-token"
        assert reset.username == "testuser"
    
    def test_reset_password_weak(self):
        """Debe fallar con contraseña débil"""
        with pytest.raises(ValidationError):
            ResetPasswordIn(
                token="some-token",
                username="testuser",
                new_password="weak"
            )

