# Seguridad y Autenticación con JWT y Passlib

---
Este proyecto implementa un sistema de gestión de acceso a recursos protegidos permitIENDO a los usuarios registrarse, iniciar sesión y
acceder a distintos recursos de la aplicación, siempre y cuando estén correctamente autenticados.
La aplicación se encarga de validar la identidad del usuario mediante un token JWT, el cual se genera al iniciar sesión y
se utiliza posteriormente para autorizar cada solicitud a la API.

El objetivo del sistema es controlar el acceso a la información y a las rutas disponibles, garantizando que únicamente
los usuarios autenticados puedan consumir los endpoints protegidos. Además, el proyecto incorpora un control de permisos basado en roles,
lo que permite diferenciar entre usuarios normales y administradores, otorgando accesos específicos según el tipo de usuario.

---
## Flujo de autenticación
### Registro de usuario (Register)
El flujo comienza cuando un usuario decide crear una cuenta en el sistema.

- El usuario ingresa un nombre de usuario, una contraseña y un rol desde el cliente (Streamlit).
- La información es enviada a la API a través del endpoint /register.
- El backend valida que el nombre de usuario no exista previamente.
- La contraseña ingresada nunca se almacena en texto plano: -Es procesada con Passlib (Argon2) para generar un hash seguro.
- El usuario es almacenado en la base de datos con su contraseña hasheada y su estado activo.

Como resultado, el sistema registra al usuario de forma segura y deja la cuenta lista para ser utilizada en el proceso de autenticación.

---
### Inicio de sesión (Login)

Una vez registrado, el usuario puede iniciar sesión en la aplicación.

- El usuario ingresa su nombre de usuario y contraseña.
- Los datos se envían al endpoint /login.
- El sistema busca el usuario en la base de datos.
- La contraseña ingresada es comparada con el hash almacenado mediante Passlib.
- Si las credenciales son válidas y el usuario está activo:
- Se genera un token JWT.
- El token incluye información relevante como:
     - El identificador del usuario (sub).
     - El rol del usuario (role).
     - La fecha de expiración (exp).

El token JWT es retornado al cliente y representa la sesión activa del usuario dentro del sistema.

---
### Verificación del token y acceso a recursos protegidos

Para acceder a rutas protegidas, el sistema utiliza el token JWT como mecanismo de verificación.

- El cliente envía el token en cada solicitud HTTP dentro del encabezado: Authorization: Bearer <token>
- La API intercepta la solicitud y extrae el token.
- El token es decodificado y validado:
  - Se verifica que la firma sea válida.
  - Se comprueba que el token no esté expirado.
- A partir del contenido del token, el sistema identifica al usuario.
- Se valida que el usuario exista y que se encuentre activo.
- Si todo es correcto, el acceso al recurso es concedido.

En el caso de rutas con restricciones adicionales (por ejemplo, solo administradores), el sistema valida también el rol del usuario, permitiendo o denegando el acceso según corresponda.

---

### Descripción del uso de Passlib

(hashing y verificación de contraseñas)

En este proyecto, Passlib se utiliza como la herramienta principal para proteger las contraseñas de los usuarios durante los procesos de registro e inicio de sesión. Su uso se integra de forma clara y controlada en el flujo de autenticación del sistema.

- El archivo de autenticación (auth_service.py), se configura Passlib creando un CryptContext con el algoritmo Argon2.
- define el contexto y las funciones reutilizables. pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
 - Esto asegura que todo el sistema use un único estándar de hashing.
- Cuando el usuario se registra desde el cliente (Streamlit), la API recibe un username y password por el endpoint /register.
- El sistema valida que el usuario no exista.
- Llama a hashear_password(password) (Passlib).
- Guarda en base de datos solo el hash, no la contraseña original.
- La base de datos nunca recibe la contraseña real; solo almacena un hash seguro.
- Cuando el usuario inicia sesión por /login, el sistema:
  - Busca el usuario en la base de datos.
  - Recupera hashed_password.
  - Usa verificar_password(plain, hashed) para comprobar si la contraseña ingresada coincide con el hash.
- No se “desencripta” nada. Passlib hace una validación segura comparando el texto ingresado contra el hash almacenado

### Resultado
- Las contraseñas no se guardan en texto plano.
- El sistema puede autenticar usuarios sin revelar información sensible.
- Si alguien accede a la base de datos, no obtiene contraseñas reales, solo hashes irreversibles.

### Ejemplo del payload JWT generado y su decodificación

En este proyecto, el token JWT se utiliza como el mecanismo principal para mantener la sesión del usuario y autorizar el acceso a los recursos protegidos. El token se genera durante el proceso de inicio de sesión y posteriormente es validado en cada solicitud a la API.

1. Cuando un usuario inicia sesión correctamente en el endpoint /login, el sistema genera un token JWT utilizando la función crear_token.

```python
token = crear_token({
    "sub": user.username,
    "role": user.role
})
```
El payload del token incluye:

- sub: identifica al usuario autenticado.
- role: define el rol del usuario dentro del sistema.
- exp: fecha de expiración del token (agregada automáticamente).

2. Una vez creado, el contenido del token JWT (payload) tiene una estructura similar a la siguiente:
   
```python
{
  "sub": "juan_perez",
  "role": "admin",
  "exp": 1733854800
}
```

Este payload permite al sistema identificar quién es el usuario, qué permisos tiene y hasta cuándo el token es válido.

3. Después del login, el cliente almacena el token y lo envía en cada petición a rutas protegidas usando el encabezado HTTP:
```python
Authorization: Bearer <token>
```
De esta forma, el token acompaña cada solicitud como prueba de autenticación.

4. Cuando la API recibe una solicitud protegida:
 - Extrae el token del encabezado Authorization.
 - Llama a la función verificar_token.
 - Decodifica el token utilizando la clave secreta y el algoritmo configurado.
 - Valida la firma y la fecha de expiración.
 - Retorna el payload si el token es válido.
```python
payload = verificar_token(token)
```
Si el token es inválido o ha expirado, el acceso es denegado automáticamente.

5. Una vez decodificado el token:
 - Se obtiene el valor de sub para identificar al usuario.
 - Se consulta la base de datos para validar que el usuario exista y esté activo.
 - Se usa el valor de role para restringir o permitir el acceso a ciertos recursos.

Gracias a este proceso, el sistema garantiza que cada solicitud esté asociada a un usuario válido y autorizado.

---

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
