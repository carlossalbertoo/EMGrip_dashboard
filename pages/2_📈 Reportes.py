import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Base import (
    obtener_datos_filtrados_rectificados,
    obtener_resultados_reclutamiento,
    obtener_resultados_fatiga,
    graficar_dia_reclutamiento,
    graficar_dia_fatiga,
    velocimetro_isb
)
from graficos import graficar_deteccion_contraccion, graficar_rms_bloques_con_pendiente
import io
import pandas as pd

st.set_page_config(page_title="Reportes - EMGrip", page_icon="📈", layout="wide")

# ---------- Encabezado principal ----------
st.markdown("""
    <div style="background-color:#1976D2; padding:25px 30px; border-radius:10px;">
        <h1 style="
            color:white;
            margin:0;
            font-weight:900;
            font-size:42px;
            font-family:'Segoe UI', sans-serif;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);">
            Reportes de pacientes
        </h1>
        <p style="
            color:white;
            font-weight:500;
            font-size:20px;
            margin:5px 0 0 0;
            font-family:'Segoe UI', sans-serif;
            letter-spacing: 0.5px;
            font-style: italic;">
            Análisis clínico de las señales EMG registradas
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------- Navegación estilo calendario -----------
st.subheader("📅 Selecciona periodo de análisis")

anio_seleccionado = st.selectbox("Año", ["2023", "2024", "2025"], index=2)

if anio_seleccionado == "2025":
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", 
             "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_seleccionado = st.selectbox("Mes", meses, index=5)  # Junio

    if mes_seleccionado == "Junio":
        semanas = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]
        semana_seleccionada = st.selectbox("Semana", semanas, index=0)

        if semana_seleccionada == "Semana 1":
            dias = ["Día 1", "Día 2", "Día 3", "Día 4", "Día 5", "Día 6", "Día 7", "Días 1–7"]
            dia_seleccionado = st.selectbox("Día", dias)

            if "confirmado" not in st.session_state:
                st.session_state.confirmado = False

            if not st.session_state.confirmado:
                if st.button("✅ Confirmar"):
                    st.session_state.confirmado = True

            if st.session_state.confirmado:
                datos_filtrados_rectificados = obtener_datos_filtrados_rectificados()
                resultados_reclutamiento = obtener_resultados_reclutamiento(datos_filtrados_rectificados)
                resultados_fatiga = obtener_resultados_fatiga(datos_filtrados_rectificados)

            # Sección posterior a la confirmación
            if st.session_state.confirmado:
                st.markdown("---")
                st.markdown(f"""
                    <div style="background-color:#BBDEFB; padding:20px; border-radius:10px;">
                        <h3 style="margin:0; font-size:24px;"> Reporte de señales EMG</h3>
                        <p style="margin:0;">Visualizando: <b>{dia_seleccionado} de {mes_seleccionado} de {anio_seleccionado}</b></p>
                    </div>
                """, unsafe_allow_html=True)

                # --- Crear DataFrame con datos filtrados y rectificados ---
                rows = []
                for dia, bloques in datos_filtrados_rectificados.items():
                    max_len = max(len(v) for v in bloques.values())
                    for i in range(max_len):
                        row = {"Día": dia}
                        for bloque, valores in bloques.items():
                            row[bloque] = valores[i] if i < len(valores) else ""
                        rows.append(row)

                df_descarga = pd.DataFrame(rows)

                # --- Crear CSV en memoria ---
                csv_buffer = io.StringIO()
                df_descarga.to_csv(csv_buffer, index=False)
                csv_bytes = csv_buffer.getvalue().encode()

                # Crear columnas para centrar visualmente el botón
                col1, col2, col3 = st.columns([2, 1, 2])  # 2 ocupa más espacio al centro

                with col2:
                    # Estilizar el botón con CSS
                    st.markdown("""
                        <style>
                        div.stDownloadButton > button {
                            background-color: #1E88E5;
                            color: white;
                            font-size: 18px;
                            padding: 14px 28px;
                            border-radius: 8px;
                            border: none;
                        }
                        div.stDownloadButton > button:hover {
                            background-color: #1565C0;
                            color: white;
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    st.download_button(
                        label="⬇📄Descargar señales EMG procesadas",
                        data=csv_bytes,
                        file_name="EMG_datos_filtrados.csv",
                        mime="text/csv",
                        key="descarga_emg_centrada"
                    )

                st.markdown("### Selecciona tipo de análisis")

                col_a, col_b = st.columns([1, 1])
                with col_a:
                    mostrar_reclutamiento = st.button("💡 Reclutamiento motor", use_container_width=True)
                with col_b:
                    mostrar_fatiga = st.button("⚡ Fatiga muscular", use_container_width=True)


                if mostrar_reclutamiento:
                    st.markdown("----")
                    st.markdown(f"""
                        <div style="background-color:#FFFFFF; padding:20px; border-radius:10px;">
                            <h3 style="margin:0; font-size:32px;"> Análisis de Reclutamiento Motor</h3>
                            <p style="margin:0;font-size:18px;">Este análisis evalúa la capacidad del músculo abductor corto del pulgar para activarse mediante contracciones voluntarias y repetidas.</p>
                            <p style="margin:0;font-size:18px;">-Ejercicio realizado: 5 repeticiones "abducción en L" de 3 segundos cada una y descanso de 3 segundos entre ellas.</p>
                            <p style="margin:0;font-size:18px;">-Parámetro medido: Amplitud RMS por contracción y amplitud RMS promedio.</p>
                            <p style="margin:0;font-size:18px;">Gráficos mostrados:</p>
                            <p style="margin:0;font-size:18px;">     1. Señal procesada con contracción detectada.</p>
                            <p style="margin:0;font-size:18px;">     2. Gráfico de barras de amplitud en cada contracción.</p>
                            <p style="margin:0;font-size:18px;">     3. Gráfico de barras de activación total.</p>
                            <p style="margin:0;font-size:18px;">     4. Índice de simetría entre ambas manos acorde a la activación muscular.</p>
                                                  
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("----")
                    st.markdown(
                        "<h3 style='text-align: center;'>Resultados del análisis</h3>",
                        unsafe_allow_html=True
                    )
                    st.markdown("----")


                    try:
                        if dia_seleccionado == "Días 1–7":
                            # Cálculo de promedio semanal de activación (basado en promedios diarios)
                            promedio_derecha_diario = []
                            promedio_izquierda_diario = []

                            for dia in range(1, 8):
                                nombre_dia = f"Dia {dia}"
                                datos = resultados_reclutamiento[nombre_dia]
                                
                                # Calcular promedio diario por mano
                                promedio_derecha_dia = np.mean(datos["rms_derecha"])
                                promedio_izquierda_dia = np.mean(datos["rms_izquierda"])

                                promedio_derecha_diario.append(promedio_derecha_dia)
                                promedio_izquierda_diario.append(promedio_izquierda_dia)

                            # Promedio semanal de los promedios diarios
                            promedio_derecha = np.mean(promedio_derecha_diario)
                            promedio_izquierda = np.mean(promedio_izquierda_diario)

                            # Gráfica con estilo limpio y horizontal
                            fig, ax = plt.subplots(figsize=(9, 1.5))

                            categorias = ["Derecha", "Izquierda"]
                            valores = [promedio_derecha, promedio_izquierda]
                            colores = ["blue", "green"]

                            bars = ax.barh(categorias, valores, color=colores, height=0.4, edgecolor='none')

                            ax.set_xlim(0, 1000)
                            ax.set_title("Promedio Semanal de Activación Total", fontsize=12)
                            ax.set_xlabel("Promedio de suma de amplitudes (mV)", fontsize=10)
                            ax.bar_label(bars, padding=4, fontsize=10)

                            # Limpiar visualmente
                            for spine in ax.spines.values():
                                spine.set_visible(False)
                            ax.xaxis.set_ticks_position('none')
                            ax.yaxis.set_ticks_position('none')
                            ax.set_xticklabels([])
                            ax.grid(False)

                            plt.tight_layout()
                            st.pyplot(fig)

                            # ISB
                            isb = (1 - abs(promedio_izquierda - promedio_derecha) / max(promedio_izquierda, promedio_derecha)) * 100

                            # Título centrado y más grande
                            st.markdown(
                                """
                                <h2 style='text-align: center; color: #000000;'>Índice de Simetría Bilateral</h2>
                                """,
                                unsafe_allow_html=True
                            )

                            # Gráfica + Leyenda alineadas
                            col1, col2 = st.columns([5, 2])

                            with col1:
                                fig_isb = velocimetro_isb(isb)
                                st.plotly_chart(fig_isb, use_container_width=True)

                            with col2:
                                st.markdown("<div style='padding-top: 150px;'>", unsafe_allow_html=True)  # Ajusta este padding para centrar más o menos
                                st.markdown("<span style='color:#21468D; font-size:20px;'>■ Asimetría (0–60%)</span>", unsafe_allow_html=True)
                                st.markdown("<span style='color:#1B71C7; font-size:20px;'>■ Desproporción (60–80%)</span>", unsafe_allow_html=True)
                                st.markdown("<span style='color:#38b4fc; font-size:20px;'>■ Normal (80–100%)</span></div>", unsafe_allow_html=True)

                        else:
                            nombre_dia = "Dia " + dia_seleccionado.split(" ")[1]
                            graficar_dia_reclutamiento(nombre_dia, resultados_reclutamiento)

                    except Exception as e:
                        st.error(f"⚠️ No se pudo generar el reporte para {dia_seleccionado}. Error: {e}")

                elif mostrar_fatiga:
                    st.markdown("----")
                    st.markdown(f"""
                        <div style="background-color:#FFFFFF; padding:20px; border-radius:10px;">
                            <h3 style="margin:0; font-size:24px;"> Análisis de Fatiga Muscular</h3>
                            <p style="margin:0;font-size:18px;">Este análisis permite identificar signos de fatiga mediante una contracción sostenida del músculo abductor corto del pulgar.</p>
                            <p style="margin:0;font-size:18px;">-Ejercicio realizado: contracción máxima sostenida durante 30 segundos "posición de L".</p>
                            <p style="margin:0;font-size:18px;">-Parámetros medidos: duración máxima de contracción, amplitud RMS.</p>
                            <p style="margin:0;font-size:18px;">Gráficos mostrados:</p>
                            <p style="margin:0;font-size:18px;">     1. Señal procesada con contracción detectada.</p>
                            <p style="margin:0;font-size:18px;">     2. Pendiente de caída de RMS por bloque de 10 segundos.</p>
                            <p style="margin:0;font-size:18px;">     3. Duración máxima de contracción por día.</p>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("----")
                    st.markdown(
                        "<h3 style='text-align: center;'>Resultados del análisis</h3>",
                        unsafe_allow_html=True
                    )
                    st.markdown("----")

                    try:
                        if dia_seleccionado == "Días 1–7":
                            dias = [f"Dia {i}" for i in range(1, 8)]
                            duraciones_d = [resultados_fatiga[d]["duracion_derecha"] for d in dias]
                            duraciones_i = [resultados_fatiga[d]["duracion_izquierda"] for d in dias]

                            fig, ax = plt.subplots(figsize=(9, 4))
                            ax.plot(dias, duraciones_d, marker='o', color='blue', label="Mano Derecha")
                            ax.plot(dias, duraciones_i, marker='o', color='green', label="Mano Izquierda")
                            ax.set_title("Duración Máxima de Contracción – Fatiga Muscular (Semana Completa)")
                            ax.set_ylabel("Duración (s)")
                            ax.set_xlabel("Día")
                            ax.set_ylim(20, 30)
                            ax.grid(True, linestyle='--', alpha=0.5)
                            ax.legend()
                            st.pyplot(fig)

                            # Cambio porcentual de pendiente
                            datos_dia1 = resultados_fatiga["Dia 1"]
                            datos_dia7 = resultados_fatiga["Dia 7"]

                            def cambio_porcentual(pend_1, pend_7):
                                if pend_1 == 0:
                                    return float('inf')
                                return ((pend_7 - pend_1) / abs(pend_1)) * 100

                            pend_1_der = datos_dia1["pendiente_derecha"]
                            pend_1_izq = datos_dia1["pendiente_izquierda"]
                            pend_7_der = datos_dia7["pendiente_derecha"]
                            pend_7_izq = datos_dia7["pendiente_izquierda"]

                            cambio_der = cambio_porcentual(pend_1_der, pend_7_der)
                            cambio_izq = cambio_porcentual(pend_1_izq, pend_7_izq)

                            st.markdown("#### Cambio porcentual en la pendiente de fatiga")

                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown("<h4 style='text-align: left;'>🟦 Mano Derecha</h4>", unsafe_allow_html=True)
                                st.metric(label="", value=f"{cambio_der:.1f} %", delta=f"{pend_7_der - pend_1_der:.2f} mV/s")

                            with col2:
                                st.markdown("<h4 style='text-align: left;'>🟩 Mano Izquierda</h4>", unsafe_allow_html=True)
                                st.metric(label="", value=f"{cambio_izq:.1f} %", delta=f"{pend_7_izq - pend_1_izq:.2f} mV/s")

                        else:
                            nombre_dia = "Dia " + dia_seleccionado.split(" ")[1]

                            fatiga_derecha = datos_filtrados_rectificados[nombre_dia]["fatiga_derecha"]
                            fatiga_izquierda = datos_filtrados_rectificados[nombre_dia]["fatiga_izquierda"]
                            resultados = resultados_fatiga[nombre_dia]

                            ini_d = resultados["inicio_derecha"]
                            fin_d = resultados["fin_derecha"]
                            ini_i = resultados["inicio_izquierda"]
                            fin_i = resultados["fin_izquierda"]
                            rms_d = resultados["rms_derecha"]
                            rms_i = resultados["rms_izquierda"]
                            tiempos = resultados["tiempos"]

                            st.markdown("#### Duración máxima de contracción sostenida:")

                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown(f"""
                                    <div style='background-color:#E3F2FD; padding:20px 25px; border-radius:10px;'>
                                        <p style='margin:0; font-size:18px; font-weight:500;'>🟦 Mano Derecha</p>
                                        <p style='margin:0; font-size:32px; font-weight:bold;'>{resultados['duracion_derecha']:.2f} s</p>
                                    </div>
                                """, unsafe_allow_html=True)

                            with col2:
                                st.markdown(f"""
                                    <div style='background-color:#E3F2FD; padding:20px 25px; border-radius:10px;'>
                                        <p style='margin:0; font-size:18px; font-weight:500;'>🟩 Mano Izquierda</p>
                                        <p style='margin:0; font-size:32px; font-weight:bold;'>{resultados['duracion_izquierda']:.2f} s</p>
                                    </div>
                                """, unsafe_allow_html=True)

                            graficar_deteccion_contraccion(
                                fatiga_derecha, fatiga_izquierda,
                                ini_d, fin_d, ini_i, fin_i,
                                dia=nombre_dia
                            )

                            st.markdown("#### Pendiente de fatiga (bloques de 10 segundos)")
                            graficar_rms_bloques_con_pendiente(
                                tiempos, rms_d, rms_i,
                                dia=nombre_dia
                            )

                    except Exception as e:
                        st.error(f"⚠️ No se pudo generar el reporte para {dia_seleccionado}. Error: {e}")


        else:
            st.info("📌 Funcionalidad disponible solo para Semana 1 de Junio por ahora.")
    else:
        st.info("📌 Actualmente solo está disponible el mes de Junio 2025 para demostración.")
else:
    st.info("📌 Actualmente solo está disponible el año 2025 para demostración.")

