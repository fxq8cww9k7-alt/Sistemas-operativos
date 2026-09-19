# REPORTE DE PRÁCTICA DE LABORATORIO

## 1. Datos Personales
- **Nombre del Alumno:** [Tu Nombre Completo Aquí]
- **Código de Estudiante:** [Tu Código / Matrícula Aquí]
- **Carrera:** Ingeniería en Computación / Informática

## 2. Datos de la Materia
- **Materia:** Sistemas Operativos / Seminario de Solución de Problemas de Sistemas Operativos
- **Profesor:** [Nombre de tu Profesor/a]
- **Sección:** [Ejemplo: D01]

## 3. Número y Título de la Actividad
- **Actividad:** Actividad #2 / Programa 2
- **Tema:** Simulación de Procesamiento por Lotes con Multiprogramación Básica (Interrupciones por E/S, Errores y Control de Ejecución)

---

## 4. Objetivo de la Actividad
Comprender y modelar el comportamiento de la gestión de procesos en los esquemas de multiprogramación por lotes, implementando la generación interna de trabajos con operaciones aritméticas válidas, la transición de estados de un proceso (Ejecución, Espera por E/S, Terminación normal y Terminación por error), la atención a interrupciones en tiempo real mediante teclado (teclas E, W, P, C) y el despliegue sincronizado en pantalla mediante una interfaz dividida en tres columnas con registro histórico de lotes terminados.

---

## 5. Notas acerca del Lenguaje de Programación

### Lenguaje Seleccionado: Python 3
**Razón de elección:**
Se seleccionó Python 3 debido a su sintaxis concisa y su potente biblioteca estándar, la cual permite enfocarse en la lógica del sistema operativo y en la máquina de estados de los procesos sin la sobrecarga de gestión manual de memoria o dependencias externas complejas. El uso de módulos nativos como `time`, `random`, `os` y `msvcrt` permite un control preciso del tiempo de CPU y de las entradas por teclado en tiempo real bajo entorno Windows.

### Tipos de Datos Abstractos (TDA) y Estructuras de Datos Utilizadas
1. **Clase / Objeto `Proceso`:**  
   Representa la unidad básica de trabajo (PCB simplificado) con los siguientes atributos esenciales:
   - `id_prog`: Identificador numérico único del proceso (consecutivo 1..N).
   - `operacion_str`: Cadena representativa de la operación matemática asignada (ej. `50 * 0`, `12 + 4`).
   - `resultado`: Resultado numérico evaluado o la cadena `"Error"` si el proceso fue abortado.
   - `tme`: Tiempo Máximo Estimado de ejecución asignado aleatoriamente (5 a 20 segundos).
   - `tt`: Tiempo Transcurrido que el proceso ha ocupado la CPU.
   - `num_lote`: Número del lote al que pertenece el proceso para su trazabilidad en terminados.

2. **Listas Dinámicas (`list`):**  
   - Se utilizaron como **Colas FIFO (First In, First Out)** para gestionar los procesos del lote en ejecución. El proceso en turno se extrae con `cola.pop(0)`.
   - En caso de interrupción por E/S, la lista permite reencolar el proceso al final mediante `cola.append(p)`.

3. **Módulo `msvcrt` (Entrada no bloqueante de teclado):**  
   - Permite consultar si el usuario ha presionado una tecla sin suspender la ejecución del programa (`msvcrt.kbhit()`).
   - Cada segundo de CPU se fragmenta en 10 intervalos de `0.1s`, logrando que la detección de las teclas sea fluida e instantánea.

---

## 6. ¿Cómo se solucionó la práctica? (Descripción de la Solución)

El desarrollo del simulador se estructuró en cuatro fases fundamentales:

### Fase 1: Generación Interna de Procesos y Validaciones
A diferencia de la práctica anterior, ya no se requiere la captura manual ni el nombre del programador. El usuario únicamente especifica el número total de trabajos inicial. Internamente, el programa genera cada proceso garantizando:
- **Identificador (ID):** Consecutivo único a partir del 1.
- **TME (Tiempo Máximo Estimado):** Generado aleatoriamente en el rango de 5 a 20 segundos (`random.randint(5, 20)`).
- **Operaciones Aritméticas:** Selección aleatoria de operadores (`+`, `-`, `*`, `/`, `%`) con operandos enteros entre 0 y 100.
- **Validación matemática:** Si la operación es división (`/`) o residuo (`%`), se asegura que el divisor sea distinto de cero para evitar excepciones aritméticas.

