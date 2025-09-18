# Paso 1
import random

# Constantes del problema
Cmax = 4   # Capacidad máxima de la represa (unidades/mes)
D = 2      # Requerimiento de agua para generar energía (unidades/mes)
T = 180    # Horizonte de simulación = 15 años * 12 meses

# Distribución de probabilidad de la cantidad de agua que fluye (C)
C_dist = {0: 0.15, 1: 0.35, 2: 0.30, 3: 0.20}

# Agua inicial
I_inicial = 1


# Paso 2
def generar_C():
    """Genera la cantidad de agua que fluye en un mes (C) según la distribución dada."""
    rand_val = random.uniform(0, 1)
    acumulado = 0
    for C, prob in C_dist.items():
        acumulado += prob
        if rand_val <= acumulado:
            return C
    return 3  # valor máximo en caso de error


# Paso 3
# Variables acumuladas
UD_total = 0  # Unidades desperdiciadas en todo el horizonte
EG_total = 0  # Número de meses con generación insuficiente

# Estado inicial
I = I_inicial

# Simulación mes a mes
for _ in range(T):
    # 1. Generar agua que fluye este mes
    C = generar_C()

    # 2. Actualizar agua almacenada
    agua_total = I + C

    # 3. Calcular unidades desperdiciadas del mes
    UD_mes = max(0, agua_total - Cmax)

    # 4. Agua disponible después de vertedero
    I = min(Cmax, agua_total)

    # 5. Liberación para generación de energía
    LG = min(D, I)

    # 6. Energía generada en el mes (EG_mes)
    EG_mes = 1 if LG < D else 0

    # 7. Actualizar acumulados
    UD_total += UD_mes
    EG_total += EG_mes

    # 8. Actualizar agua inicial para el siguiente mes
    I = I - LG

# Paso 4
# Resultados
print("Resultados de la simulación de Montecarlo (Represa):")
print("-" * 60)
print(f"Unidades desperdiciadas totales en 15 años: {UD_total}")
print(f"Meses con generación insuficiente en 15 años: {EG_total}")
print("-" * 60)
