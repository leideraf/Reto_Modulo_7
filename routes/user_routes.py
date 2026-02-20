from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from models.user_model import User
from auth.auth_service import hashear_password, verificar_password
from auth.auth_handler import crear_token
from auth.dependencies import get_current_user, require_admin
from schemas.user_schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    LoginResponse,
    Message
)

router = APIRouter(
    tags=["Autenticación y Autorización"]
)

# =====================================================
# LOGIN
# =====================================================
@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesión"
)
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Autentica un usuario y devuelve un token JWT junto con
    los datos básicos del usuario.

    - username: Nombre de usuario
    - password: Contraseña

    Retorna:
    - access_token
    - token_type
    - user
    """
    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if not user or not verificar_password(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    # 🔐 El token ahora incluye rol (autorización)
    token = crear_token({
        "sub": user.username,
        "role": user.role
    })

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

# =====================================================
# REGISTER
# =====================================================
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario"
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo usuario en el sistema.

    - username: único (mínimo 3 caracteres)
    - password: mínimo 6 caracteres
    - role: user | admin
    """
    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
        )

    hashed_password = hashear_password(data.password)

    nuevo_usuario = User(
        username=data.username,
        hashed_password=hashed_password,
        role=data.role
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return UserResponse.model_validate(nuevo_usuario)

# =====================================================
# USUARIO AUTENTICADO
# =====================================================
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener usuario autenticado"
)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Devuelve la información del usuario autenticado.

    Requiere:
    Authorization: Bearer <token>
    """
    return UserResponse.model_validate(current_user)

# =====================================================
# RECURSO PROTEGIDO (USER)
# =====================================================
@router.get(
    "/resources",
    summary="Recurso protegido para usuarios autenticados"
)
async def protected_resources(
    current_user: User = Depends(get_current_user)
):
    """
    Ruta accesible para cualquier usuario autenticado.
    """
    return {
        "message": "Acceso permitido a recursos generales",
        "user": current_user.to_dict()
    }

# =====================================================
# RECURSO ADMIN
# =====================================================
@router.get(
    "/admin/resources",
    summary="Recurso protegido solo para administradores"
)
async def admin_resources(
    admin_user: User = Depends(require_admin)
):
    """
    Ruta protegida exclusivamente para usuarios con rol admin.
    """
    return {
        "message": f"Bienvenido administrador {admin_user.username}"
    }
