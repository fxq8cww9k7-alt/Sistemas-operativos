import os
import sys
import time
import random
import msvcrt

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

class Proceso:
    def __init__(self, id_prog, operacion_str, resultado, tme):
        self.id_prog = id_prog
        self.operacion_str = operacion_str
        self.resultado = resultado
        self.tme = tme
        self.tt = 0
        self.num_lote = 0

def resolver_operacion(n1, op, n2):
    if op == '+':
        return n1 + n2
    elif op == '-':
        return n1 - n2
    elif op == '*':
        return n1 * n2
    elif op == '/':
        return round(n1 / n2, 2)
    elif op in ['%', 'residuo']:
        return n1 % n2
    return 0

def pedir_entero_positivo(msg):
    while True:
        try:
            val = int(input(msg).strip())
            if val > 0:
                return val
            print("Error: El valor debe ser mayor a 0.")
        except ValueError:
            print("Error: Ingresa un número entero válido.")

def generar_procesos():
    limpiar_pantalla()
    n = pedir_entero_positivo("# Procesos: ")
    procesos = []
    operadores = ['+', '-', '*', '/', '%']

    for i in range(1, n + 1):
        id_prog = i
        tme = random.randint(5, 20)
        op = random.choice(operadores)
        num1 = random.randint(0, 100)
        num2 = random.randint(0, 100)

        # Evitar division entre 0
        if op in ['/', '%'] and num2 == 0:
            num2 = random.randint(1, 100)

        res = resolver_operacion(num1, op, num2)
        simbolo = "%" if op == "residuo" else op

        # Formatear números si no tienen decimales
        n1_str = int(num1) if num1 % 1 == 0 else num1
        n2_str = int(num2) if num2 % 1 == 0 else num2
        res_final = int(res) if res % 1 == 0 else res

        operacion_str = f"{n1_str} {simbolo} {n2_str}"
        procesos.append(Proceso(id_prog, operacion_str, res_final, tme))

    return procesos

def crear_lotes(procesos, capacidad=5):
    lotes = []
    for i in range(0, len(procesos), capacidad):
        lote = procesos[i:i + capacidad]
        num_lote = (i // capacidad) + 1
        for p in lote:
            p.num_lote = num_lote
        lotes.append(lote)
    return lotes

def leer_tecla():
    if msvcrt.kbhit():
        return msvcrt.getch().decode('utf-8', errors='ignore').lower()
    return None

def mostrar_interfaz(lotes_pendientes, lote_actual, proceso_actual, terminados, reloj):
    limpiar_pantalla()
    print(f"# Lotes Pendientes: {lotes_pendientes}\n")

    # Columna 1: Lote trabajando
    col1 = ["Lote trabajando", f"{'ID':<6}{'TME':<6}{'TT':<6}"]
    for p in lote_actual:
        col1.append(f"{p.id_prog:<6}{p.tme:<6}{p.tt:<6}")
    while len(col1) < 8:
        col1.append("")
    col1.append(f"Contador: {reloj}")

    # Columna 2: Ejecución
    col2 = ["Ejecución"]
    if proceso_actual:
        tr = proceso_actual.tme - proceso_actual.tt
        col2.append(f"ID       {proceso_actual.id_prog}")
        col2.append(f"Ope      {proceso_actual.operacion_str}")
        col2.append(f"TME      {proceso_actual.tme}")
        col2.append(f"TT       {proceso_actual.tt}")
        col2.append(f"TR       {tr}")
    else:
        col2.append("(Ninguno)")

    # Columna 3: Terminados
    col3 = ["Terminados", f"{'ID':<6}{'Ope':<16}{'Res':<10}{'NL':<4}"]
    for item in terminados:
        if isinstance(item, str):
            col3.append(item)
        else:
            col3.append(f"{item.id_prog:<6}{item.operacion_str:<16}{str(item.resultado):<10}{str(item.num_lote):<4}")

    filas = max(len(col1), len(col2), len(col3))
    while len(col1) < filas:
        col1.append("")
    while len(col2) < filas:
        col2.append("")
    while len(col3) < filas:
        col3.append("")

    for i in range(filas):
        print(f"{col1[i]:<24} {col2[i]:<26} {col3[i]}")

def simular(lotes):
    reloj = 0
    terminados = []
    total = len(lotes)

    for idx, lote in enumerate(lotes):
        pendientes = total - (idx + 1)
        cola = list(lote)

        while cola:
            p = cola.pop(0)
            interrumpido = False
            error = False

            while p.tt < p.tme:
                mostrar_interfaz(pendientes, cola, p, terminados, reloj)

                # Esperar 1 segundo revisando teclas cada 0.1s
                for _ in range(10):
                    tecla = leer_tecla()
                    if tecla == 'p':
                        print("\n--- PAUSA (Presione C para continuar) ---")
                        while True:
                            t_pausa = leer_tecla()
                            if t_pausa == 'c':
                                break
                            time.sleep(0.05)
                    elif tecla == 'e':
                        interrumpido = True
                        break
                    elif tecla == 'w':
                        error = True
                        break

                    time.sleep(0.1)

                if interrumpido:
                    cola.append(p)
                    break

                if error:
                    p.resultado = "Error"
                    terminados.append(p)
                    break

                p.tt += 1
                reloj += 1

                if p.tt >= p.tme:
                    terminados.append(p)
                    break

        terminados.append("-" * 36)

    mostrar_interfaz(0, [], None, terminados, reloj)
    print("\n>>> FIN DE LA SIMULACION - TODOS LOS LOTES EJECUTADOS <<<")
    input("Presione ENTER para salir...")

def main():
    procesos = generar_procesos()
    lotes = crear_lotes(procesos)

    limpiar_pantalla()
    print("=" * 50)
    print("  Generación de procesos completada con éxito.")
    print(f"  Total de procesos generados: {len(procesos)}")
    print(f"  Total de lotes generados: {len(lotes)}")
    print("=" * 50)
    input("\nPresione ENTER para iniciar la ejecución de los lotes...")

    simular(lotes)

if __name__ == "__main__":
    main()
