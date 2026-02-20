from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
import secrets

from core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


# 🔐 Seguridad: si no existe SECRET_KEY en entorno, se genera una temporal
if not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(32)


def crear_token(
    data: dict,
    expiration: int = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    """
    Crea un token JWT con expiración.

    :param data: payload del token (ej: sub, role)
    :param expiration: minutos de expiración
    :return: JWT firmado
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiration)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verificar_token(token: str) -> dict | None:
    """
    Verifica y decodifica un token JWT.

    :param token: JWT recibido
    :return: payload si es válido, None si falla
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None
