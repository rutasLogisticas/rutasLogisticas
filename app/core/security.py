from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "secret-key-aqui"  # cámbiala en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_EXPIRE_MINUTES = 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === Contraseñas ===
def get_password_hash(password: str) -> str:
    """Genera un hash seguro con bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que la contraseña en texto plano coincida con el hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

# === Preguntas de seguridad ===
def hash_answer(answer: str) -> str:
    """Genera hash normalizado para respuestas."""
    return pwd_context.hash(answer.strip().lower())

def verify_answer(plain: str, hashed: str) -> bool:
    """Verifica respuesta con normalización de mayúsculas/minúsculas."""
    try:
        return pwd_context.verify(plain.strip().lower(), hashed)
    except Exception:
        return False

# === Tokens JWT ===
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_reset_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "scope": "password_reset", "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("scope") != "password_reset":
            raise JWTError("Invalid scope")
        return payload.get("sub")
    except JWTError:
        raise
