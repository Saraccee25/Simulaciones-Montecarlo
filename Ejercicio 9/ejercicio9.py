import random
import numpy as np

# ==============================
# Constantes conocidas
# ==============================
DF = 1  # Duración de cada fase (semanas)
fases = ["A", "B", "C"]
p_aprobar = [0.4, 0.5, 0.2]   # Probabilidades de aprobar fases A, B, C
NE = 100  # Número de estudiantes a simular

# ==============================
# Variables de respuesta
# ==============================
TC = []  # Tiempo total para completar el programa
TE = [[] for _ in fases]  # Tiempo por etapa (lista de cada fase)
# Tmin y Tmax se calculan después


# ==============================
# Función de simulación
# ==============================
def simular_estudiante():
    """
    Simula el tiempo que tarda un estudiante en completar las 3 fases.
    Retorna el tiempo total (TC) y el tiempo invertido en cada fase (TEi).
    """
    tiempo_total = 0
    tiempos_por_etapa = []

    for i, p in enumerate(p_aprobar):
        NR = 0   # número de veces que se presenta la prueba en esta fase
        aprobado = False
        while not aprobado:
            NR += 1
            tiempo_total += DF
            if random.random() <= p:  # aprueba con probabilidad p
                aprobado = True
        tiempos_por_etapa.append(NR * DF)

    return tiempo_total, tiempos_por_etapa


# ==============================
# Simulación Montecarlo
# ==============================
for _ in range(NE):
    tiempo_total, tiempos_por_etapa = simular_estudiante()
    TC.append(tiempo_total)
    for i in range(len(fases)):
        TE[i].append(tiempos_por_etapa[i])

# ==============================
# Resultados (Modelo Matemático)
# ==============================
# TEi = (DF * Sumatoria{NR}) / NE
TE_promedio = [np.mean(te) for te in TE]

Tmin = np.min(TC)   # Tiempo mínimo total
Tmax = np.max(TC)   # Tiempo máximo total
TC_promedio = np.mean(TC)

# ==============================
# Impresión de resultados
# ==============================
print("Resultados de la simulación de Montecarlo (Programa de Entrenamiento):")
print("-" * 60)
print(f"Número de estudiantes simulados (NE): {NE}")
print("Punto a)")
for i, media in enumerate(TE_promedio):
    print(f"Tiempo medio (TE) en la etapa {fases[i]}: {media:.2f} semanas")
print("-" * 60)
print(f"Tiempo medio TOTAL (TC): {TC_promedio:.2f} semanas")

print("Punto b)")
print(f"Tiempo mínimo TOTAL (Tmin): {Tmin} semanas")
print(f"Tiempo máximo TOTAL (Tmax): {Tmax} semanas")
print("-" * 60)
