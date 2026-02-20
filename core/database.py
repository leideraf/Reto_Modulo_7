from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from core.config import DATABASE_URL
from core.logger import init_logger

logger = init_logger()

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base = declarative_base()

    logger.info("Conexión a PostgreSQL establecida correctamente")

except SQLAlchemyError as e:
    logger.critical(
        "Error crítico al conectar con la base de datos",
        exc_info=True
    )
    raise RuntimeError(
        f"Error al conectar con la base de datos: {str(e)}"
    )


def get_db():
    """
    Dependency de FastAPI para manejar la sesión de BD
    Incluye commit, rollback y cierre seguro
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(
            "Error durante operación en base de datos",
            exc_info=True
        )
        raise RuntimeError(
            f"Error en la operación de base de datos: {str(e)}"
        )
    finally:
        db.close()