### Fase 2: Segmentación y Asignación de Lotes
- La lista total de procesos se divide en bloques de máximo 5 elementos utilizando rebanado de listas (`slicing`).
- A cada proceso se le estampa su número de lote correspondiente (`p.num_lote = num_lote`), asegurando que aun si sufre interrupciones, conserve su pertenencia al lote original.

### Fase 3: Motor de Simulación y Manejo de Teclas
Durante la ejecución de un proceso en la CPU, se evalúa segundo a segundo el paso del tiempo y las posibles señales de entrada:
- **Tecla `E` (Interrupción por Entrada/Salida):**  
  El proceso en ejecución es desalojado de la CPU de forma inmediata. Conserva su tiempo transcurrido acumulado (`tt`) y regresa al final de la cola del lote actual (`cola.append(p)`), cediendo el procesador al siguiente trabajo disponible.
- **Tecla `W` (Terminación por Error):**  
  El proceso activo termina de manera prematura. Su resultado se sobrescribe con `"Error"` y se envía inmediatamente a la lista de **Terminados**, registrando su salida sin concluir su TME restante.
- **Tecla `P` (Pausa) y Tecla `C` (Continuar):**  
  Al presionar `P`, el avance del reloj global y de los procesos se detiene por completo. El programa entra en un ciclo de espera que solo se desbloquea cuando el usuario presiona la tecla `C`.

### Fase 4: Despliegue Visual en 3 Columnas (Formato de Pizarra)
La consola se redibuja en cada segundo presentando el esquema formal definido en clase:
- **Encabezado superior:** `# Lotes Pendientes: X` (especifica los lotes que aún no han ingresado a la memoria/procesador).
- **Columna 1 — Lote trabajando:** Lista los procesos que esperan turno dentro del lote en ejecución, mostrando sus columnas `ID`, `TME` y `TT` (este último refleja el avance previo si el proceso fue interrumpido con `E`). Debajo de esta lista se muestra el `Contador: X` (reloj global).
- **Columna 2 — Ejecución:** Muestra la ficha técnica del proceso en uso de la CPU: `ID`, `Ope`, `TME`, `TT` y `TR` (Tiempo Restante).
- **Columna 3 — Terminados:** Historial acumulado de todos los trabajos completados con las columnas `ID`, `Ope`, `Res` (resultado numérico o `"Error"`) y `NL` (Número de Lote). Al concluir cada lote, se inserta una línea horizontal divisoria (`------------------------------------`).

---

## 7. Conclusiones

La realización del Programa 2 permitió comprender la transición de un modelo estricto de procesamiento por lotes hacia los conceptos iniciales de **multiprogramación y gestión de estados de procesos**. 

Se comprobó experimentalmente la ventaja del mecanismo de interrupción por Entrada/Salida: cuando un proceso requiere esperar un recurso, desalojar la CPU y cederla a otro proceso evita el desperdicio de ciclos de reloj, maximizando el rendimiento del sistema. 

Asimismo, se aprendió a manejar la sincronización entre eventos externos en tiempo real (teclas del usuario) y el avance de un reloj simulado, reforzando la importancia de mantener la consistencia entre los tiempos de servicio de cada proceso, los tiempos restantes y el contador global del sistema operativo.

---

## 8. Evidencias de Ejecución (Capturas de Pantalla)

*(Inserta aquí las capturas de pantalla de la ejecución de tu programa en consola)*

1. **Captura 1: Inicio y Generación de Lotes:** Entrada del número inicial de procesos y confirmación de lotes creados.
2. **Captura 2: Proceso Interrumpido por E/S (Tecla 'E'):** Proceso esperando en *Lote trabajando* mostrando su `TT > 0` tras haber sido interrumpido.
3. **Captura 3: Terminación por Error (Tecla 'W') y Columna NL:** Procesos en la columna de *Terminados* mostrando `Res: Error`, su respectivo número de lote (`NL`) y la línea divisoria de fin de lote.
4. **Captura 4: Estado de Pausa (Tecla 'P') y Fin de la Simulación:** Demostración del reloj pausado y pantalla final con 0 lotes pendientes y todos los trabajos concluidos.
