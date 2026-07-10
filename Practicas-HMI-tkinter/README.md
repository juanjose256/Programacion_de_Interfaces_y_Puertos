# Laboratorios Tkinter — Interfaces Gráficas con Python

Manual de prácticas de **Programación de Interfaces y Puertos** (Ingeniería en Sistemas Computacionales). Desarrollo de interfaces HMI (Human-Machine Interface) funcionales para comunicar una PC con microcontroladores, transitando desde la ventana básica hasta un dashboard serial en tiempo real.

## Requisitos de Instalación
* **Python 3.8+** (incluye `tkinter`).
* **Librerías necesarias**:
  ```bash
  pip install matplotlib pyserial pandas
  ```

---

## Detalle de Laboratorios

### 1. Primera Ventana y Widgets Esenciales (Lab Tk-1)
* **Objetivos**: `tk.Tk`, `Label`, `Button`, `Entry`, `StringVar`, `messagebox`.
* **Descripción**: Construcción de la primera ventana interactiva con Python. Se explora el *event loop* y el manejo de widgets fundamentales.
* **Evidencias**:
  <table>
    <tr>
      <td><img src="Laboratorios/lab1/evidencia/Pantalla_principal.png" width="180" alt="Pantalla Principal"></td>
      <td><img src="Laboratorios/lab1/evidencia/Saludar.png" width="180" alt="Saludar"></td>
      <td><img src="Laboratorios/lab1/evidencia/Mayusculas.png" width="180" alt="Mayusculas"></td>
      <td><img src="Laboratorios/lab1/evidencia/Salir.png" width="180" alt="Salir"></td>
    </tr>
  </table>

### 2. Layout y Organización de Widgets (Lab Tk-2)
* **Objetivos**: `pack`, `grid`, `place`, `LabelFrame`, `ttk.Notebook`, `ttk.Progressbar`.
* **Descripción**: Dominio de la colocación y alineación estructurada de widgets. Uso de pestañas (`ttk.Notebook`) y organización modular de la interfaz.
* **Evidencias**:
  <table>
    <tr>
      <td><img src="Laboratorios/lab2/evidencia/2026-07-09_11-13.png" width="180" alt="Evidencia 1"></td>
      <td><img src="Laboratorios/lab2/evidencia/2026-07-09_11-14.png" width="180" alt="Evidencia 2"></td>
      <td><img src="Laboratorios/lab2/evidencia/2026-07-09_11-14_1.png" width="180" alt="Evidencia 3"></td>
    </tr>
    <tr>
      <td><img src="Laboratorios/lab2/evidencia/2026-07-09_11-14_2.png" width="180" alt="Evidencia 4"></td>
      <td><img src="Laboratorios/lab2/evidencia/2026-07-09_11-15.png" width="180" alt="Evidencia 5"></td>
      <td><img src="Laboratorios/lab2/evidencia/2026-07-09_11-15_1.png" width="180" alt="Evidencia 6"></td>
    </tr>
  </table>

### 3. Canvas — Indicadores Visuales y Animaciones (Lab Tk-3)
* **Objetivos**: `Canvas`, `create_oval`, `create_rectangle`, `itemconfig`, `after()`.
* **Descripción**: Dibujo geométrico y creación de animaciones. Ideal para simular indicadores visuales tipo LED o barras dinámicas.
* **Evidencias**:
  <table>
    <tr>
      <td><img src="Laboratorios/lab3/evidencia/Captura%20desde%202026-07-09%2011-11-04.png" width="240" alt="Evidencia 1"></td>
      <td><img src="Laboratorios/lab3/evidencia/Captura%20desde%202026-07-09%2011-11-20.png" width="240" alt="Evidencia 2"></td>
      <td><img src="Laboratorios/lab3/evidencia/Captura%20desde%202026-07-09%2011-11-42.png" width="240" alt="Evidencia 3"></td>
    </tr>
  </table>

