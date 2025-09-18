import random
import numpy as np

# -------------------------------
# Constantes
# -------------------------------
PV = 8000     # Precio venta revista
CC1 = 6000    # Costo compra primera parte
DR1D = 2400   # Pérdida después de 10 días
U1 = 2000     # Utilidad primera parte

CC2 = 4800    # Costo compra segunda parte
DR2D = 3600   # Pérdida después de 20 días
U2 = 3200     # Utilidad segunda parte

TS = 12       # Meses de simulación

# -------------------------------
# Distribuciones de demanda
# -------------------------------
D1_dist = {5:0.05, 6:0.05, 7:0.10, 8:0.15, 9:0.25, 10:0.25, 11: 0.15}   # Demanda primeros 10 días
D2_dist = {4:0.15, 5:0.20, 6:0.30, 7:0.20, 8:0.15}  # Demanda últimos 20 días

# -------------------------------
# Función para generar demanda
# -------------------------------
def generar_demanda(dist):
    r = random.random()
    acumulado = 0
    for val, prob in dist.items():
        acumulado += prob
        if r <= acumulado:
            return val
    return max(dist.keys())

# -------------------------------
# Función para simular un mes
# -------------------------------
def simular_mes(Q1, Q2):
    # Demanda primera parte
    D1 = generar_demanda(D1_dist)
    RV1 = min(Q1, D1)   # Revistas vendidas
    RS1 = max(Q1 - D1, 0)  # Sobrantes
    Ud1 = (U1 * RV1) - (RS1 * DR1D)

    # Decisión: si hay sobrantes <4 se compra, si >8 se vende, si no se mantiene
    decision = Q2
    if RS1 < 4:
        decision = Q2
    elif RS1 > 8:
        decision = 0   # No comprar más
    else:
        decision = Q2

    # Demanda segunda parte
    D2 = generar_demanda(D2_dist)
    RV2 = min(decision, D2)
    RS2 = max(decision - D2, 0)
    Ud2 = (U2 * RV2) - (RS2 * DR2D)

    return Ud1 + Ud2

# -------------------------------
# Función para simular política
# -------------------------------
def simular_politica(Q1, Q2, TS=12, N=1000):
    ganancias = []
    for _ in range(N):
        total = 0
        for _ in range(TS):
            total += simular_mes(Q1, Q2)
        ganancias.append(total)
    return np.mean(ganancias)

# -------------------------------
# Búsqueda de política óptima
# -------------------------------
mejor_ganancia = -1e9
mejor_politica = (0, 0)

for Q1 in range(5, 12):   # Q1 en rango [5,11]
    for Q2 in range(4, 9): # Q2 en rango [4,8]
        g = simular_politica(Q1, Q2)
        if g > mejor_ganancia:
            mejor_ganancia = g
            mejor_politica = (Q1, Q2)

print("Política óptima encontrada:")
print(f"Q1* = {mejor_politica[0]} revistas al inicio")
print(f"Q2* = {mejor_politica[1]} revistas después de 10 días")
print(f"Ganancia esperada mensual ≈ ${mejor_ganancia/TS:,.2f}")
