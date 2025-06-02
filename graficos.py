# === archivo: graficos.py ===
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

#-----------------------------------RECLUTAMIENTO MOTOR-----------------------------

def graficar_eventos(signal_derecha, eventos_derecha, signal_izquierda, eventos_izquierda, dia="Día X"):
    fig, axs = plt.subplots(2, 1, figsize=(14, 6))

    axs[0].plot(signal_derecha, label="Reclutamiento Derecha", color="blue")
    for i, (inicio, fin) in enumerate(eventos_derecha):
        axs[0].axvline(x=inicio, color="red", linestyle="--", label="Inicio de contracción" if i == 0 else "")
        axs[0].axvline(x=fin, color="orange", linestyle="--", label="Fin de contracción" if i == 0 else "")
    axs[0].set_title(f"Señal procesada – Mano Derecha ({dia})", fontsize=14)
    axs[0].set_xlabel("Muestra (0.1 s)", fontsize=12)
    axs[0].set_ylabel("Amplitud (mV)", fontsize=12)
    axs[0].set_ylim(0, 3000)
    axs[0].grid(True)
    axs[0].legend()


    axs[1].plot(signal_izquierda, label="Reclutamiento Izquierda", color="green")
    for i, (inicio, fin) in enumerate(eventos_izquierda):
        axs[1].axvline(x=inicio, color="red", linestyle="--", label="Inicio de contracción" if i == 0 else "")
        axs[1].axvline(x=fin, color="orange", linestyle="--", label="Fin de contracción" if i == 0 else "")
    axs[1].set_title(f"Señal procesada – Mano Izquierda ({dia})", fontsize=14)
    axs[1].set_xlabel("Muestra (0.1 s)", fontsize=12)
    axs[1].set_ylabel("Amplitud (mV)", fontsize=12)
    axs[1].set_ylim(0, 3000)
    axs[1].grid(True)
    axs[1].legend()

    plt.tight_layout()
    st.pyplot(fig)

def graficar_rms_barras(valores_rms_derecha, valores_rms_izquierda, dia="Día X"):
    fig, ax = plt.subplots(figsize=(11, 5))
    indices = np.arange(max(len(valores_rms_derecha), len(valores_rms_izquierda)))
    bar_width = 0.35
    bars_d = ax.bar(indices[:len(valores_rms_derecha)], valores_rms_derecha, width=bar_width, label='Derecha', color='blue')
    bars_i = ax.bar(indices[:len(valores_rms_izquierda)] + bar_width, valores_rms_izquierda, width=bar_width, label='Izquierda', color='green')
    ax.set_title(f"Amplitud RMS por Contracción – {dia}", fontsize=14)
    ax.set_xlabel("Contracción", fontsize=12)
    ax.set_ylabel("Amplitud RMS (mV)", fontsize=12)
    ax.set_ylim(0, 1000)
    ax.set_xticks(indices + bar_width / 2)
    ax.set_xticklabels([f'C{i+1}' for i in indices])
    ax.legend()
    #ax.grid(True)
    ax.bar_label(bars_d, padding=3)
    ax.bar_label(bars_i, padding=3)
    plt.tight_layout()
    st.pyplot(fig)


def graficar_activacion_total(valores_rms_derecha, valores_rms_izquierda, dia="Día X"):
    # Sumar los valores RMS de cada contracción
    suma_derecha = np.sum(valores_rms_derecha)
    suma_izquierda = np.sum(valores_rms_izquierda)
    suma_derecha = suma_derecha/5
    suma_izquierda = suma_izquierda/5

    fig, ax = plt.subplots(figsize=(9, 1.5))  # compacto pero legible

    categorias = ['Derecha', 'Izquierda']
    valores = [suma_derecha, suma_izquierda]
    colores = ['blue', 'green']

    bars = ax.barh(categorias, valores, color=colores, height=0.4, edgecolor='none')

    ax.set_xlim(0, 1000)
    ax.set_title(f"Activación Total – 5 contracciones ({dia})", fontsize=12)
    ax.set_xlabel("Amplitud promedio (mV)", fontsize=10)
    ax.bar_label(bars, padding=4, fontsize=10)

    # Eliminar bordes, ticks y etiquetas del eje X
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.set_xticklabels([])
    ax.grid(False)

    plt.tight_layout()
    st.pyplot(fig)


#-----------------------------------FATIGA MUSCULAR-----------------------------

def graficar_deteccion_contraccion(fatiga_derecha, fatiga_izquierda, inicio_d, fin_d, inicio_i, fin_i, dia="Día 1"):
    fig, axs = plt.subplots(2, 1, figsize=(12, 5))

    axs[0].plot(fatiga_derecha, label="Fatiga Derecha", color="blue")
    axs[0].axvspan(inicio_d, fin_d, color="red", alpha=0.3, label="Contracción detectada")
    axs[0].set_title(f"Señal procesada – Mano Derecha ({dia})")
    axs[0].set_xlabel("Tiempo (ms)")
    axs[0].set_ylabel("Amplitud (mV)")
    axs[0].set_ylim(0, 3000)
    axs[0].grid(True)
    axs[0].legend()

    axs[1].plot(fatiga_izquierda, label="Fatiga Izquierda", color="green")
    axs[1].axvspan(inicio_i, fin_i, color="red", alpha=0.3, label="Contracción detectada")
    axs[1].set_title(f"Señal procesada – Mano Izquierda ({dia})")
    axs[1].set_xlabel("Tiempo (ms)")
    axs[1].set_ylabel("Amplitud (mV)")
    axs[1].set_ylim(0, 3000)
    axs[1].grid(True)
    axs[1].legend()

    plt.tight_layout()
    st.pyplot(fig)

def graficar_rms_bloques_con_pendiente(tiempos, rms_der, rms_izq, dia="Día 1"):
    pend_der, inter_der = np.polyfit(tiempos, rms_der, 1)
    pend_izq, inter_izq = np.polyfit(tiempos, rms_izq, 1)

    fig, axs = plt.subplots(1, 2, figsize=(11, 6))

    bars_d = axs[0].bar(tiempos, rms_der, width=4, color='blue', alpha=0.7, label="RMS derecha")
    axs[0].plot(tiempos, pend_der * tiempos + inter_der, '--', color='black', label=f"Pendiente: {pend_der:.2f}")
    axs[0].set_title(f"Fatiga – Mano Derecha ({dia})")
    axs[0].set_ylabel("RMS (mV)")
    axs[0].set_xticks(tiempos)
    axs[0].set_xticklabels([f'Bloque {i+1}' for i in range(len(tiempos))])
    #axs[0].grid(True, axis='y', linestyle='--', alpha=0.6)
    axs[0].legend()
    axs[0].set_ylim(0, 600)
    axs[0].bar_label(bars_d, padding=3)

    bars_i = axs[1].bar(tiempos, rms_izq, width=4, color='green', alpha=0.7, label="RMS izquierda")
    axs[1].plot(tiempos, pend_izq * tiempos + inter_izq, '--', color='black', label=f"Pendiente: {pend_izq:.2f}")
    axs[1].set_title(f"Fatiga – Mano Izquierda ({dia})")
    axs[1].set_ylabel("RMS (mV)")
    axs[1].set_xticks(tiempos)
    axs[1].set_xticklabels([f'Bloque {i+1}' for i in range(len(tiempos))])
    #axs[1].grid(True, axis='y', linestyle='--', alpha=0.6)
    axs[1].legend()
    axs[1].set_ylim(0, 600)
    axs[1].bar_label(bars_i, padding=3)

    plt.tight_layout()
    st.pyplot(fig)




