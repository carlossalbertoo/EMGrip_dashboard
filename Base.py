# === Importación de módulos ===
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
from funciones import (
    filtro_pasabanda, clipping_intermedio, detectar_eventos,
    calcular_rms_por_evento, obtener_contracciones_alineadas,
    calcular_duracion_contraccion, calcular_rms_bloques
)
from graficos import (
    graficar_eventos, graficar_rms_barras, graficar_activacion_total,
    graficar_deteccion_contraccion, graficar_rms_bloques_con_pendiente
)

# === Función para obtener datos filtrados y rectificados ===
def obtener_datos_filtrados_rectificados():
    fs = 10
    lowcut = 0.2
    highcut = 4.5
    nombre_documento = "EMG_data"

    alcance = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credenciales_dict = dict(st.secrets["gcp_service_account"])
    credenciales = ServiceAccountCredentials.from_json_keyfile_dict(credenciales_dict, alcance)
    cliente = gspread.authorize(credenciales)

    datos_filtrados = {}

    for i in range(1, 8):
        nombre_hoja = f"Dia {i}"
        hoja = cliente.open(nombre_documento).worksheet(nombre_hoja)
        valores = hoja.get_all_values()

        bloques = {
            "reclutamiento_derecha": [],
            "fatiga_derecha": [],
            "reclutamiento_izquierda": [],
            "fatiga_izquierda": []
        }

        for fila in valores[2:]:
            try: bloques["reclutamiento_derecha"].append(float(fila[0]))
            except: pass
            try: bloques["fatiga_derecha"].append(float(fila[1]))
            except: pass
            try: bloques["reclutamiento_izquierda"].append(float(fila[2]))
            except: pass
            try: bloques["fatiga_izquierda"].append(float(fila[3]))
            except: pass

        procesados = {}
        for clave, señal in bloques.items():
            señal_array = np.array(señal)
            if len(señal_array) > 27:
                señal_filtrada = filtro_pasabanda(señal_array, lowcut, highcut, fs)
                señal_rectificada = np.abs(señal_filtrada)
            else:
                señal_rectificada = np.abs(señal_array)
            procesados[clave] = señal_rectificada.tolist()

        datos_filtrados[nombre_hoja] = procesados

    return datos_filtrados

# === Función para obtener resultados de reclutamiento ===
def obtener_resultados_reclutamiento(datos_filtrados):
    resultados = {}
    fs = 10

    for dia in range(1, 8):
        nombre_dia = f"Dia {dia}"
        try:
            reclutamiento_derecha = datos_filtrados[nombre_dia]["reclutamiento_derecha"]
            reclutamiento_izquierda = datos_filtrados[nombre_dia]["reclutamiento_izquierda"]

            derecha_clip = clipping_intermedio(reclutamiento_derecha)
            izquierda_clip = clipping_intermedio(reclutamiento_izquierda)

            eventos_derecha = detectar_eventos(derecha_clip, umbral_inicio=450, umbral_fin=600, fs=fs, min_duracion_s=2)
            eventos_izquierda = detectar_eventos(izquierda_clip, umbral_inicio=450, umbral_fin=600, fs=fs, min_duracion_s=2)

            rms_derecha = calcular_rms_por_evento(reclutamiento_derecha, eventos_derecha)
            rms_izquierda = calcular_rms_por_evento(reclutamiento_izquierda, eventos_izquierda)

            valores_rms_derecha = [rms for _, _, rms in rms_derecha]
            valores_rms_izquierda = [rms for _, _, rms in rms_izquierda]

            longitud_contraccion = 20
            segmentos_derecha = obtener_contracciones_alineadas(derecha_clip, eventos_derecha, longitud_contraccion)
            segmentos_izquierda = obtener_contracciones_alineadas(izquierda_clip, eventos_izquierda, longitud_contraccion)

            promedio_derecha = np.mean(segmentos_derecha, axis=0) if len(segmentos_derecha) > 0 else np.zeros(longitud_contraccion)
            promedio_izquierda = np.mean(segmentos_izquierda, axis=0) if len(segmentos_izquierda) > 0 else np.zeros(longitud_contraccion)

            suma_derecha = np.sum(promedio_derecha)
            suma_izquierda = np.sum(promedio_izquierda)

            resultados[nombre_dia] = {
                "signal_derecha": reclutamiento_derecha,
                "signal_izquierda": reclutamiento_izquierda,
                "eventos_derecha": eventos_derecha,
                "eventos_izquierda": eventos_izquierda,
                "rms_derecha": valores_rms_derecha,
                "rms_izquierda": valores_rms_izquierda,
                "promedio_derecha": promedio_derecha,
                "promedio_izquierda": promedio_izquierda,
                "suma_derecha": suma_derecha,
                "suma_izquierda": suma_izquierda
            }

        except Exception as e:
            st.error(f"❌ Error procesando {nombre_dia}: {e}")

    return resultados

