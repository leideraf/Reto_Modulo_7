# Seguridad en APIs con FastAPI: Autenticación con JWT y Passlib

## Descripción del proyecto

En el desarrollo de aplicaciones modernas es fundamental proteger el acceso a los recursos del sistema y garantizar que la información de los usuarios sea manejada de forma segura.

Este proyecto implementa un sistema de **autenticación y autorización basado en tokens JWT (JSON Web Tokens)** utilizando **FastAPI**, junto con **Passlib** para la gestión segura de contraseñas mediante hashing.

El objetivo es demostrar de forma práctica cómo se implementa un flujo completo de autenticación en una API moderna, incluyendo:

- Registro de usuarios
- Inicio de sesión
- Generación de tokens JWT
- Validación de tokens para acceder a rutas protegidas
- Manejo seguro de contraseñas mediante hashing

Este tipo de arquitectura es ampliamente utilizada en aplicaciones web modernas y microservicios.

---

# Tecnologías utilizadas

El proyecto fue desarrollado utilizando las siguientes tecnologías:

- **Python**
- **FastAPI** – Framework moderno para construcción de APIs
- **Passlib** – Librería para hashing seguro de contraseñas
- **JWT (JSON Web Tokens)** – Sistema de autenticación basado en tokens
- **Uvicorn** – Servidor ASGI para ejecutar la aplicación
- **Streamlit / Postman** – Cliente para probar las peticiones
- **Pydantic** – Validación de datos
- **Python-dotenv** – Manejo de variables de entorno

---

# Estructura del proyecto

El repositorio está organizado de forma modular siguiendo buenas prácticas de desarrollo.
```python
src/
│
├── main.py                # Punto de entrada de la aplicación FastAPI
│
├── auth/                  # Lógica de autenticación
│   ├── auth_handler.py    # Manejo de tokens JWT y seguridad
│   ├── auth_service.py    # Lógica de login y registro de usuarios
│   └── dependencies.py    # Dependencias para autenticación y protección de rutas
│
├── core/                  # Configuración central del sistema
│   ├── config.py          # Variables de configuración y entorno
│   ├── database.py        # Conexión a la base de datos
│   └── logger.py          # Configuración del sistema de logs
│
├── models/                # Modelos de base de datos
│   └── user_model.py      # Modelo de usuario
│
├── routes/                # Endpoints de la API
│   └── user_routes.py     # Rutas relacionadas con usuarios
│
├── schemas/               # Esquemas de validación con Pydantic
│   └── user_schemas.py    # Esquemas de entrada y salida de usuarios
│
├── logs/                  # Archivos de registro generados por la aplicación
│
├── streamlit_app.py       # Cliente simple para interactuar con la API
│
├── requirements.txt       # Dependencias del proyecto
│
├── .env                   # Variables de entorno (no debe subirse al repositorio)
│
└── README.md              # Documentación del proyecto
```

---

# Flujo de autenticación

El sistema implementa un flujo de autenticación basado en **JWT**, el cual permite manejar sesiones de usuario sin necesidad de mantener estado en el servidor.

El flujo se compone de tres etapas principales:

- Registro de usuario
- Inicio de sesión
- Verificación del token para acceder a recursos protegidos

---

## Registro de usuario

El proceso de registro permite crear nuevas cuentas dentro del sistema.

Flujo del proceso:

1. El cliente envía `username` y `password` al endpoint `/register`.
2. El backend valida que el usuario no exista previamente.
3. La contraseña es procesada utilizando **Passlib con el algoritmo Argon2**.
4. Se genera un **hash seguro de la contraseña**.
5. El sistema almacena en la base de datos:
   - username
   - hashed_password
   - estado del usuario

Es importante destacar que **la contraseña nunca se almacena en texto plano**.

Esto protege la información del usuario incluso si la base de datos fuera comprometida.

---

## Inicio de sesión (Login)

Una vez registrado, el usuario puede autenticarse en el sistema.

Flujo del login:

1. El cliente envía `username` y `password` al endpoint `/login`.
2. El sistema busca el usuario en la base de datos.
3. La contraseña ingresada es comparada con el **hash almacenado** utilizando Passlib.
4. Si las credenciales son válidas, el sistema genera un **token JWT**.

Este token será utilizado por el cliente para acceder a los recursos protegidos de la API.

---

## Verificación del token y acceso a rutas protegidas

Para acceder a rutas protegidas, el cliente debe enviar el token JWT en cada solicitud.

Ejemplo del header de autorización:

Authorization: Bearer <token>

Cuando el backend recibe la solicitud:

1. Extrae el token del header.
2. Decodifica el token.
3. Verifica que la firma sea válida.
4. Comprueba que el token no esté expirado.
5. Identifica al usuario desde el contenido del token.

Si todas las validaciones son correctas, el usuario obtiene acceso al recurso solicitado.

---

# Uso de Passlib para seguridad de contraseñas

El proyecto utiliza **Passlib** como mecanismo de seguridad para proteger las contraseñas de los usuarios.

