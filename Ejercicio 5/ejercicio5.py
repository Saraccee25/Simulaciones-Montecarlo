from random import random

def demanda_con_sim_montecarlo():
    A = random()
    if A < 0.10:
      D = 10
    elif 0.10 < A <= 0.30:
      D = 20
    elif 0.30 < A <= 0.60:
      D = 25
    elif 0.60 < A <= 0.80:
      D = 30
    elif 0.80 < A <= 0.90:
      D = 50
    elif 0.90 < A <= 0.96:
      D = 70
    else:
        D = 100

    return D

print("Demanda diaria: ", demanda_con_sim_montecarlo())


from random import random

def multa_con_sim_montecarlo():
    A = random()
    if A < 0.75:
      C = 0
    else:
      C = 1

    return C

print("Evento de la policía: ", multa_con_sim_montecarlo())

def tortasVendidas():
  P = 50
  D = demanda_con_sim_montecarlo()
  S = min(P, D)
  return S

print("Tortas vendidas: ", tortasVendidas())

def tortasTiradas():
  P = 50
  B = P - tortasVendidas()
  return B
print("Tortas tiradas: ", tortasTiradas())

def tortasFaltantes():
    P = 50
    D = demanda_con_sim_montecarlo()
    if D > P:
        TF = D - P
    else:
        TF = 0
    return TF
print("Tortas faltantes: ", tortasFaltantes())


def ingreso():
  R = 3000 * tortasVendidas()
  return R

print("Ingreso diario: ", ingreso())

def usinPermiso():
  C = multa_con_sim_montecarlo()
  if C == 0:
    print('No Multado')
  else:
    print('multado')

  M = 30000 * C
  UsinPermiso = ingreso() - 1000 - M
  return UsinPermiso

print("Utilidad sin permiso: ", usinPermiso())

def uconPermiso():
  UconPermiso = ingreso() - 1000 - 2857
  return UconPermiso

print("Utilidad con permiso: ", uconPermiso())