# === Función para obtener resultados de fatiga ===
def obtener_resultados_fatiga(datos_filtrados):
    fs = 10
    duracion_bloque_s = 10
    muestras_por_bloque = fs * duracion_bloque_s
    umbral_fatiga = 600

    resultados = {}

    for dia in range(1, 8):
        nombre_dia = f"Dia {dia}"
        fatiga_derecha = datos_filtrados[nombre_dia]["fatiga_derecha"]
        fatiga_izquierda = datos_filtrados[nombre_dia]["fatiga_izquierda"]

        dur_d, ini_d, fin_d = calcular_duracion_contraccion(fatiga_derecha, umbral_fatiga, fs)
        dur_i, ini_i, fin_i = calcular_duracion_contraccion(fatiga_izquierda, umbral_fatiga, fs)

        rms_d = calcular_rms_bloques(fatiga_derecha, muestras_por_bloque)
        rms_i = calcular_rms_bloques(fatiga_izquierda, muestras_por_bloque)
        tiempos = np.arange(len(rms_d)) * duracion_bloque_s

        pendiente_derecha, _ = np.polyfit(tiempos, rms_d, 1)
        pendiente_izquierda, _ = np.polyfit(tiempos, rms_i, 1)

        resultados[nombre_dia] = {
            "duracion_derecha": dur_d,
            "inicio_derecha": ini_d,
            "fin_derecha": fin_d,
            "duracion_izquierda": dur_i,
            "inicio_izquierda": ini_i,
            "fin_izquierda": fin_i,
            "rms_derecha": rms_d,
            "rms_izquierda": rms_i,
            "tiempos": tiempos,
            "pendiente_derecha": pendiente_derecha,
            "pendiente_izquierda": pendiente_izquierda
        }

    return resultados

# === Funciones auxiliares de visualización ===
def graficar_dia_reclutamiento(nombre_dia, resultados):
    datos = resultados[nombre_dia]
    graficar_eventos(datos["signal_derecha"], datos["eventos_derecha"], datos["signal_izquierda"], datos["eventos_izquierda"], dia=nombre_dia)
    graficar_rms_barras(datos["rms_derecha"], datos["rms_izquierda"], dia=nombre_dia)
    graficar_activacion_total(datos["rms_derecha"], datos["rms_izquierda"], dia=nombre_dia)

def graficar_dia_fatiga(nombre_dia, resultados):
    datos = resultados[nombre_dia]
    graficar_deteccion_contraccion(datos["rms_derecha"], datos["rms_izquierda"], datos["tiempos"], nombre_dia)
    graficar_rms_bloques_con_pendiente(datos["rms_derecha"], datos["rms_izquierda"], datos["tiempos"], nombre_dia)

def velocimetro_isb(isb):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=isb,
        number={'suffix': "%", 'font': {'size': 48, 'color': '#21468D'}},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickvals': [0, 20, 40, 60, 80, 100],
                'ticktext': ["0%", "20%", "40%", "60%", "80%", "100%"],
                'tickfont': {'color': 'black', 'size': 20}
            },
            'bar': {'color': "#FFFFFF", 'thickness': 0.05},
            'steps': [
                {'range': [0, 60], 'color': "#21468D"},
                {'range': [60, 80], 'color': "#1B71C7"},
                {'range': [80, 100], 'color': "#38b4fc"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 1,
                'value': isb
            }
        }
    ))
    fig.update_layout(height=500, margin={'t': 50, 'b': 80, 'l': 20, 'r': 20})
    return fig