### 4. Diseño con Figma → Traducción a Tkinter (Lab Tk-4)
* **Objetivos**: Prototipado UX/UI, Sistemas de diseño, Mockup a Código.
* **Descripción**: Diseño preliminar de una interfaz HMI profesional en Figma y su traducción exacta y estructurada a código Tkinter.
* **Evidencias**:
  <table>
    <tr>
      <td><img src="Laboratorios/lab4/evidencia/BocetoFigma.png" width="260" alt="Boceto Figma"></td>
      <td><img src="Laboratorios/lab4/evidencia/Python.png" width="260" alt="Implementacion Python"></td>
    </tr>
  </table>

### 5. Menús, Diálogos y Eventos de Teclado (Lab Tk-5)
* **Objetivos**: `Menu`, `filedialog`, `colorchooser`, `bind`, `event`, `Toplevel`.
* **Descripción**: Creación de menús profesionales, atajos de teclado, cuadros de diálogo para abrir/guardar archivos, paletas de colores y ventanas flotantes secundarias.
* **Evidencias**:
  <table>
    <tr>
      <td><img src="Laboratorios/lab5/evidencia/Captura%20desde%202026-07-09%2013-38-13.png" width="180" alt="Evidencia 1"></td>
      <td><img src="Laboratorios/lab5/evidencia/Captura%20desde%202026-07-09%2013-38-52.png" width="180" alt="Evidencia 2"></td>
      <td><img src="Laboratorios/lab5/evidencia/Captura%20desde%202026-07-09%2013-39-06.png" width="180" alt="Evidencia 3"></td>
    </tr>
    <tr>
      <td><img src="Laboratorios/lab5/evidencia/Captura%20desde%202026-07-09%2013-39-31.png" width="180" alt="Evidencia 4"></td>
      <td colspan="2"><img src="Laboratorios/lab5/evidencia/Captura%20desde%202026-07-09%2013-39-54.png" width="180" alt="Evidencia 5"></td>
    </tr>
  </table>

### 6. Gráfica en Tiempo Real con Matplotlib (Lab Tk-6)
* **Objetivos**: `FigureCanvasTkAgg`, `animation`, `after()`, `deque`, multi-eje.
* **Descripción**: Embeber gráficos dinámicos de `matplotlib` en la UI de Tkinter actualizándose periódicamente con `after()` sin congelar el hilo de ejecución principal.
* **Evidencias**:
  <table>
    <tr>
      <td><img src="Laboratorios/lab6/evidencia/Captura%20desde%202026-07-09%2014-11-27.png" width="260" alt="Evidencia 1"></td>
      <td><img src="Laboratorios/lab6/evidencia/Captura%20desde%202026-07-09%2014-11-41.png" width="260" alt="Evidencia 2"></td>
    </tr>
  </table>

### 7. Tkinter + Hilos + Puerto Serial (Lab Tk-7)
* **Objetivos**: `threading`, `queue.Queue`, `pyserial`, arquitectura sin bloqueo.
* **Descripción**: Recepción de datos de sensores por puerto serial UART desde un microcontrolador usando un hilo secundario (background thread) y paso de datos seguro mediante colas (`queue.Queue`) al hilo de la interfaz.
* **Evidencias**:
  <br>
  <img src="Laboratorios/lab7/evidencia/2026-07-09_13-59.png" width="400" alt="Evidencia Serial Threading">

### 8. Dashboard Serial Completo (Lab Tk-8)
* **Objetivos**: Integración de interfaz oscura, gráficas matplotlib, alarmas visuales, registro en CSV, multihilo y puerto serial.
* **Descripción**: Proyecto integrador HMI definitivo. Reúne la comunicación serial multihilo, visualización gráfica en tiempo real de múltiples sensores, panel de control interactivo, log e historial con exportación CSV.
* **Evidencias**:
  <table>
    <tr>
      <td><img src="Laboratorios/lab8/evidencia/2026-07-09_14-16.png" width="260" alt="Evidencia 1"></td>
      <td><img src="Laboratorios/lab8/evidencia/evidencia.jpeg" width="260" alt="Evidencia 2"></td>
    </tr>
  </table>
