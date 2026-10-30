import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

import jwt
from passlib.context import CryptContext

from akta.config import settings
from akta.logging import get_logger

logger = get_logger(__name__)

# Password hashing context supporting argon2 and bcrypt algorithms
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hashes a plaintext password using Argon2id/Bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a stored hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def hash_token(token: str) -> str:
    """Computes SHA-256 hash of a refresh token string for secure database storage."""
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def create_access_token(user_id: str, username: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a short-lived signed JWT access token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload: Dict[str, Any] = {
        "sub": user_id,
        "username": username,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": expire,
        "jti": str(uuid.uuid4())
    }

    return jwt.encode(payload, settings.auth_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decodes and validates a JWT access token, returning payload dict."""
    try:
        payload = jwt.decode(token, settings.auth_secret, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise ValueError("Token is not an access token.")
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Access token has expired.")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid access token: {e}")


def generate_refresh_token() -> tuple[str, str]:
    """Generates a secure random refresh token string and a unique JTI."""
    jti = str(uuid.uuid4())
    token_str = f"rt_{jti}_{uuid.uuid4().hex}"
    return token_str, jti
