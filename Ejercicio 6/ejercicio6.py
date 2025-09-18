import random
import numpy as np

# -------------------------------
# Constantes
# -------------------------------
PV = 8000     # Precio venta revista
CC1 = 6000    # Costo compra primera parte
CC2 = 4800    # Costo compra segunda parte
DEV = 3600    # Precio de devolución al proveedor
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
    # ----- Primera parte -----
    D1 = generar_demanda(D1_dist)
    RV1 = min(Q1, D1)          # Revistas vendidas
    RS1 = max(Q1 - D1, 0)      # Sobrantes

    ingresos1 = RV1 * PV
    costo1 = Q1 * CC1
    devolucion1 = RS1 * DEV    # Se devuelven sobrantes a 3600
    utilidad1 = ingresos1 + devolucion1 - costo1

    # ----- Decisión segunda parte -----
    if RS1 < 4:
        decision = Q2   # Comprar más
    elif RS1 > 8:
        decision = 0    # No comprar más
    else:
        decision = Q2   # Mantener

    # ----- Segunda parte -----
    D2 = generar_demanda(D2_dist)
    RV2 = min(decision, D2)
    RS2 = max(decision - D2, 0)

    ingresos2 = RV2 * PV
    costo2 = decision * CC2
    devolucion2 = RS2 * DEV
    utilidad2 = ingresos2 + devolucion2 - costo2

    return utilidad1 + utilidad2

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
