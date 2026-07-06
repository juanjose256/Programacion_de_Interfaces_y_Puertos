import serial, json, time
import serial.tools.list_ports
from statistics import mean, pstdev
from collections import deque
import os
import matplotlib

import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Detección dinámica de puerto serial (con fallback a /dev/ttyACM0)
# ------------------------------------------------------------------
puertos = [p.device for p in serial.tools.list_ports.comports()
           if 'ttyACM' in p.device or 'ttyUSB' in p.device]
PORT = puertos[0] if puertos else '/dev/ttyACM0'
print(f"Puerto detectado: {PORT}")

BAUD = 115200
INTERVALO_ESPERADO_MS = 500
TOLERANCIA_MS = 100

# Cuántos puntos mostrar en la ventana deslizante del gráfico
VENTANA_GRAFICO = 100

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # Esperar reset del Arduino

ts_anterior = None
deltas_ts = []       # intervalos reportados por el Arduino (ts)
bytes_totales = 0
t_inicio_medicion = None
tiempos_llegada = []  # timestamps del lado de Python (time.time())
temperaturas = []     # lista para almacenar temperaturas
tiempos_plot = []     # lista para almacenar tiempos en segundos (eje X)

# Variable para evitar envío redundante de comandos
ultimo_estado_led = None

# Configuración de Matplotlib para Graficación en Tiempo Real
plt.ion()  # Modo interactivo
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=False)
fig.canvas.manager.set_window_title('Telemetría de Temperatura y Jitter')

# Gráfico 1: Temperatura
line_temp, = ax1.plot([], [], 'r-o', label='Temperatura (°C)')
ax1.axhline(y=30, color='b', linestyle='--', label='Umbral (30°C)')
ax1.set_ylabel('Temperatura (°C)')
ax1.grid(True)
ax1.legend(loc='upper left')
ax1.set_title('Temperatura en Tiempo Real')

# Gráfico 2: Jitter (Deltas del timestamp de Arduino)
line_delta, = ax2.plot([], [], 'g-^', label='Intervalo (ms)')
ax2.axhline(y=INTERVALO_ESPERADO_MS, color='k', linestyle=':', label='Esperado (500ms)')
ax2.set_xlabel('Tiempo de ejecución (s)')
ax2.set_ylabel('Delta (ms)')
ax2.grid(True)
ax2.legend(loc='upper left')
ax2.set_title('Intervalo de Envío (Consistencia)')

plot_activo = True

def al_cerrar(event):
    global plot_activo
    plot_activo = False

fig.canvas.mpl_connect('close_event', al_cerrar)

try:
    while True:
        t_llegada = time.time()
        linea_bytes = ser.readline()
        if not linea_bytes:
            continue

        n_bytes = len(linea_bytes)
        bytes_totales += n_bytes

        if t_inicio_medicion is None:
            t_inicio_medicion = t_llegada

        # Se añade errors='ignore' para evitar caídas por bytes corruptos
        linea = linea_bytes.decode('utf-8', errors='ignore').strip()
        if not linea:
            continue

        try:
            datos = json.loads(linea)
        except json.JSONDecodeError:
            continue

        ts_actual = datos.get('ts')
        temp = datos.get('temp')
        led = datos.get('led')

        tiempos_llegada.append(t_llegada)
        t_relativo = t_llegada - t_inicio_medicion

        # Control del LED y guardado de datos
        if temp is not None:
            try:
                temp_float = float(temp)
                temperaturas.append(temp_float)
                tiempos_plot.append(t_relativo)

                # Control del LED optimizado para evitar reenvío redundante
                nuevo_estado = b'LED_ON\n' if temp_float > 30 else b'LED_OFF\n'
                if nuevo_estado != ultimo_estado_led:
                    ser.write(nuevo_estado)
                    ultimo_estado_led = nuevo_estado
            except (ValueError, TypeError):
                pass

        # Intervalo reportado por el Arduino (basado en millis())
        if ts_anterior is not None and ts_actual is not None:
            try:
                delta = int(ts_actual) - int(ts_anterior)
                if delta < 0:
                    delta += 2**32
                deltas_ts.append(delta)
            except (ValueError, TypeError):
                pass

        ts_anterior = ts_actual

        # Throughput acumulado
        t_transcurrido = t_llegada - t_inicio_medicion
        bytes_por_seg = bytes_totales / t_transcurrido if t_transcurrido > 0 else 0

        print(f"ts={ts_actual} ms | Temp: {temp}°C | LED: {led} | "
              f"{n_bytes} bytes | throughput acum: {bytes_por_seg:.1f} B/s")

        # Actualizar gráficos en tiempo real
        if plot_activo and matplotlib.get_backend().lower() != 'agg':
            # Temperatura
            line_temp.set_data(tiempos_plot[-VENTANA_GRAFICO:], temperaturas[-VENTANA_GRAFICO:])
            ax1.relim()
            ax1.autoscale_view()

            # Deltas/Jitter
            if len(deltas_ts) > 0:
                ultimos_tiempos = tiempos_plot[-len(deltas_ts):]
                line_delta.set_data(ultimos_tiempos[-VENTANA_GRAFICO:], deltas_ts[-VENTANA_GRAFICO:])
                ax2.relim()
                ax2.autoscale_view()

            # Refrescar interfaz de Matplotlib
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.001)

