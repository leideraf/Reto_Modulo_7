from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

from core.database import Base


class User(Base):
    """
    Modelo de usuario para la aplicación.

    Representa un usuario del sistema con autenticación JWT
    y control de acceso basado en roles.
    """
    __tablename__ = "users"

    # ============================
    # CAMPOS PRINCIPALES
    # ============================
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="ID único del usuario"
    )

    username = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="Nombre de usuario único"
    )

    hashed_password = Column(
        String(255),
        nullable=False,
        comment="Contraseña hasheada del usuario"
    )

    # ============================
    # ESTADO Y ROLES
    # ============================
    role = Column(
        String(20),
        nullable=False,
        default="user",
        comment="Rol del usuario (user, admin)"
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Indica si el usuario está activo"
    )

    # ============================
    # TIMESTAMPS
    # ============================
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Fecha y hora de creación del usuario"
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Fecha y hora de última actualización"
    )

    # ============================
    # VALIDACIONES
    # ============================
    @validates("username")
    def validate_username(self, key, username: str) -> str:
        """
        Valida el formato del nombre de usuario.
        """
        if not username:
            raise ValueError("El nombre de usuario no puede estar vacío")

        username = username.strip().lower()

        if len(username) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")

        if len(username) > 50:
            raise ValueError("El nombre de usuario no puede tener más de 50 caracteres")

        if not username.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "El nombre de usuario solo puede contener letras, números, guiones y guiones bajos"
            )

        return username

    @validates("hashed_password")
    def validate_hashed_password(self, key, hashed_password: str) -> str:
        """
        Valida que la contraseña hasheada no esté vacía.
        """
        if not hashed_password:
            raise ValueError("La contraseña hasheada no puede estar vacía")
        return hashed_password

    # ============================
    # MÉTODOS DE UTILIDAD
    # ============================
    def __repr__(self) -> str:
        """
        Representación legible del objeto User.
        """
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"

    def to_dict(self) -> dict:
        """
        Convierte el usuario a diccionario sin exponer la contraseña.
        Útil para respuestas controladas o logs.
        """
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
