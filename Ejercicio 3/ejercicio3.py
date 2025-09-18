# Paso 1: Importar librerías y definir constantes
import random

# Constantes del problema
H = 2_000_000  # Habitantes totales
IBM = 500      # Impuesto de Baja a Media
IMA = 800      # Impuesto de Media a Alta
TS = 20        # Tiempo de simulación en años
Prob_CS_Bueno = 9/20  # Probabilidad de Comercio Senegal Bueno
Prob_CS_Malo = 11/20   # Probabilidad de Comercio Senegal Malo

# Paso 2: Definir la función para el estado anual de CS
def generar_cs_anual():
    """Genera el estado de Comercio Senegal (CS) para un año."""
    r = random.uniform(0, 1)
    if r <= Prob_CS_Bueno:
        return 'Bueno'
    else:
        return 'Malo'

# Paso 3: Simulación de Montecarlo
def simular_montecarlo_gambia():
    """
    Realiza una simulación de Montecarlo para calcular la recaudación
    de impuestos usando el conteo de personas por clase (Nt,C).
    """
    # Estado inicial de la población
    poblacion_actual = {
        'Baja': 1_000_000,
        'Media': 700_000,
        'Alta': 300_000
    }

    DRGT = 0  # Dinero a recaudar total
    
    # Bucle de la simulación año a año
    for anio in range(TS):
        DRGA = 0  # Dinero a recaudar en el año actual
        
        # Generar el estado de CS para el año
        cs_anual = generar_cs_anual()
        
        # Guardar el conteo de personas antes de la transición
        poblacion_pre_transicion = poblacion_actual.copy()
        
        # Reiniciar los contadores de la población para el siguiente año
        poblacion_actual = {'Baja': 0, 'Media': 0, 'Alta': 0}
        
        # Aplicar las transiciones según el modelo matemático
        if cs_anual == 'Bueno':
            # Transiciones desde la clase Baja
            transiciones_B_M = round(poblacion_pre_transicion['Baja'] * 0.6)
            transiciones_B_B = poblacion_pre_transicion['Baja'] - transiciones_B_M
            poblacion_actual['Baja'] += transiciones_B_B
            poblacion_actual['Media'] += transiciones_B_M
            DRGA += transiciones_B_M * IBM
            
            # Transiciones desde la clase Media
            transiciones_M_A = round(poblacion_pre_transicion['Media'] * 0.6)
            transiciones_M_M = poblacion_pre_transicion['Media'] - transiciones_M_A
            poblacion_actual['Media'] += transiciones_M_M
            poblacion_actual['Alta'] += transiciones_M_A
            DRGA += transiciones_M_A * IMA
            
            # Transiciones desde la clase Alta
            poblacion_actual['Alta'] += poblacion_pre_transicion['Alta']
            
        elif cs_anual == 'Malo':
            # Transiciones desde la clase Baja
            transiciones_B_B = poblacion_pre_transicion['Baja']
            poblacion_actual['Baja'] += transiciones_B_B
            
            # Transiciones desde la clase Media
            transiciones_M_B = round(poblacion_pre_transicion['Media'] * 0.5)
            transiciones_M_M = poblacion_pre_transicion['Media'] - transiciones_M_B
            poblacion_actual['Baja'] += transiciones_M_B
            poblacion_actual['Media'] += transiciones_M_M
            
            # Transiciones desde la clase Alta
            transiciones_A_M = round(poblacion_pre_transicion['Alta'] * 0.5)
            transiciones_A_A = poblacion_pre_transicion['Alta'] - transiciones_A_M
            poblacion_actual['Media'] += transiciones_A_M
            poblacion_actual['Alta'] += transiciones_A_A

        DRGT += DRGA
        
    return DRGT

# Paso 4: Ejecutar la simulación y mostrar los resultados
num_simulaciones = 100  # Número de veces que se ejecutará la simulación
resultados_DRGT = [simular_montecarlo_gambia() for _ in range(num_simulaciones)]

print("Resultados de la simulación de Montecarlo (Gambia):")
print("-" * 60)
print(f"Recaudación total en 20 años para {num_simulaciones} simulaciones:")
print(f"  Promedio: ${sum(resultados_DRGT) / num_simulaciones:,.2f}")
print("-" * 60)