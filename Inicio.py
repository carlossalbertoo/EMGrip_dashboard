import streamlit as st
import base64

st.set_page_config(page_title="Dashboard EMGrip", page_icon="🦾", layout="wide")

# ---------- Encabezado principal ----------
col1, col2 = st.columns([1, 7])

with col1:
    st.image("recursos/logo.png", width=150)

with col2:
    st.markdown("""
        <div style="background-color:#1976D2; padding:25px 30px; border-radius:10px;">
            <h1 style="
                color:white;
                margin:0;
                font-weight:900;
                font-size:42px;
                font-family:'Segoe UI', sans-serif;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);">
                Dashboard EMGrip
            </h1>
            <p style="
                color:white;
                font-weight:500;
                font-size:20px;
                margin:5px 0 0 0;
                font-family:'Segoe UI', sans-serif;
                letter-spacing: 0.5px;
                font-style: italic;">
                Monitoreo eficaz del Síndrome de Túnel Carpiano
            </p>
            
        </div>
    """, unsafe_allow_html=True)

# ---------- Hero message ----------
st.markdown("""
    <div style="text-align:center; margin-top:30px; margin-bottom:5px;">
        <p style="font-size:22px; font-style:italic; color:#333; font-family:'Segoe UI', sans-serif;">
            Visión: Transformar el tratamiento de lesiones en una experiencia personalizada, medible y accesible para todos.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align:center; margin-top:5px; margin-bottom:15px;">
        <p style="font-size:22px; font-style:italic; color:#333; font-family:'Segoe UI', sans-serif;">
            Misión: Brindar un sistema accesible, cuantificable y no invasivo para el monitoreo y rehabilitación de STC.
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------- Tarjetas de resumen ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style="background-color:#E3F2FD; border-left:5px solid #1976D2; border-radius:10px; padding:15px;">
            <h2 style="margin:0; color:#1976D2;">12</h2>
            <p style="margin:0;">Pacientes en monitoreo</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background-color:#E3F2FD; border-left:5px solid #1976D2; border-radius:10px; padding:15px;">
            <h2 style="margin:0; color:#1976D2;">8</h2>
            <p style="margin:0;">Pacientes de alta</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="background-color:#E3F2FD; border-left:5px solid #1976D2; border-radius:10px; padding:15px;">
            <h2 style="margin:0; color:#1976D2;">20</h2>
            <p style="margin:0;">Pacientes totales</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------- Frase motivacional ----------
st.markdown("""
    <div style="text-align:center; margin:30px 0;">
        <h2 style="font-size:24px; font-style:italic; font-family:'Segoe UI', sans-serif; color:#1976D2;">
            “El primer paso hacia tu recuperación es medible”
        </h2>
    </div>
""", unsafe_allow_html=True)

# ---------- Modelos disponibles ----------
cols = st.columns(2)

modelos = [
    {
        "nombre": "Ortesis de inmovilización",
        "ruta": "recursos/ortesis (2).png",
        "descripcion": [
            "Medidas: 16x12 cm",
            "Material: PET-G reforzado",
            "Tela: neopreno y licra",
            "Ajuste flexible con velcro",
            "Resistencia: 300 N",
            "Uso recomendado: etapas intermedias/avanzadas"
        ]
    },
    {
        "nombre": "Dispositivo de monitoreo EMG",
        "ruta": "recursos/EMG.png",
        "descripcion": [
            "Sensor EMG incorporado (1 canal)",
            "Pantalla LCD y botones interactivos",
            "Switch de alimentación",
            "Electrodos y baterías incluidas",
            "Acceso a reportes y análisis de datos",
            "Capacitación introductoria de uso"
        ]
    },
]

def cargar_imagen_base64(ruta):
    with open(ruta, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

for i, modelo in enumerate(modelos):
    with cols[i]:
        img_base64 = cargar_imagen_base64(modelo["ruta"])
        descripcion_lista = "".join([f"<li>{item}</li>" for item in modelo["descripcion"]])
        st.markdown(
            f"""
            <div style='text-align: center;'>
                <img src='data:image/jpeg;base64,{img_base64}' style='height: 320px; object-fit: cover; border-radius: 10px; margin-bottom:10px;' />
                <p style='font-weight: bold; font-size:18px; color:#1976D2; margin-bottom:5px;'>{modelo['nombre']}</p>
                <div style='display: inline-block; text-align: left; margin: 0 auto;'>
                    <ul style='font-size:14px; color:#333; list-style-position: inside;'>{descripcion_lista}</ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
# ---------- Botones inferiores centrados ----------
col_btn1, col_spacer, col_btn2 = st.columns([8, 1, 8])

with col_btn1:
    st.markdown(
        """
        <div style='text-align: center;'>
            <a href='#' style='display:inline-block; padding:10px 24px; background-color:#1976D2; color:white; border-radius:8px; text-decoration:none; font-weight:bold; font-size:16px;'>🔍 Ver detalles adicionales</a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_btn2:
    st.markdown(
        """
        <div style='text-align: center;'>
            <a href='#' style='display:inline-block; padding:10px 24px; background-color:#1976D2; color:white; border-radius:8px; text-decoration:none; font-weight:bold; font-size:16px;'>📩 Contactar equipo EMGrip</a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------- Capacitaciones futuras ----------
st.subheader("Capacitaciones futuras")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    <div style="border: 1px solid #1976D2; border-radius: 10px; padding: 15px;">
        <b>Curso:</b> Tratamiento actual del STC<br>
        👉 Más información
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div style="border: 1px solid #1976D2; border-radius: 10px; padding: 15px;">
        <b>Taller:</b> Evaluación EMG en pacientes con STC<br>
        👉 Más información
    </div>
    """, unsafe_allow_html=True)

# Cargar el archivo PDF
with open("Manual_EMGrip.pdf", "rb") as file:
    pdf_bytes = file.read()

# Título centrado
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center;'>
        <p style='font-size:18px; font-weight:500;'>¿Necesitas ayuda con el sistema?</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Centrar botón usando columnas
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    st.download_button(
        label="📄 Descargar manual de usuario",
        data=pdf_bytes,
        file_name="Manual_EMGrip.pdf",
        mime="application/pdf",
        key="manual_emgrip",
        help="Haz clic para obtener una copia del manual en PDF."
    )

