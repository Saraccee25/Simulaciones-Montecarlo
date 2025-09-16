# Paso 1 - Importar librerías y definir constantes
import random
import numpy as np

# Constantes del problema
GC_GANANCIA_CRECIMIENTO = 45000  # USD por año
GD_GANANCIA_DECAIDA = 45000      # USD por año  
GF_GANANCIA_FAMA = 100000        # USD por año
T = 20                           # Horizonte de simulación (años)
NUM_CANTANTES = 30              # Número inicial de cantantes
NUM_SIMULACIONES = 50         # Número de simulaciones Monte Carlo

# Estados posibles
CRECIMIENTO = 0
FAMA = 1
DECAIDA = 2
PERDIDA = 3     # Estado terminal
TERMINADO = 4   # Estado terminal

# Probabilidades de transición
prob_crecimiento_a_fama = 0.3
prob_fama_decae = 0.7
prob_fama_perdida = 0.3
prob_fama_mantener = 0.5
prob_recuperacion = 0.2

# Paso 2 - Funciones para generar transiciones
def generar_transicion_crecimiento():
    """Genera la transición desde el estado de crecimiento."""
    if random.random() < prob_crecimiento_a_fama:
        return FAMA
    else:
        return CRECIMIENTO

def generar_transicion_fama():
    """Genera la transición desde el estado de fama."""
    rand_val = random.random()
    if rand_val < prob_fama_decae:
        return DECAIDA
    elif rand_val < prob_fama_decae + prob_fama_perdida:
        return PERDIDA
    else:
        return FAMA  # Se mantiene en fama

def generar_transicion_decaida():
    """Genera la transición desde el estado de decaída."""
    if random.random() < prob_recuperacion:
        return CRECIMIENTO  # Recuperación
    else:
        return TERMINADO    # Termina carrera

def simular_cantante(estado_inicial):
    """Simula la carrera completa de un cantante durante T años."""
    estado_actual = estado_inicial  # Empieza en el estado asignado
    ganancia_total = 0
    tiempo_activo = 0
    
    for año in range(T):
        # Si está en estado terminal, no genera más ingresos ni cambia estado
        if estado_actual in [PERDIDA, TERMINADO]:
            break
            
        tiempo_activo += 1
        
        # Calcular ganancia del año actual
        if estado_actual == CRECIMIENTO:
            ganancia_total += GC_GANANCIA_CRECIMIENTO
        elif estado_actual == FAMA:
            ganancia_total += GF_GANANCIA_FAMA
        elif estado_actual == DECAIDA:
            ganancia_total += GD_GANANCIA_DECAIDA
        
        # Generar transición de estado para el siguiente año
        if estado_actual == CRECIMIENTO:
            estado_actual = generar_transicion_crecimiento()
        elif estado_actual == FAMA:
            estado_actual = generar_transicion_fama()
        elif estado_actual == DECAIDA:
            estado_actual = generar_transicion_decaida()
    
    return {
        'estado_final': estado_actual,
        'ganancia_total': ganancia_total,
        'tiempo_activo': tiempo_activo
    }

# Paso 3 - Ejecutar simulaciones
# Variables acumuladas para todas las simulaciones
cantantes_crecimiento_final = 0
cantantes_fama_final = 0
cantantes_decaida_final = 0
cantantes_perdida_final = 0
cantantes_terminado_final = 0
cantantes_activos_20_años = 0
tiempos_carrera = []
ganancias_totales = []

print(f"Ejecutando {NUM_SIMULACIONES} simulaciones de Monte Carlo...")
print("-" * 60)

for simulacion in range(NUM_SIMULACIONES):
    if (simulacion + 1) % 100 == 0:
        print(f"Progreso: {simulacion + 1}/{NUM_SIMULACIONES} simulaciones completadas")
    
    # Definir distribución inicial: 20 crecimiento, 5 fama, 5 decaída
    estados_iniciales = (
        [CRECIMIENTO] * 20 +  # 20 cantantes en crecimiento
        [FAMA] * 5 +          # 5 cantantes en fama  
        [DECAIDA] * 5         # 5 cantantes en decaída
    )
    
    # Simular los 30 cantantes de esta simulación
    for cantante in range(NUM_CANTANTES):
        estado_inicial = estados_iniciales[cantante]
        resultado = simular_cantante(estado_inicial)
        
        # Acumular estadísticas
        if resultado['estado_final'] == CRECIMIENTO:
            cantantes_crecimiento_final += 1
        elif resultado['estado_final'] == FAMA:
            cantantes_fama_final += 1
        elif resultado['estado_final'] == DECAIDA:
            cantantes_decaida_final += 1
        elif resultado['estado_final'] == PERDIDA:
            cantantes_perdida_final += 1
        elif resultado['estado_final'] == TERMINADO:
            cantantes_terminado_final += 1
            
        if resultado['tiempo_activo'] == 20:
            cantantes_activos_20_años += 1
            
        tiempos_carrera.append(resultado['tiempo_activo'])
        ganancias_totales.append(resultado['ganancia_total'])

