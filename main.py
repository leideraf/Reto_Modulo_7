# ============================================================
# IMPORTS PRINCIPALES
# ============================================================
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# ============================================================
# IMPORTS DEL PROYECTO
# ============================================================
from core.database import Base, engine
from core.config import CORS_ORIGINS
from core.logger import init_logger
from routes.user_routes import router as user_router

# Import del modelo para que SQLAlchemy registre la tabla
from models.user_model import User  # noqa: F401

# ============================================================
# INICIALIZAR LOGGER (UNA SOLA VEZ)
# ============================================================
logger = init_logger()

# ============================================================
# CICLO DE VIDA DE LA APLICACIÓN
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el inicio y cierre de la aplicación.
    - Crea las tablas al iniciar
    - Registra eventos críticos
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.critical(
            "Error al inicializar la base de datos",
            exc_info=True
        )
        raise

    yield  # Aplicación en ejecución

    logger.info("Aplicación finalizando correctamente")

# ============================================================
# INSTANCIA DE FASTAPI
# ============================================================
app = FastAPI(
    title="Sistema de Gestión de Acceso a Recursos Protegidos",
    description=(
        "API segura desarrollada con FastAPI que implementa "
        "autenticación JWT, hashing de contraseñas y "
        "control de acceso basado en roles."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# ============================================================
# MIDDLEWARE CORS
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MANEJADOR GLOBAL DE EXCEPCIONES
# ============================================================
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(
        "Error no controlado en la aplicación",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

# ============================================================
# RUTAS DE LA APLICACIÓN
# ============================================================
app.include_router(
    user_router,
    prefix="/api/v1"
)

# ============================================================
# PUNTO DE ENTRADA
# ============================================================
def main():
    """
    Función principal para iniciar el servidor con Uvicorn.
    """
    import uvicorn
    import webbrowser
    from threading import Timer

    host = "127.0.0.1"
    port = 8000

    # Abrir automáticamente Swagger UI
    def open_browser():
        webbrowser.open(f"http://{host}:{port}/docs")

    Timer(1.5, open_browser).start()

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()