except KeyboardInterrupt:
    print("\nDeteniendo lectura por el usuario...")

finally:
    ser.close()
    print("Conexión serial cerrada.")
    
    # Desactivar modo interactivo para bloquear la ventana al final
    plt.ioff()

    # Mostrar resumen
    print("\n--- Resumen de la medición ---")
    print(f"Baudrate usado: {BAUD}")
    print(f"Mensajes recibidos: {len(tiempos_llegada)}")
    print(f"Bytes totales: {bytes_totales}")

    if t_inicio_medicion and tiempos_llegada:
        duracion = tiempos_llegada[-1] - t_inicio_medicion
        print(f"Duración total: {duracion:.2f} s")
        if duracion > 0:
            print(f"Throughput promedio: {bytes_totales/duracion:.2f} B/s")

    if deltas_ts:
        try:
            print(f"Intervalo promedio (Arduino ts): {mean(deltas_ts):.1f} ms")
            print(f"Desviación estándar: {pstdev(deltas_ts):.1f} ms")
            print(f"Intervalo mínimo: {min(deltas_ts)} ms")
            print(f"Intervalo máximo: {max(deltas_ts)} ms")
        except Exception as e:
            print(f"Error calculando estadísticas de intervalos: {e}")

    # Latencia entre llegadas medida en Python (jitter real del sistema)
    if len(tiempos_llegada) > 1:
        deltas_llegada = [
            (tiempos_llegada[i] - tiempos_llegada[i-1]) * 1000
            for i in range(1, len(tiempos_llegada))
        ]
        try:
            print(f"Intervalo promedio (reloj de Python): {mean(deltas_llegada):.1f} ms")
            print(f"Jitter (desv. estándar): {pstdev(deltas_llegada):.1f} ms")
        except Exception as e:
            print(f"Error calculando estadísticas del reloj: {e}")

    # Manejar salida del gráfico
    if plot_activo:
        if matplotlib.get_backend().lower() != 'agg':
            # Actualización final para asegurar que se dibuje todo
            line_temp.set_data(tiempos_plot[-VENTANA_GRAFICO:], temperaturas[-VENTANA_GRAFICO:])
            if len(deltas_ts) > 0:
                ultimos_tiempos = tiempos_plot[-len(deltas_ts):]
                line_delta.set_data(ultimos_tiempos[-VENTANA_GRAFICO:], deltas_ts[-VENTANA_GRAFICO:])
            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()
            
            print("\nCierra la ventana del gráfico para terminar el programa por completo.")
            plt.show()
        else:
            # Si estamos en modo headless, dibujar y guardar a PNG
            line_temp.set_data(tiempos_plot[-VENTANA_GRAFICO:], temperaturas[-VENTANA_GRAFICO:])
            if len(deltas_ts) > 0:
                ultimos_tiempos = tiempos_plot[-len(deltas_ts):]
                line_delta.set_data(ultimos_tiempos[-VENTANA_GRAFICO:], deltas_ts[-VENTANA_GRAFICO:])
            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()
            
            ruta_imagen = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'telemetria_reporte.png')
            fig.savefig(ruta_imagen)
            print(f"\nGráfico estático guardado con éxito en: {ruta_imagen} (modo sin pantalla detectado)")