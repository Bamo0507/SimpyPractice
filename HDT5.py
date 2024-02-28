import simpy
import random

# Parámetros de la simulación
CANT_PROCESOS = 25  # Número de procesos a simular
INTERVALO_LLEGADA = 10  # Intervalo de llegada de procesos
VEL_CPU = 1  # Velocidad del CPU (instrucciones por unidad de tiempo)
INSTRUCCIONES_POR_TURNO = 3  # Número de instrucciones por turno
MEMORIA = 100 #Cantidad de Memoria a utilizar
RANDOM_SEED = 10 #Se deja un Seed para asegurarse que los números dados sean invariables

# Variables para la simulación de procesos
env = simpy.Environment()
ram = simpy.Container(env, init=MEMORIA, capacity=MEMORIA)
cpu = simpy.Resource(env, capacity=1)

# Función para simular un proceso
def proceso(env, nombre, ram, cpu):
    # Llegada del proceso al sistema
    TIEMPO_LLEGADA = env.now
    SOLICITUD_MEMORIA = random.randint(1, 10)
    INSTRUCCIONES = random.randint(1, 10)

    # Mensaje Indicando el Proceso por el que se va, y el tiempo en el que comienza a ejecutarse
    print(f"{nombre} llega en el tiempo {TIEMPO_LLEGADA}.\n")
    # Mensaje para indicar cuántas instrucciones tiene que hacer el Proceso
    print(f"{nombre} tiene que hacer {INSTRUCCIONES} instrucciones.\n")

    # Simula la espera y la ejecución de 3 instrucciones
    with ram.get(SOLICITUD_MEMORIA) as req:
        yield req  # Se simula que pide la memoria
        print(f"{nombre} solicita {SOLICITUD_MEMORIA} de memoria RAM.\n")

        # Ciclo a correr siempre que se tenga alguna instrucción disponible en el Proceso
        while INSTRUCCIONES > 0:
            with cpu.request() as req1:
                yield req1
                # Simulación de solicitud del CPU para hacer un proceso
                INSTRUCCIONES_REALIZAR = min(VEL_CPU * INSTRUCCIONES_POR_TURNO, INSTRUCCIONES)
                INSTRUCCIONES -= INSTRUCCIONES_REALIZAR

                # Mensaje indicando la actualización en las instrucciones de algún Proceso
                print(f"{nombre} ha hecho {INSTRUCCIONES_REALIZAR} instrucciones, le quedan {INSTRUCCIONES}.\n")

                # Se espera cierta cantidad de tiempo (simula la ejecución de la instrucción, espera)
                yield env.timeout(INSTRUCCIONES_REALIZAR)

                # Si ya no tiene instrucciones lo indica con su tiempo
                if INSTRUCCIONES <= 0:
                    TIEMPO_FINAL = env.now
                    print(f"{nombre} ha terminado sus instrucciones en el tiempo {TIEMPO_FINAL}.\n")
                    break;

            # Hace sus 3 instrucciones, entra a Waiting (1) o Ready (2)
            decision = random.randint(1, 2)
            if decision == 1:
                print(f"{nombre} ha entrado a Waiting.\n")
                # No se ha indicado cuánto debe esperar si entra a Waiting
                # Se hace un timeout de 1
                yield env.timeout(1)
                print(f"{nombre} ha regresado a la cola.\n")
            else:
                print(f"{nombre} ha regresado a la cola.\n")

    ULTIMO_TIEMPO = env.now
    print(f"{nombre} ha terminado sus instrucciones en el tiempo {ULTIMO_TIEMPO}.\n")

# Generador de procesos
def llegada_procesos(env, ram, cpu):
    for j in range(CANT_PROCESOS):
        yield env.timeout(random.expovariate(1.0 / INTERVALO_LLEGADA))
        env.process(proceso(env, f'Proceso-{j+1}', ram, cpu))

random.seed(RANDOM_SEED)
env.process(llegada_procesos(env, ram, cpu))
env.run()
