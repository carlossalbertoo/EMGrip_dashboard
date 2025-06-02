# === archivo: funciones.py ===

from scipy.signal import butter, filtfilt
import numpy as np

#-------------------------------------RECLUTAMIENTO MOTOR----------------------------------------------

# Filtro pasa banda
def filtro_pasabanda(signal, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

# Clipping intermedio para eliminar picos medianos
def clipping_intermedio(signal, lim_sup=750, lim_inf=350):
    return [val if (val <= lim_inf or val >= lim_sup) else lim_inf for val in signal]

# Detección de eventos (contracciones) con anticipación del inicio
def detectar_eventos(signal, umbral_inicio=450, umbral_fin=600, fs=10, min_duracion_s=2, anticipacion_ms=250):
    eventos = []
    en_contraccion = False
    inicio = None
    min_muestras = int(min_duracion_s * fs)
    muestras_anticipacion = int((anticipacion_ms / 1000) * fs)

    for i, valor in enumerate(signal):
        if not en_contraccion and valor >= umbral_inicio:
            en_contraccion = True
            # Anticipar el índice de inicio, sin ir antes del inicio de la señal
            inicio = max(0, i - muestras_anticipacion)
        elif en_contraccion:
            if i - inicio >= min_muestras and valor < umbral_fin:
                fin = i
                eventos.append((inicio, fin))
                en_contraccion = False

    if en_contraccion and len(signal) - inicio >= min_muestras:
        eventos.append((inicio, len(signal) - 1))

    return eventos

# Cálculo de RMS

def calcular_rms_por_evento(signal, eventos):
    rms_eventos = []
    for inicio, fin in eventos:
        segmento = signal[inicio:fin+1]
        rms = np.sqrt(np.mean(np.square(segmento)))
        rms_eventos.append((inicio, fin, rms))
    return rms_eventos

# Extraer y alinear contracciones

def obtener_contracciones_alineadas(signal, eventos, longitud_fija=20):
    contracciones = []
    for inicio, fin in eventos:
        segmento = signal[inicio:fin]
        if len(segmento) >= longitud_fija:
            contracciones.append(segmento[:longitud_fija])
    return np.array(contracciones)

#-----------------------------------FATIGA MUSCULAR-----------------------------
# --- Calcular duración de contracción ---
def calcular_duracion_contraccion(signal, umbral, fs):
    indices_activos = [i for i, valor in enumerate(signal) if valor > umbral]
    if not indices_activos:
        return 0, 0, 0
    inicio = indices_activos[0]
    fin = indices_activos[-1]
    duracion_muestras = fin - inicio + 1
    duracion_segundos = duracion_muestras / fs
    return duracion_segundos, inicio, fin

# --- RMS por bloques ---
def calcular_rms_bloques(signal, muestras_por_bloque):
    bloques = [signal[i:i + muestras_por_bloque] for i in range(0, len(signal), muestras_por_bloque)]
    bloques = [b for b in bloques if len(b) == muestras_por_bloque]
    return [np.sqrt(np.mean(np.square(b))) for b in bloques]