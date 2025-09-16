import random
import numpy as np

# Probabilidades de aprobar fases A, B, C
p_aprobar = [0.4, 0.5, 0.2]
num_fases = len(p_aprobar)
TS = 100  # Número de simulaciones

# Resultados acumulados
tiempos_totales = []
tiempos_etapas = [[] for _ in range(num_fases)]

def simular_programa():

    tiempo_total = 0
    tiempos_por_etapa = []

    for i in range(num_fases):
        tiempo_etapa = 0
        aprobado = False
        while not aprobado:
            tiempo_etapa += 1  # Cada intento consume 1 semana
            tiempo_total += 1
            if random.random() <= p_aprobar[i]:
                aprobado = True
        tiempos_por_etapa.append(tiempo_etapa)

    return tiempo_total, tiempos_por_etapa


# Ejecutar simulaciones
for _ in range(TS):
    tiempo_total, tiempos_por_etapa = simular_programa()
    tiempos_totales.append(tiempo_total)
    for i in range(num_fases):
        tiempos_etapas[i].append(tiempos_por_etapa[i])

# Estadísticas
tiempo_medio_total = np.mean(tiempos_totales)
tiempo_min_total = np.min(tiempos_totales)
tiempo_max_total = np.max(tiempos_totales)
tiempo_medio_etapas = [np.mean(t) for t in tiempos_etapas]

# Resultados
print("Resultados de la simulación de Montecarlo (Programa de Entrenamiento):")
print("-" * 60)
print(f"Simulaciones realizadas: {TS}")
for i, media in enumerate(tiempo_medio_etapas):
    print(f"Tiempo medio en semanas en la etapa {chr(65+i)}: {media:.2f}")
print("-" * 60)
print(f"Tiempo medio TOTAL en semanas: {tiempo_medio_total:.2f}")
print(f"Tiempo mínimo TOTAL en semanas: {tiempo_min_total}")
print(f"Tiempo máximo TOTAL en semanas: {tiempo_max_total}")
print("-" * 60)
