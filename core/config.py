import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# BASE DE DATOS POSTGRESQL
# ===============================
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ===============================
# SEGURIDAD JWT
# ===============================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

# ===============================
# CORS
# ===============================
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
