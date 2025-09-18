from random import random

def generar_boleta(i, n):
    boleta = random()
    if boleta <= 0.5:
        boleta = i
    else:
        boleta = n

    return boleta

boleta_1 = generar_boleta(1, 2)
boleta_2 = generar_boleta(3, 4)
boleta_3 = generar_boleta(5, 6)

def generar_valor():
    valor = random()
    if valor <= 0.5:
        valor = 1000
    else:
        valor = 5000
    return valor

valor_boleta_1 = generar_valor()
valor_boleta_2 = generar_valor()
valor_boleta_3 = generar_valor()

print(valor_boleta_1)
print(valor_boleta_2)
print(valor_boleta_3)

###Calcular Utilidad o Ganancia según boletos generados

def calcular_utilidad (valor_boleta_1, valor_boleta_2, valor_boleta_3):
    if valor_boleta_1 == valor_boleta_2 == valor_boleta_3 == 1000 :
        utilidad = 1000
    elif valor_boleta_1 == valor_boleta_2 == valor_boleta_3 == 5000 :
        utilidad = 5000
    else:
        utilidad = 0
    return utilidad

utilidad = calcular_utilidad(valor_boleta_1, valor_boleta_2, valor_boleta_3)
print(f"Utilidad: {utilidad}")

###Calcular valor para cada boleta y el costo para la empresa

costo_minimo = 0

for i in range(10000):
    boleta_1 = generar_boleta(1, 2)
    boleta_2 = generar_boleta(3, 4)
    boleta_3 = generar_boleta(5, 6)

    valor_boleta_1 = generar_valor()
    valor_boleta_2 = generar_valor()
    valor_boleta_3 = generar_valor()

    utilidad = calcular_utilidad(valor_boleta_1, valor_boleta_2, valor_boleta_3)

    costo_minimo += utilidad


print(f"El costo total para la empresa fue de: {costo_minimo}")
print(f"Total de boletas vendidas: {i+1}")
print(f"El costo minimo por boleta debe ser: {(costo_minimo / (i + 1)) + 1}")
