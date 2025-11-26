"""
Tests unitarios para el módulo de seguridad
"""
import pytest
from datetime import timedelta
from jose import jwt, JWTError

from app.core.security import (
    validate_password_policy,
    verify_password,
    verify_answer,
    create_access_token,
    create_reset_token,
    verify_reset_token,
    verify_access_token,
    SECRET_KEY,
    ALGORITHM,
    PASSWORD_POLICY_DESCRIPTION
)


class TestPasswordPolicy:
    """Tests para validación de política de contraseñas"""
    
    def test_valid_password(self):
        """Contraseña válida no debe lanzar excepción"""
        valid_password = "TestPass123!"
        validate_password_policy(valid_password)  # No debe lanzar excepción
    
    def test_password_none(self):
        """Contraseña None debe lanzar ValueError"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_policy(None)
        assert PASSWORD_POLICY_DESCRIPTION in str(exc_info.value)
    
    def test_password_too_short(self):
        """Contraseña muy corta debe lanzar ValueError"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_policy("Ab1!")
        assert "8 caracteres" in str(exc_info.value)
    
    def test_password_with_spaces(self):
        """Contraseña con espacios debe lanzar ValueError"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_policy("Test Pass123!")
        assert "espacios" in str(exc_info.value)
    
    def test_password_no_uppercase(self):
        """Contraseña sin mayúsculas debe lanzar ValueError"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_policy("testpass123!")
        assert "mayúscula" in str(exc_info.value)
    
    def test_password_no_lowercase(self):
        """Contraseña sin minúsculas debe lanzar ValueError"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_policy("TESTPASS123!")
        assert "minúscula" in str(exc_info.value)
    
    def test_password_no_special_char(self):
        """Contraseña sin carácter especial debe lanzar ValueError"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_policy("TestPass123")
        assert "especial" in str(exc_info.value)


class TestVerifyWithInvalidHash:
    """Tests para verificación con hash inválido"""
    
    def test_verify_password_invalid_hash(self):
        """Verificar con hash inválido debe retornar False"""
        assert verify_password("password", "invalid_hash") is False
    
    def test_verify_answer_invalid_hash(self):
        """Verificar con hash inválido debe retornar False"""
        assert verify_answer("respuesta", "invalid_hash") is False


class TestJWTTokens:
    """Tests para funciones de tokens JWT"""
    
    def test_create_access_token_returns_string(self):
        """create_access_token debe retornar un string"""
        token = create_access_token({"sub": "testuser"})
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_custom_expiry(self):
        """Token con expiración personalizada"""
        token = create_access_token(
            {"sub": "testuser"}, 
            expires_delta=timedelta(hours=1)
        )
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload
    
    def test_create_access_token_sub_is_string(self):
        """El campo 'sub' debe ser string en el token"""
        token = create_access_token({"sub": 123})  # Pasamos int
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "123"  # Debe ser string
    
    def test_verify_access_token_valid(self):
        """Verificar token válido debe retornar payload"""
        original_data = {"sub": "testuser", "role": "admin"}
        token = create_access_token(original_data)
        payload = verify_access_token(token)
        assert payload["sub"] == "testuser"
        assert payload["role"] == "admin"
    
    def test_verify_access_token_invalid(self):
        """Verificar token inválido debe lanzar JWTError"""
        with pytest.raises(JWTError):
            verify_access_token("invalid.token.here")
    
    def test_create_reset_token_returns_string(self):
        """create_reset_token debe retornar un string"""
        token = create_reset_token("testuser")
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_reset_token_has_correct_scope(self):
        """Reset token debe tener scope 'password_reset'"""
        token = create_reset_token("testuser")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["scope"] == "password_reset"
        assert payload["sub"] == "testuser"
    
    def test_verify_reset_token_valid(self):
        """Verificar reset token válido debe retornar username"""
        username = "testuser"
        token = create_reset_token(username)
        result = verify_reset_token(token)
        assert result == username
    
    def test_verify_reset_token_invalid_scope(self):
        """Reset token con scope incorrecto debe fallar"""
        # Crear token con scope diferente
        payload = {"sub": "testuser", "scope": "other_scope", "exp": 9999999999}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        with pytest.raises(JWTError):
            verify_reset_token(token)
    
    def test_verify_reset_token_invalid(self):
        """Verificar reset token inválido debe lanzar JWTError"""
        with pytest.raises(JWTError):
            verify_reset_token("invalid.token.here")


class TestTokenExpiration:
    """Tests para expiración de tokens"""
    
    def test_expired_token_raises_error(self):
        """Token expirado debe lanzar error"""
        # Crear token que ya expiró
        token = create_access_token(
            {"sub": "testuser"}, 
            expires_delta=timedelta(seconds=-1)
        )
        with pytest.raises(JWTError):
            verify_access_token(token)