# Paso 4 - Calcular y mostrar resultados
total_cantantes = NUM_SIMULACIONES * NUM_CANTANTES

# Respuestas a las preguntas del ejercicio
print("\nResultados de la simulación de Monte Carlo (Carrera de Cantantes):")
print("=" * 70)

# (a) ¿Cuántos cantantes dejaron de ser cantantes en 20 años?
cantantes_que_dejaron_carrera = cantantes_perdida_final + cantantes_terminado_final

print(f"(a) Cantantes que dejaron de ser cantantes al final de 20 años:")
print(f"    Total que abandonaron: {cantantes_que_dejaron_carrera} de {total_cantantes}")
print(f"    Porcentaje: {cantantes_que_dejaron_carrera/total_cantantes*100:.2f}%")
print(f"    - Por pérdida de carrera: {cantantes_perdida_final}")
print(f"    - Por terminar carrera (decaída→terminado): {cantantes_terminado_final}")

# Cantantes que siguieron activos
cantantes_activos = cantantes_crecimiento_final + cantantes_fama_final + cantantes_decaida_final
print(f"    Cantantes aún activos: {cantantes_activos} ({cantantes_activos/total_cantantes*100:.2f}%)")
print(f"    - En crecimiento: {cantantes_crecimiento_final}")
print(f"    - En fama: {cantantes_fama_final}")
print(f"    - En decaída: {cantantes_decaida_final}")

# (b) ¿Cuál es el tiempo estimado de carrera de un cantante de reggaetón?
tiempo_promedio = np.mean(tiempos_carrera)
tiempo_mediana = np.median(tiempos_carrera)
tiempo_std = np.std(tiempos_carrera)

print(f"\n(b) Tiempo estimado de carrera de un cantante de reggaetón:")
print(f"    Tiempo promedio: {tiempo_promedio:.2f} años")
print(f"    Tiempo mediano: {tiempo_mediana:.2f} años")
print(f"    Desviación estándar: {tiempo_std:.2f} años")
print(f"    Cantantes que completaron 20 años activos: {cantantes_activos_20_años}")

# (c) Dinero promedio que gana un cantante de reggaetón en 20 años
ganancia_promedio = np.mean(ganancias_totales)
ganancia_mediana = np.median(ganancias_totales)
ganancia_std = np.std(ganancias_totales)

print(f"\n(c) Dinero promedio que gana un cantante de reggaetón en 20 años:")
print(f"    Ganancia promedio total: ${ganancia_promedio:,.2f} USD")
print(f"    Ganancia mediana total: ${ganancia_mediana:,.2f} USD")
print(f"    Desviación estándar: ${ganancia_std:,.2f} USD")
print(f"    Ganancia anual promedio: ${ganancia_promedio/20:,.2f} USD")

print("=" * 70)

# Estadísticas adicionales
print(f"\nEstadísticas generales:")
print(f"Número total de simulaciones: {NUM_SIMULACIONES}")
print(f"Cantantes simulados por simulación: {NUM_CANTANTES}")
print(f"Total de cantantes simulados: {total_cantantes}")
print(f"Horizonte de simulación: {T} años")
print(f"\nDistribución inicial por simulación:")
print(f"    - 20 cantantes empiezan en CRECIMIENTO")
print(f"    - 5 cantantes empiezan en FAMA") 
print(f"    - 5 cantantes empiezan en DECAÍDA")

# Distribución de estados finales
estados_nombres = ['Crecimiento', 'Fama', 'Decaída', 'Pérdida', 'Terminado']
print(f"\nDistribución de estados finales:")

# Usar los contadores ya calculados durante la simulación principal
conteo_estados = [
    cantantes_crecimiento_final,
    cantantes_fama_final, 
    cantantes_decaida_final,
    cantantes_perdida_final,
    cantantes_terminado_final
]

for i, nombre in enumerate(estados_nombres):
    porcentaje = (conteo_estados[i] / total_cantantes) * 100
    print(f"    {nombre}: {conteo_estados[i]} cantantes ({porcentaje:.2f}%)")

# Resumen de cantantes que dejaron la carrera
print(f"\nResumen:")
print(f"    Total cantantes que DEJARON de ser cantantes: {cantantes_que_dejaron_carrera} ({cantantes_que_dejaron_carrera/total_cantantes*100:.2f}%)")
print(f"    Total cantantes que AÚN SIGUEN activos: {cantantes_activos} ({cantantes_activos/total_cantantes*100:.2f}%)")