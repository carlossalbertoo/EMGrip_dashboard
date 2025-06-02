import streamlit as st

# Configurar la página
st.set_page_config(page_title="EMGrip - Iniciar sesión", page_icon="🔐", layout="centered")

# Ocultar sidebar y menú hamburguesa
st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"],
    [data-testid="collapsedControl"] {
        display: none;
    }
    body {
        background-color: #E3F2FD;
    }
    </style>
""", unsafe_allow_html=True)

# Simulación de usuarios válidos (demo)
usuarios_validos = {
    "invitado@emgrip.com": "123456",
    "admin@emgrip.com": "123456"
}

# Redirección si ya inició sesión
if st.session_state.get("logueado", False):
    st.switch_page("pages/1_🏚️ Inicio.py")

# Encabezado visual centrado
st.markdown("""
    <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
        <h1 style="font-size: 48px; font-weight: 800; font-family: 'Segoe UI', sans-serif; color: #1976D2;">
            EMGrip
        </h1>
        <p style="font-size: 20px; color: #333; font-family: 'Segoe UI', sans-serif; font-style: italic;">
            Sistema de monitoreo y rehabilitación funcional para STC
        </p>
    </div>
""", unsafe_allow_html=True)

with st.form("login_form"):
    st.markdown("#### Iniciar sesión", unsafe_allow_html=True)
    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    st.markdown("""
        <style>
            div.stButton > button {
                background-color: #1976D2;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
                transition: 0.3s;
            }
            div.stButton > button:hover {
                background-color: #125ea4;
            }
        </style>
    """, unsafe_allow_html=True)

    submit = st.form_submit_button("Iniciar sesión")

    if submit:
        if correo in usuarios_validos and usuarios_validos[correo] == contrasena:
            st.success("Inicio de sesión exitoso. Redirigiendo...")
            st.session_state.logueado = True
            st.rerun()
        else:
            st.error("Correo o contraseña incorrectos")

st.markdown("</div>", unsafe_allow_html=True)  # Cierre del contenedor
