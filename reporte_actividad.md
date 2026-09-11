# REPORTE DE PRÁCTICA DE LABORATORIO

## 1. Datos Personales
- **Nombre del Alumno:** [Tu Nombre Completo Aquí]
- **Código de Estudiante:** [Tu Código / Matrícula Aquí]
- **Carrera:** Ingeniería en Computación / Informática

## 2. Datos de la Materia
- **Materia:** Seminario de Solución de Problemas de Sistemas Operativos / Sistemas Operativos
- **Profesor:** [Nombre de tu Profesor/a]
- **Sección:** [Ejemplo: D01]

## 3. Número y Título de la Actividad
- **Actividad:** Actividad #2 (o la que corresponda)
- **Tema:** Simulación de Procesamiento por Lotes

---

## 4. Objetivo de la Actividad
Comprender y modelar el funcionamiento de los primeros sistemas operativos mediante la simulación de un esquema de **Procesamiento por Lotes (Batch Processing)**, implementando la captura, validación de datos, conformación de lotes con capacidad fija de 5 procesos, control de tiempos de ejecución (TME, transcurrido y restante) y despliegue continuo de información en pantalla.

---

## 5. Notas acerca del Lenguaje de Programación

### Lenguaje Seleccionado: Python 3
**Razón de elección:**
Se eligió Python debido a su sintaxis clara, legible y directa, lo que permite enfocarse en la lógica del sistema operativo y en el flujo de los procesos en lugar de lidiar con problemas de bajo nivel o gestión manual de memoria. Además, cuenta con módulos nativos como `time` y `os` que facilitan el control del reloj segundo a segundo y la actualización de la pantalla en consola sin necesidad de librerías externas.

### Tipos de Datos Abstractos (TDA) y Estructuras de Datos Utilizadas
1. **Clase / Objeto `Proceso`:**  
   Se implementó una clase sencilla para representar a cada proceso con sus atributos esenciales:
   - `id_prog`: Identificador numérico único del programa.
   - `nombre`: Nombre del programador responsable.
   - `operacion_str`: Cadena representativa de la operación y datos (ej. `12 + 4`).
   - `resultado`: Resultado numérico tras evaluar la operación.
   - `tme`: Tiempo Máximo Estimado de ejecución en segundos.
   - `tt`: Tiempo transcurrido en la CPU.

2. **Listas (`list` en Python):**  
   - Se utilizaron listas dinámicas para almacenar todos los procesos capturados.
   - Se emplearon listas como **Colas FIFO (First In, First Out)** para gestionar el lote en ejecución: el proceso en turno se extrae con `cola.pop(0)` para ser atendido.
   - Se usó una lista de listas (`terminados_por_lote`) para agrupar y mostrar los procesos finalizados separados por cada lote.

3. **Conjuntos (`set`):**  
   - Se utilizó un conjunto (`ids_registrados`) para validar de manera rápida y eficiente que no existan IDs duplicados al momento de la captura.

---

## 6. ¿Cómo se solucionó la práctica? (Descripción de la Solución)

El desarrollo del simulador se dividió en tres fases principales:

1. **Fase de Captura y Validación de Datos:**
   - Se solicita al usuario el número total de procesos $N$.
   - En un ciclo iterativo, se capturan uno a uno los datos de cada proceso validando lo siguiente:
     - **ID único:** No se permite que se repita ningún ID previamente registrado y debe ser un entero positivo.
     - **Nombre del programador:** No puede quedar vacío.
     - **Operación a realizar y datos:** Se solicita la operación (+, -, *, /, residuo) con sus respectivos datos numéricos (Dato 1 y Dato 2).
     - **Validación de operaciones:** Solo se aceptan `+`, `-`, `*`, `/`, `%` o `residuo`. Si la operación es división o residuo, se valida que el segundo dato no sea cero para evitar errores matemáticos.
     - **Tiempo Máximo Estimado (TME):** Debe ser un entero positivo mayor a cero.

2. **Fase de Segmentación en Lotes:**
   - La lista global de procesos capturados se divide en bloques de máximo 5 elementos utilizando rebanado de listas (`slicing`).
   - El número inicial de lotes pendientes se calcula restando el lote actualmente activo al total de lotes.

3. **Fase de Simulación y Ejecución (Diseño en 3 Columnas):**
   - La pantalla se organiza en 3 columnas horizontales dinámicas tal como se especificó en la pizarra:
     - **Superior:** `No. Lotes Pendientes: X`
     - **Columna 1 (Lote Trabajando):** Lista de procesos en espera del lote actual con `ID` y `TME`, seguido en la parte inferior por el `Contador: X` (reloj global).
     - **Columna 2 (Proceso en Ejecución):** Información detallada del proceso activo: `Nombre`, `Ope` (operación), `ID`, `TME`, `TT` (tiempo transcurrido) y `TR` (tiempo restante).
     - **Columna 3 (Terminados):** Historial con columnas `ID`, `Ope` y `Res`, marcando el fin de cada lote con `-- Fin Lote X --`.
   - Con un ciclo que se actualiza segundo a segundo (`time.sleep(1)`):
     - Se limpia y redibuja la pantalla en cada segundo (`limpiar_pantalla()`), mostrando el avance del reloj y los procesos.
     - Se incrementa el **Contador** global y el **TT** del proceso, decrementando su **TR**.
   - Al concluir el TME del proceso, este pasa a la columna de terminados con su resultado y se atiende el siguiente proceso del lote.
   - Al terminar todos los procesos de un lote, el sistema avanza automáticamente al siguiente lote disminuyendo el contador de lotes pendientes.

4. **Fin de la Simulación:**
   - Al procesar el último lote, la pantalla se actualiza con el estado final (0 lotes pendientes, proceso en ejecución en blanco y la lista completa de terminados) y se pausa la ejecución (`input`) para observación.

---

## 7. Conclusiones

La realización de esta práctica permitió comprender de manera práctica los conceptos fundamentales de los sistemas operativos tempranos (sistemas por lotes). Se observó cómo los trabajos se agrupaban para ejecutarse secuencialmente sin intervención interactiva del usuario una vez iniciada la simulación. 

Asimismo, se reforzó la importancia de la validación estricta de datos de entrada en cualquier sistema computacional para evitar inconsistencias (como IDs duplicados o divisiones entre cero) y el uso adecuado de estructuras tipo Cola (FIFO) para el despacho ordenado de procesos.

---

## 8. Evidencias de Ejecución (Capturas de Pantalla)

*(Inserta aquí las capturas de pantalla de la ejecución de tu programa en consola)*

1. **Captura 1:** Entrada de datos y validaciones (IDs duplicados o TME <= 0).
2. **Captura 2:** Simulación en curso (mostrando Lote en ejecución, Proceso actual y Procesos terminados).
3. **Captura 3:** Fin de la simulación con el resumen total y el reloj global detenido.
