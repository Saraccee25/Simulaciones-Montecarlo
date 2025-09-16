import random
import numpy as np


# -----------------------------
# Constantes del problema
# -----------------------------
CP = 200_000   # costo de producción por unidad
CI = 30_000    # costo de mantener inventario (unidad/día)
CND = 50_000   # costo por demanda no satisfecha (unidad)
CCA = 180_000  # costo fijo por contratar capacidad extra (día)
TS = 365       # horizonte de simulación = 365 días

# -----------------------------
# Distribución de demanda diaria
# -----------------------------
demand_probs = {1: 0.3, 2: 0.45, 3: 0.25}

# -----------------------------
# Políticas de producción
# -----------------------------
policy_a = {0: 2, 1: 1, 2: 1, 3: 0}   # sin capacidad extra
policy_b = {0: 2, 1: 1, 2: 1, 3: 1}   # con capacidad extra


# -----------------------------
# Funciones auxiliares
# -----------------------------
def sample_demand(dist):
    r = random.random()
    acc = 0.0
    for d, p in dist.items():
        acc += p
        if r <= acc:
            return d
    return max(dist.keys())


def simulate(policy, hire_capacity=False, days=TS, init_inventory=0):
    II = init_inventory
    costs = []

    for _ in range(days):
        D = sample_demand(demand_probs)
        Q = policy.get(II, 0)
        DV = II + Q
        UV = min(DV, D)
        IF = DV - UV
        UF = max(D - DV, 0)

        cost_prod = CP * Q
        cost_inv = CI * IF
        cost_short = CND * UF
        cost_capacity = CCA if hire_capacity else 0
        CT = cost_prod + cost_inv + cost_short + cost_capacity
        costs.append(CT)

        II = min(IF, 3)  # límite inventario

    return {
        "avg_daily_cost": np.mean(costs),
        "std_daily_cost": np.std(costs),
        "total_cost": np.sum(costs)
    }


# -----------------------------
# (a) Comparación II=1 producir 1 vs. producir 2
# -----------------------------
# Caso A1: II=1, producir 1 (como en policy_a)
policy_a1 = policy_a.copy()
policy_a1[1] = 1
res_a1 = simulate(policy_a1, days=TS, init_inventory=1)

# Caso A2: II=1, producir 2
policy_a2 = policy_a.copy()
policy_a2[1] = 2
res_a2 = simulate(policy_a2, days=TS, init_inventory=1)

# -----------------------------
# (b) Capacidad extra
# -----------------------------
res_b1 = simulate(policy_a, hire_capacity=False, init_inventory=0)  # sin capacidad extra
res_b2 = simulate(policy_b, hire_capacity=True, init_inventory=0)   # con capacidad extra

# -----------------------------
# Resultados
# -----------------------------
print("Simulación Montecarlo — Tarheel Computers")
print("=" * 70)

print("(a) Inventario inicial = 1")
print(f"  Caso A1 (producir 1): Costo promedio diario = ${res_a1['avg_daily_cost']:,.2f}")
print(f"  Caso A2 (producir 2): Costo promedio diario = ${res_a2['avg_daily_cost']:,.2f}")
if res_a2["avg_daily_cost"] < res_a1["avg_daily_cost"]:
    print("  ✅ Es más viable producir 2 unidades.")
else:
    print("  ❌ No es viable producir 2 unidades, mejor producir 1.")

print("=" * 70)
print("(b) Capacidad extra")
print(f"  Sin capacidad extra: Costo promedio diario = ${res_b1['avg_daily_cost']:,.2f}")
print(f"  Con capacidad extra: Costo promedio diario = ${res_b2['avg_daily_cost']:,.2f}")
if res_b2["avg_daily_cost"] < res_b1["avg_daily_cost"]:
    print("  ✅ Conviene contratar la capacidad extra.")
else:
    print("  ❌ No conviene contratar la capacidad extra.")
