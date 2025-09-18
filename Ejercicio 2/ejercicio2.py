# Paso 1
import random

# Constantes del problema
CC = 8000    # Costo de compra de un paquete de 10 kg
PC = 15000   # Precio de venta de un paquete de 10 kg
CD = 1600    # Costo adicional por donación (2 kg) por paquete vendido
PP = 0.45    # Probabilidad de pérdida de sobrante
TS = 365 * 5  # Tiempo de simulación = 5 años (en días)

# Distribución de probabilidad de la demanda diaria (PV = paquetes vendidos)
PV_dist = {
    5: 0.25,
    10: 0.15,
    12: 0.35,
    15: 0.125,
    20: 0.125
}

# Rango de producción (CO: paquetes producidos/ofrecidos por día)
rango_CO = [5, 10, 12, 15, 20]


# Paso 2
def generar_PV(PV_dist):
    """Genera la demanda diaria de paquetes (PV) según la distribución dada."""
    rand_val = random.uniform(0, 1)
    acumulado = 0
    for PV, prob in PV_dist.items():
        acumulado += prob
        if rand_val <= acumulado:
            return PV
    return max(PV_dist.keys())  # valor máximo en caso de error


# Paso 3
def calcular_ganancia_dia(CO, PV, CD_actual):
    """Calcula la ganancia neta del día dado CO, PV y el costo de donación."""
    vendidos = min(CO, PV)
    sobrante = max(0, CO - PV)

    ingresos = PC * vendidos
    costo_produccion = CC * CO
    costo_donacion = CD_actual * vendidos

    rand_val = random.uniform(0, 1)
    if rand_val <= PP:
        costo_sobrante = CC * sobrante
    else:
        costo_sobrante = 0

    Gdia = ingresos - costo_produccion - costo_donacion - costo_sobrante
    return Gdia


# Paso 4 - Escenario (a): donación de 2 kg
resultados_a = {}

for CO in rango_CO:
    ganancia_total = 0
    for _ in range(TS):  # Simular 5 años
        PV = generar_PV(PV_dist)
        ganancia_total += calcular_ganancia_dia(CO, PV, CD)
    ganancia_promedio = ganancia_total / TS
    resultados_a[CO] = ganancia_promedio

CO_optimo_a = max(resultados_a, key=resultados_a.get)
ganancia_maxima_a = resultados_a[CO_optimo_a]

# Resultados Escenario (a)
print("Resultados de la simulación de Montecarlo (Croquetas):")
print("-" * 60)
print("Escenario (a) -> Donación de 2 kg por paquete vendido")
for CO, Gdia in resultados_a.items():
    print(f"CO = {CO} paquetes -> Ganancia promedio diaria = ${Gdia:,.2f}")

print("-" * 60)
print(f"La cantidad óptima de producción es CO* = {CO_optimo_a} paquetes")
print(f"La ganancia promedio máxima es: ${ganancia_maxima_a:,.2f}")


# Paso 5 - Escenario (b): demanda +20% y donación de 4 kg
PV_dist_b = {round(PV * 1.2): prob for PV, prob in PV_dist.items()}
CD_nuevo = 2 * CD

resultados_b = {}

for CO in rango_CO:
    ganancia_total = 0
    for _ in range(TS):  # Simular 5 años
        PV = generar_PV(PV_dist_b)
        ganancia_total += calcular_ganancia_dia(CO, PV, CD_nuevo)
    ganancia_promedio = ganancia_total / TS
    resultados_b[CO] = ganancia_promedio

CO_optimo_b = max(resultados_b, key=resultados_b.get)
ganancia_maxima_b = resultados_b[CO_optimo_b]

# Resultados Escenario (b)
print("\n" + "=" * 60)
print("Escenario (b) -> Demanda +20% y Donación de 4 kg por paquete vendido")
for CO, Gdia in resultados_b.items():
    print(f"CO = {CO * 1.2:,.2f} paquetes -> Ganancia promedio diaria = ${Gdia:,.2f}")

print("-" * 60)
print(f"La cantidad óptima de producción es CO* = {CO_optimo_b} paquetes")
print(f"La ganancia promedio máxima es: ${ganancia_maxima_b:,.2f}")

# Recomendación
print("-" * 60)
if ganancia_maxima_b > ganancia_maxima_a:
    print("✅ Conviene aumentar la donación a 4 kg, pues la ganancia esperada sube.")
else:
    print("❌ No conviene aumentar la donación a 4 kg, pues la ganancia esperada baja.")
