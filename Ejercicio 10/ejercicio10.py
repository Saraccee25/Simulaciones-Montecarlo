# Paso 1
import numpy as np
import random

# Constantes del problema
CP = 11000000 / 365.0   # Costo promedio de un auto por día
R = 52000               # Renta por auto/día
CND = 30000             # Costo por no tener auto disponible
CO = 7500               # Costo por tener auto ocioso/día
NA_dist = {0: 0.10, 1: 0.10, 2: 0.25, 3: 0.30, 4: 0.25}
ND_dist = {1: 0.40, 2: 0.35, 3: 0.15, 4: 0.10}
TS = 10000

# Rango de autos a evaluar
rango_N = range(8)  # Desde 0 hasta 7 autos


# Paso 2
def generar_NA():
    """Genera la demanda diaria (NA) según la distribución dada."""
    rand_val = random.uniform(0, 1)
    acumulado = 0
    for NA, prob in NA_dist.items():
        acumulado += prob
        if rand_val <= acumulado:
            return NA
    return 4  # valor máximo en caso de error


def generar_ND():
    """Genera los días de alquiler (ND) según la distribución dada."""
    rand_val = random.uniform(0, 1)
    acumulado = 0
    for ND, prob in ND_dist.items():
        acumulado += prob
        if rand_val <= acumulado:
            return ND
    return 4  # valor máximo en caso de error


# Paso 3
resultados = {}

for N in rango_N:
    E = np.zeros(N) 
    costo_total_acumulado = 0

    # Simulación día a día
    for _ in range(TS):
        E = np.maximum(0, E - 1)
        AD = np.sum(E == 0) 
        NA = generar_NA()
        AL = min(AD, NA)
        DI = max(0, NA - AD)

        if AL > 0:
            indices_disponibles = np.where(E == 0)[0]
            autos_a_alquilar_indices = np.random.choice(indices_disponibles, AL, replace=False)
            for indice in autos_a_alquilar_indices:
                E[indice] = generar_ND()

        ingresos = AL * R
        costo_ocioso = (AD - AL) * CO
        costo_no_disponible = DI * CND
        costo_propiedad = N * CP

        CD = costo_ocioso + costo_no_disponible + costo_propiedad - ingresos
        costo_total_acumulado += CD

    costo_promedio = costo_total_acumulado / TS
    resultados[N] = costo_promedio


# Paso 4
N_optimo = min(resultados, key=resultados.get)
costo_minimo = resultados[N_optimo]

# Resultados
print("Resultados de la simulación de Montecarlo:")
print("-" * 50)
for N, CD in resultados.items():
    print(f"  N = {N} autos: Costo Diario Promedio (CD) = ${CD:,.2f}")

print("-" * 50)
print(f"El número óptimo de autos a comprar es: N = {N_optimo}")
print(f"El costo diario promedio mínimo es: ${costo_minimo:,.2f}")
