import streamlit as st
import requests

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="Acceso a Recursos Protegidos",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Sistema de Gestión de Acceso a Recursos Protegidos")

# ============================================================
# ESTADO DE SESIÓN
# ============================================================
if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
def auth_headers():
    if not st.session_state.token:
        return {}
    return {"Authorization": f"Bearer {st.session_state.token}"}


def cargar_usuario_actual():
    """
    Obtiene los datos del usuario autenticado desde la API.
    """
    if not st.session_state.token:
        return

    try:
        r = requests.get(
            f"{API_BASE_URL}/me",
            headers=auth_headers()
        )
        if r.status_code == 200:
            st.session_state.user = r.json()
        else:
            st.session_state.user = None
    except Exception as e:
        st.error(f"❌ Error al obtener usuario: {e}")


# ============================================================
# MENÚ
# ============================================================
menu = [
    "Registro",
    "Login",
    "Mi Perfil",
    "Recursos",
    "Admin"
]

choice = st.sidebar.selectbox("Menú", menu)

# ============================================================
# REGISTRO
# ============================================================
if choice == "Registro":
    st.subheader("🧾 Registro de nuevo usuario")

    with st.form("register_form", clear_on_submit=True):
        username = st.text_input(
            "Usuario",
            help="Entre 3 y 50 caracteres"
        )
        password = st.text_input(
            "Contraseña",
            type="password",
            help="Mínimo 6 caracteres"
        )
        role = st.selectbox(
            "Rol",
            ["user", "admin"],
            help="Rol del usuario"
        )

        submit = st.form_submit_button("Registrar")

        if submit:
            if len(username) < 3 or len(username) > 50:
                st.error("❌ El usuario debe tener entre 3 y 50 caracteres")
            elif len(password) < 6:
                st.error("❌ La contraseña debe tener al menos 6 caracteres")
            else:
                data = {
                    "username": username,
                    "password": password,
                    "role": role
                }

                try:
                    r = requests.post(
                        f"{API_BASE_URL}/register",
                        json=data
                    )

                    if r.status_code == 201:
                        st.success(
                            f"✅ Usuario '{username}' creado correctamente"
                        )
                    else:
                        st.error(
                            f"❌ {r.json().get('detail', r.text)}"
                        )
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")

# ============================================================
# LOGIN
# ============================================================
elif choice == "Login":
    st.subheader("🔑 Iniciar sesión")

    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Usuario")
        password = st.text_input(
            "Contraseña",
            type="password"
        )

        submit = st.form_submit_button("Entrar")

        if submit:
            if not username or not password:
                st.warning("⚠️ Completa usuario y contraseña")
            else:
                try:
                    r = requests.post(
                        f"{API_BASE_URL}/login",
                        json={
                            "username": username,
                            "password": password
                        }
                    )

                    if r.status_code == 200:
                        st.session_state.token = r.json()["access_token"]
                        cargar_usuario_actual()
                        st.success("✅ Login exitoso")
                    else:
                        st.error("❌ Credenciales inválidas")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")

    if st.session_state.token and st.session_state.user:
        st.info(
            f"Sesión activa: "
            f"{st.session_state.user['username']} "
            f"({st.session_state.user['role']})"
        )

        if st.button("🚪 Cerrar sesión"):
            st.session_state.token = None
            st.session_state.user = None
            st.success("Sesión cerrada correctamente")
            st.rerun()

# ============================================================
# PERFIL
# ============================================================
elif choice == "Mi Perfil":
    st.subheader("👤 Mi perfil")

    if not st.session_state.token:
        st.warning("⚠️ Debes iniciar sesión")
    else:
        cargar_usuario_actual()

        if st.session_state.user:
            st.json(st.session_state.user)
        else:
            st.error("❌ No se pudo cargar el perfil")

# ============================================================
# RECURSOS GENERALES
# ============================================================
elif choice == "Recursos":
    st.subheader("📦 Recursos protegidos")

    if not st.session_state.token:
        st.warning("⚠️ Inicia sesión para acceder")
    else:
        try:
            r = requests.get(
                f"{API_BASE_URL}/resources",
                headers=auth_headers()
            )

            if r.status_code == 200:
                st.success("✅ Acceso permitido")
                st.json(r.json())
            else:
                st.error(
                    f"❌ {r.json().get('detail', r.text)}"
                )
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")

# ============================================================
# RECURSOS ADMIN
# ============================================================
elif choice == "Admin":
    st.subheader("🛡️ Recursos administrativos")

    if not st.session_state.token:
        st.warning("⚠️ Inicia sesión")
    else:
        try:
            r = requests.get(
                f"{API_BASE_URL}/admin/resources",
                headers=auth_headers()
            )

            if r.status_code == 200:
                st.success("✅ Acceso administrador concedido")
                st.json(r.json())
            else:
                st.error(
                    f"❌ {r.json().get('detail', r.text)}"
                )
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")
