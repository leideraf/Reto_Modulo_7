from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Literal

# ============================================================
# SCHEMA: REGISTRO DE USUARIO
# ============================================================
class UserCreate(BaseModel):
    """
    Schema para el registro de nuevos usuarios.
    """
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nombre de usuario único",
        examples=["juan_perez"]
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Contraseña del usuario",
        examples=["MiPassword123"]
    )
    role: Literal["user", "admin"] = Field(
        default="user",
        description="Rol del usuario dentro del sistema",
        examples=["user", "admin"]
    )

# ============================================================
# SCHEMA: LOGIN
# ============================================================
class UserLogin(BaseModel):
    """
    Schema para autenticación de usuarios.
    """
    username: str = Field(
        ...,
        description="Nombre de usuario",
        examples=["juan_perez"]
    )
    password: str = Field(
        ...,
        description="Contraseña del usuario",
        examples=["MiPassword123"]
    )

# ============================================================
# SCHEMA: RESPUESTA DE USUARIO (SIN PASSWORD)
# ============================================================
class UserResponse(BaseModel):
    """
    Schema para devolver información del usuario
    sin exponer datos sensibles.
    """
    id: int = Field(examples=[1])
    username: str = Field(examples=["juan_perez"])
    role: str = Field(examples=["user"])
    is_active: bool = Field(examples=[True])
    created_at: Optional[datetime] = Field(
        default=None,
        examples=["2025-10-09T14:30:00"]
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        examples=[None]
    )

    model_config = ConfigDict(
        from_attributes=True
    )

# ============================================================
# SCHEMA: TOKEN JWT
# ============================================================
class Token(BaseModel):
    """
    Schema para la respuesta de autenticación JWT.
    """
    access_token: str = Field(
        ...,
        description="Token JWT de acceso",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        ]
    )
    token_type: str = Field(
        default="bearer",
        description="Tipo de token",
        examples=["bearer"]
    )

# ============================================================
# SCHEMA: RESPUESTA DE LOGIN COMPLETA
# ============================================================
class LoginResponse(BaseModel):
    """
    Respuesta completa del login:
    token + datos del usuario.
    """
    access_token: str = Field(
        ...,
        description="Token JWT de acceso"
    )
    token_type: str = Field(
        default="bearer",
        description="Tipo de token"
    )
    user: UserResponse = Field(
        ...,
        description="Datos del usuario autenticado"
    )

# ============================================================
# SCHEMA: MENSAJES GENERALES
# ============================================================
class Message(BaseModel):
    """
    Schema genérico para mensajes de respuesta.
    """
    mensaje: str = Field(
        examples=["Operación realizada exitosamente"]
    )
