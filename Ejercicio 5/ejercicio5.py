from random import random

# ======================
# CONFIGURACIÓN
# ======================
N_DIAS = 10000   # Tiempo de simulación
PRODUCCION = 50
COSTO_UNITARIO = 1000
PRECIO_UNITARIO = 3000
MULTA = 30000
COSTO_PERMISO_SEMANA = 20000
COSTO_PERMISO_DIA = COSTO_PERMISO_SEMANA / 7

# ======================
# FUNCIONES AUXILIARES
# ======================
def demanda_con_sim_montecarlo():
    A = random()
    if A < 0.10: return 10
    elif A <= 0.30: return 20
    elif A <= 0.60: return 25
    elif A <= 0.80: return 30
    elif A <= 0.90: return 50
    elif A <= 0.96: return 70
    else: return 100

def multa_con_sim_montecarlo():
    return 1 if random() < 0.25 else 0  # 25% de probabilidad

# ======================
# SIMULACIÓN
# ======================
faltantes_totales = 0
tiradas_totales = 0
utilidad_sin_permiso_total = 0
utilidad_con_permiso_total = 0

for _ in range(N_DIAS):
    demanda = demanda_con_sim_montecarlo()
    vendidas = min(PRODUCCION, demanda)
    tiradas = max(0, PRODUCCION - demanda)
    faltantes = max(0, demanda - PRODUCCION)

    # ingresos
    ingreso = vendidas * PRECIO_UNITARIO
    costo = PRODUCCION * COSTO_UNITARIO

    # utilidad sin permiso
    multa = multa_con_sim_montecarlo() * MULTA
    utilidad_sin = ingreso - costo - multa

    # utilidad con permiso
    utilidad_con = ingreso - costo - COSTO_PERMISO_DIA

    # acumular
    faltantes_totales += faltantes
    tiradas_totales += tiradas
    utilidad_sin_permiso_total += utilidad_sin
    utilidad_con_permiso_total += utilidad_con

# ======================
# RESULTADOS
# ======================
faltantes_prom = faltantes_totales / N_DIAS
tiradas_prom = tiradas_totales / N_DIAS
utilidad_sin_prom = utilidad_sin_permiso_total / N_DIAS
utilidad_con_prom = utilidad_con_permiso_total / N_DIAS

print("Resultados de la simulación Montecarlo ({} días):".format(N_DIAS))
print(f"a) Número medio de tortas faltantes: {faltantes_prom:.2f}")
print(f"b) Número medio de tortas tiradas: {tiradas_prom:.2f}")
print(f"c) Utilidad media sin permiso: ${utilidad_sin_prom:,.2f} por día")
print(f"   Utilidad media con permiso: ${utilidad_con_prom:,.2f} por día")

if utilidad_con_prom > utilidad_sin_prom:
    print("d) Conviene conseguir el permiso.")
else:
    print("d) Conviene seguir tirando las tortas (sin permiso).")
