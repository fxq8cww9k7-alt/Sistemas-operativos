import os
import sys
import time

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

class Proceso:
    def __init__(self, id_prog, nombre, operacion_str, resultado, tme):
        self.id_prog = id_prog
        self.nombre = nombre
        self.operacion_str = operacion_str
        self.resultado = resultado
        self.tme = tme
        self.tt = 0

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

def capturar_operacion_y_datos():
    while True:
        op = input("Operación (+, -, *, /, %): ").strip().lower()
        if op in ['+', '-', '*', '/', '%', 'residuo']:
            break
        print("Operación no válida. Intenta de nuevo.")

    while True:
        try:
            num1 = float(input("  Dato 1: "))
            break
        except ValueError:
            print("  Error: Ingresa un número válido.")

    while True:
        try:
            num2 = float(input("  Dato 2: "))
            if op in ['/', '%', 'residuo'] and num2 == 0:
                print("  Error: No se permite 0 en el segundo dato para división o residuo.")
                continue
            break
        except ValueError:
            print("  Error: Ingresa un número válido.")

    res = resolver_operacion(num1, op, num2)
    simbolo = "%" if op == "residuo" else op
    
    # Formatear números si no tienen decimales
    n1_str = int(num1) if num1 % 1 == 0 else num1
    n2_str = int(num2) if num2 % 1 == 0 else num2
    res_final = int(res) if res % 1 == 0 else res
    
    return f"{n1_str} {simbolo} {n2_str}", res_final

def capturar_procesos():
    limpiar_pantalla()
    n = pedir_entero_positivo("# Procesos: ")
    procesos = []
    ids_registrados = set()

    for i in range(n):
        print(f"\n--- Proceso {i + 1} ---")
        while True:
            nombre = input("Nombre: ").strip()
            if nombre != "":
                break
            print("Error: El nombre no puede estar vacío.")

        operacion_str, resultado = capturar_operacion_y_datos()

        while True:
            id_prog = pedir_entero_positivo("ID: ")
            if id_prog in ids_registrados:
                print(f"Error: El ID {id_prog} ya existe. Ingresa uno único.")
            else:
                ids_registrados.add(id_prog)
                break

        tme = pedir_entero_positivo("TME: ")
        procesos.append(Proceso(id_prog, nombre, operacion_str, resultado, tme))

    return procesos

def crear_lotes(procesos, capacidad=5):
    lotes = []
    for i in range(0, len(procesos), capacidad):
        lotes.append(procesos[i:i + capacidad])
    return lotes

def mostrar_interfaz(lotes_pendientes, lote_actual, proceso_actual, terminados, reloj):
    limpiar_pantalla()
    print(f"No. Lotes Pendientes: {lotes_pendientes}\n")

    # Columna 1: Lote Trabajando
    col1 = ["Lote Trabajando", f"{'ID':<6}{'TME':<6}"]
    for p in lote_actual:
        col1.append(f"{p.id_prog:<6}{p.tme:<6}")
    while len(col1) < 7:
        col1.append("")
    col1.append(f"Contador: {reloj}")

    # Columna 2: Proceso en Ejecución
    col2 = ["Proceso en Ejecución"]
    if proceso_actual:
        tr = proceso_actual.tme - proceso_actual.tt
        col2.append(f"Nombre   {proceso_actual.nombre}")
        col2.append(f"Ope      {proceso_actual.operacion_str}")
        col2.append(f"ID       {proceso_actual.id_prog}")
        col2.append(f"TME      {proceso_actual.tme}")
        col2.append(f"TT       {proceso_actual.tt}")
        col2.append(f"TR       {tr}")
    else:
        col2.append("(Ninguno)")

    # Columna 3: Terminados
    col3 = ["Terminados", f"{'ID':<6}{'Ope':<16}{'Res':<10}"]
    for item in terminados:
        if isinstance(item, str):
            col3.append(item)
        else:
            col3.append(f"{item.id_prog:<6}{item.operacion_str:<16}{str(item.resultado):<10}")

    filas = max(len(col1), len(col2), len(col3))
    while len(col1) < filas:
        col1.append("")
    while len(col2) < filas:
        col2.append("")
    while len(col3) < filas:
        col3.append("")

    for i in range(filas):
        print(f"{col1[i]:<24} {col2[i]:<28} {col3[i]}")

def simular(lotes):
    reloj = 0
    terminados = []
    total = len(lotes)

    for idx, lote in enumerate(lotes):
        pendientes = total - (idx + 1)
        cola = list(lote)

        while cola:
            p = cola.pop(0)
            while p.tt < p.tme:
                mostrar_interfaz(pendientes, cola, p, terminados, reloj)
                time.sleep(1)
                p.tt += 1
                reloj += 1
            terminados.append(p)

        terminados.append(f"-- Fin Lote {idx + 1} --")

    mostrar_interfaz(0, [], None, terminados, reloj)
    print("\n>>> FIN DE LA SIMULACION - TODOS LOS LOTES EJECUTADOS <<<")
    input("Presione ENTER para salir...")

def main():
    procesos = capturar_procesos()
    lotes = crear_lotes(procesos)
    
    limpiar_pantalla()
    print("=" * 50)
    print("  Captura completada con éxito.")
    print(f"  Total de procesos registrados: {len(procesos)}")
    print(f"  Total de lotes generados: {len(lotes)}")
    print("=" * 50)
    input("\nPresione ENTER para iniciar la ejecución de los lotes...")
    
    simular(lotes)

if __name__ == "__main__":
    main()


