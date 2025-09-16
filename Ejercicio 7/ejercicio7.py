import random
import numpy as np

random.seed(42)  # reproducibilidad

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
# Escenario (a) sin capacidad extra
policy_a = {0: 2, 1: 1, 2: 1, 3: 0}

# Escenario (b) con capacidad extra (si II=3 produce 1)
policy_b = {0: 2, 1: 1, 2: 1, 3: 1}


# -----------------------------
# Funciones auxiliares
# -----------------------------
def sample_demand(dist):
    """Genera una demanda diaria según distribución dada."""
    r = random.random()
    acc = 0.0
    for d, p in dist.items():
        acc += p
        if r <= acc:
            return d
    return max(dist.keys())  # seguridad


def simulate(policy, hire_capacity=False, days=TS):
    """Simula el sistema día a día con la política dada."""
    II = 0  # inventario inicial
    costs = []

    for _ in range(days):
        # Demanda aleatoria
        D = sample_demand(demand_probs)

        # Producción según inventario inicial
        Q = policy.get(II, 0)
        DV = II + Q
        UV = min(DV, D)
        IF = DV - UV
        UF = max(D - DV, 0)

        # Costos del día
        cost_prod = CP * Q
        cost_inv = CI * IF
        cost_short = CND * UF
        cost_capacity = CCA if hire_capacity else 0
        CT = cost_prod + cost_inv + cost_short + cost_capacity

        costs.append(CT)

        # Inventario del siguiente día (limitado a 3)
        II = min(IF, 3)

    return {
        "avg_daily_cost": np.mean(costs),
        "std_daily_cost": np.std(costs),
        "total_cost": np.sum(costs),
        "days": days
    }


# -----------------------------
# Ejecutar simulaciones
# -----------------------------
res_a = simulate(policy_a, hire_capacity=False)
res_b = simulate(policy_b, hire_capacity=True)

# -----------------------------
# Resultados
# -----------------------------
print("Simulación Montecarlo — Tarheel Computers")
print("=" * 70)

print("Escenario (a) Sin capacidad extra contratada:")
print(f"  Costo promedio diario: ${res_a['avg_daily_cost']:,.2f}")
print(f"  Desviación estándar del costo diario: ${res_a['std_daily_cost']:,.2f}")
print(f"  Costo total en {TS} días: ${res_a['total_cost']:,.2f}")

print("-" * 70)
print("Escenario (b) Con capacidad extra contratada:")
print(f"  Costo promedio diario: ${res_b['avg_daily_cost']:,.2f}")
print(f"  Desviación estándar del costo diario: ${res_b['std_daily_cost']:,.2f}")
print(f"  Costo total en {TS} días: ${res_b['total_cost']:,.2f}")

print("=" * 70)
if res_b['avg_daily_cost'] < res_a['avg_daily_cost']:
    print("✅ Conviene contratar la capacidad extra.")
else:
    print("❌ No conviene contratar la capacidad extra.")