Se configura un contexto de hashing utilizando el algoritmo **Argon2**, considerado uno de los métodos más seguros actualmente.

Ejemplo de configuración:

```python
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
```
Este contexto permite:

- generar hashes de contraseñas
- verificar contraseñas durante el login
- Proceso de hashing

Durante el registro:

- El usuario envía su contraseña al sistema.
- La contraseña se transforma en un hash irreversible.
- Solo el hash es almacenado en la base de datos.
- Verificación de contraseña

Durante el login:

- El usuario envía su contraseña.
- El sistema compara la contraseña ingresada con el hash almacenado.
- Si coinciden, la autenticación es exitosa.
- En ningún momento se desencripta la contraseña original.

Ejemplo de Token JWT

Cuando un usuario inicia sesión correctamente, el sistema genera un token JWT que contiene información del usuario autenticado.

### Ejemplo de payload del token:
```python
{
  "sub": "usuario1",
  "role": "admin",
  "exp": 1715620000
}
```
Descripción de los campos:

sub → identificador del usuario
role → rol del usuario dentro del sistema
exp → fecha de expiración del token

Este token puede ser decodificado por el backend para identificar al usuario y validar su acceso a las rutas protegidas.

### Ejemplo de uso de la API
Registro de usuario

Endpoint

POST /register
```python
Body

{
 "username": "usuario1",
 "password": "password123"
}
Login
```
Endpoint
```python
POST /login

Body

{
 "username": "usuario1",
 "password": "password123"
}
```
Respuesta
```python
{
 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
 "token_type": "bearer"
}
```

## Pasos para ejecutar y compilar el proyecto

A continuación, se describen los pasos necesarios para ejecutar correctamente el proyecto, tanto el backend (FastAPI) como el cliente visual (Streamlit).

1. Primero, se debe clonar el repositorio desde GitHub
```bash
git clone https://github.com/leideraf/Reto_Modulo_7.git
```

2. Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.
```bash
python -m venv venv
venv\Scripts\activate
```

3. Con el entorno virtual activo, se instalan las librerías necesarias
```bash
pip install -r requirements.txt
```

4. Configurar las variables de entorno
El proyecto utiliza variables de entorno para manejar información sensible.
 -Crear un archivo .env en la raíz del proyecto.
 -Definir las siguientes variables:
```bash
DB_USER=postgres
DB_PASS=tu_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_db

SECRET_KEY=clave_secreta_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
5. Crear la base de datos
 - Antes de ejecutar la aplicación, se debe crear la base de datos en PostgreSQL
```bash
CREATE DATABASE auth_db;
```

Al iniciar la API, las tablas se crean automáticamente mediante SQLAlchemy.

6. Ejecutar el backend (FastAPI)
 - Con la base de datos configurada, se inicia el servidor backend
```bash
uvicorn main:app --reload
```

Esto ejecuta:
- El servidor FastAPI en http://127.0.0.1:8000
- La documentación Swagger en http://127.0.0.1:8000/docs

7. Ejecutar el cliente (Streamlit)
 -En una nueva terminal, con el entorno virtual activo, se ejecuta el cliente visual
```bash
streamlit run streamlit_app.py
```

Esto abre la interfaz gráfica en el navegador, desde donde se puede:
 - Registrar usuarios
 - Iniciar sesión
 - Acceder a recursos protegidos
 - Probar rutas de administrador

Siguiendo estos pasos, el proyecto queda completamente funcional, permitiendo probar de forma práctica el sistema de autenticación y autorización basado en JWT y Passlib.


Video explicativo

En el siguiente video se explica el funcionamiento del sistema, el flujo de autenticación y las medidas de seguridad implementadas.

Enlace al video:

https://youtube.com/tu_video

### Buenas prácticas aplicadas

Durante el desarrollo de este proyecto se aplicaron diversas buenas prácticas de seguridad y desarrollo:

- Uso de hashing seguro de contraseñas
- Autenticación basada en tokens JWT
- Validación de entradas mediante Pydantic
- Separación modular del código
- Uso de variables de entorno para información sensible
- Implementación de rutas protegidas

Estas prácticas son utilizadas en sistemas reales para proteger la información de los usuarios.

Conclusiones

- El desarrollo de este proyecto permitió comprender la importancia de implementar mecanismos de seguridad en las aplicaciones backend.
- Se pudo observar cómo herramientas como Passlib permiten proteger las contraseñas mediante hashing seguro, evitando almacenar información sensible en texto plano.
- Asimismo, el uso de JWT facilita la gestión de autenticación en APIs modernas, permitiendo identificar a los usuarios mediante tokens firmados digitalmente.

Este ejercicio permitió reforzar conceptos importantes relacionados con:

- seguridad en aplicaciones web
- autenticación basada en tokens
- protección de credenciales
- diseño de APIs seguras



Autor

Proyecto desarrollado como actividad académica del módulo de seguridad en APIs.

Autor:
Leider Arias Franco













