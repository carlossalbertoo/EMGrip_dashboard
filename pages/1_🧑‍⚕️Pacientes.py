import streamlit as st 

st.set_page_config(page_title="Pacientes - EMGrip", page_icon="🧑‍⚕️", layout="wide")

# Sección principal con estilo visual consistente
st.markdown("""
    <div style="background-color:#1976D2; padding:25px 30px; border-radius:10px;">
        <h1 style="
            color:white;
            margin:0;
            font-weight:900;
            font-size:42px;
            font-family:'Segoe UI', sans-serif;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);">
            Gestión de pacientes
        </h1>
        <p style="
            color:white;
            font-weight:500;
            font-size:20px;
            margin:5px 0 0 0;
            font-family:'Segoe UI', sans-serif;
            letter-spacing: 0.5px;
            font-style: italic;">
            Aquí se mostrarán los detalles, historial clínico y estado actual de los pacientes monitoreados
        </p>
    </div>
""", unsafe_allow_html=True)
