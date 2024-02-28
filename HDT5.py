import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la simulación
CANT_PROCESOS = [25, 50, 100, 150, 200]  # Lista de cantidades de procesos a simular
INTERVALO_LLEGADA = 10  # Intervalo de llegada de procesos
VEL_CPU = 1  # Velocidad del CPU (instrucciones por unidad de tiempo)
INSTRUCCIONES_POR_TURNO = 3  # Número de instrucciones por turno
MEMORIA = 100  # Cantidad de Memoria a utilizar
RANDOM_SEED = 10  # Se deja un Seed para asegurarse que los números dados sean invariables

# Variables para almacenar los tiempos de cada simulación
tiempos_promedio = []
desviaciones_estandar = []

# Función para simular un proceso
def proceso(env, nombre, ram, cpu, tiempos):
    # Llegada del proceso al sistema
    TIEMPO_LLEGADA = env.now
    SOLICITUD_MEMORIA = random.randint(1, 10)
    INSTRUCCIONES = random.randint(1, 10)

    # Mensaje Indicando el Proceso por el que se va, y el tiempo en el que comienza a ejecutarse
    print(f"{nombre} llega en el tiempo {TIEMPO_LLEGADA}.\n")
    # Mensaje para indicar cuántas instrucciones tiene que hacer el Proceso
    print(f"{nombre} tiene que hacer {INSTRUCCIONES} instrucciones.\n")

    # Simula la espera y la ejecución de instrucciones
    with ram.get(SOLICITUD_MEMORIA) as req:
        yield req  # Se simula que pide la memoria
        print(f"{nombre} solicita {SOLICITUD_MEMORIA} de memoria RAM.\n")

        # Ciclo para ejecutar instrucciones
        while INSTRUCCIONES > 0:
            with cpu.request() as req1:
                yield req1
                # Simulación de solicitud del CPU para hacer un proceso
                INSTRUCCIONES_REALIZAR = min(VEL_CPU * INSTRUCCIONES_POR_TURNO, INSTRUCCIONES)
                INSTRUCCIONES -= INSTRUCCIONES_REALIZAR

                # Mensaje indicando la actualización en las instrucciones de algún Proceso
                print(f"{nombre} ha hecho {INSTRUCCIONES_REALIZAR} instrucciones, le quedan {INSTRUCCIONES}.\n")

                # Se espera cierta cantidad de tiempo (simula la ejecución de la instrucción)
                yield env.timeout(INSTRUCCIONES_REALIZAR)

        # Calcula el tiempo que el proceso pasó en la computadora
        tiempo_final = env.now
        tiempo_total = tiempo_final - TIEMPO_LLEGADA
        tiempos.append(tiempo_total)
        print(f"{nombre} ha terminado sus instrucciones en el tiempo {tiempo_final}.\n")

# Función para ejecutar una simulación con una cantidad específica de procesos
def ejecutar_simulacion(cantidad_procesos):
    env = simpy.Environment()
    ram = simpy.Container(env, init=MEMORIA, capacity=MEMORIA)
    cpu = simpy.Resource(env, capacity=2)
    tiempos = []

    env.process(llegada_procesos(env, cantidad_procesos, ram, cpu, tiempos))
    env.run()

    return tiempos

# Generador de procesos
def llegada_procesos(env, cantidad_procesos, ram, cpu, tiempos):
    for j in range(cantidad_procesos):
        yield env.timeout(random.expovariate(1.0 / INTERVALO_LLEGADA))
        env.process(proceso(env, f'Proceso-{j+1}', ram, cpu, tiempos))

# Fijar la semilla aleatoria
random.seed(RANDOM_SEED)

# Ejecuta la simulación para cada cantidad de procesos
for cantidad in CANT_PROCESOS:
    tiempos = ejecutar_simulacion(cantidad)
    tiempo_promedio = np.mean(tiempos)
    desviacion_estandar = np.std(tiempos)
    tiempos_promedio.append(tiempo_promedio)
    desviaciones_estandar.append(desviacion_estandar)
    print(f"Para {cantidad} procesos:")
    print(f"Tiempo promedio: {tiempo_promedio}")
    print(f"Desviación estándar: {desviacion_estandar}")
    print()

print("---------------------------------------------------------------")
# Imprime los tiempos promedio y desviaciones estándar al final
print("Resultados finales:")
for i, cantidad in enumerate(CANT_PROCESOS):
    print(f"Para {cantidad} procesos:")
    print(f"Tiempo promedio: {tiempos_promedio[i]}")
    print(f"Desviación estándar: {desviaciones_estandar[i]}")
    print()
print("---------------------------------------------------------------")


# Grafica los resultados
plt.plot(CANT_PROCESOS, tiempos_promedio, marker='o')
plt.title('Número de Procesos vs Tiempo Promedio')
plt.xlabel('Número de Procesos')
plt.ylabel('Tiempo Promedio')
plt.grid(True)
plt.show()

