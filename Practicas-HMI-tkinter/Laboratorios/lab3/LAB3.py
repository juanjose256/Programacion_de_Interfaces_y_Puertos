"""
Lab Tk-3 — Indicadores Visuales con Canvas (versión propia)
Programación de Interfaces y Puertos

Objetivo: dibujar en Canvas indicadores tipo LED, barra de nivel y dial
analógico, con animación mediante after().

Incluye las 3 actividades del manual:
  8) Segundo dial (Presión) además del de Temperatura
  9) Aviso (messagebox) cuando el tanque baja del 15%
  10) Botones "Llenar" y "Vaciar" que mueven el nivel 10% por clic
"""

import math
import random
import tkinter as tk
from tkinter import messagebox


# Paleta propia: carbón + morado/cian (distinta a la del manual)
FONDO = "#18181b"
PANEL = "#0a0a0b"
TEXTO = "#d4d4d8"
TEXTO_SEC = "#71717a"
MORADO = "#a78bfa"
CIAN = "#22d3ee"


class LED:
    """Indicador circular con colores de estado."""
    PALETA = {
        "verde": ("#4ade80", "#166534"),
        "rojo": ("#f87171", "#7f1d1d"),
        "ambar": ("#fbbf24", "#78350f"),
        "apagado": ("#3f3f46", "#27272a"),
    }

    def __init__(self, parent, etiqueta, fila):
        self.lienzo = tk.Canvas(parent, width=22, height=22, bg=PANEL, highlightthickness=0)
        self.lienzo.grid(row=fila, column=0, padx=(6, 4), pady=3)
        relleno, borde = self.PALETA["apagado"]
        self.circulo = self.lienzo.create_oval(2, 2, 20, 20, fill=relleno, outline=borde, width=2)
        tk.Label(parent, text=etiqueta, bg=PANEL, fg=TEXTO, font=("Segoe UI", 9)
                  ).grid(row=fila, column=1, sticky="w")

    def estado(self, nombre):
        relleno, borde = self.PALETA.get(nombre, self.PALETA["apagado"])
        self.lienzo.itemconfig(self.circulo, fill=relleno, outline=borde)


class DialAnalogico:
    """Dial semicircular con aguja que rota según el valor."""

    def __init__(self, parent, titulo, unidad, color, minimo=0, maximo=100):
        marco = tk.LabelFrame(parent, text=titulo, bg=FONDO, fg=TEXTO_SEC, font=("Segoe UI", 9))
        marco.pack(side=tk.LEFT, padx=8, pady=10)

        self.min, self.max, self.color = minimo, maximo, color
        self.cx, self.cy, self.radio = 90, 135, 58

        self.lienzo = tk.Canvas(marco, width=180, height=170, bg=PANEL, highlightthickness=0)
        self.lienzo.pack(padx=6, pady=6)
        self.lienzo.create_arc(22, 20, 158, 156, start=0, extent=180, outline="#3f3f46", width=3)

        for i, valor in enumerate(range(minimo, maximo + 1, (maximo - minimo) // 5)):
            angulo = math.radians(180 - (180 * i / 5))
            x1 = self.cx + (self.radio - 8) * math.cos(angulo)
            y1 = self.cy - (self.radio - 8) * math.sin(angulo)
            x2 = self.cx + self.radio * math.cos(angulo)
            y2 = self.cy - self.radio * math.sin(angulo)
            self.lienzo.create_line(x1, y1, x2, y2, fill="#52525b", width=2)

        self.aguja = self.lienzo.create_line(
            self.cx, self.cy, self.cx - self.radio, self.cy, fill=color, width=3, capstyle=tk.ROUND
        )
        self.lbl_valor = tk.Label(marco, text=f"-- {unidad}", bg=FONDO, fg=color,
                                    font=("Consolas", 13, "bold"))
        self.lbl_valor.pack(pady=(0, 6))
        self.unidad = unidad

    def actualizar(self, valor):
        valor = max(self.min, min(self.max, valor))
        proporcion = (valor - self.min) / (self.max - self.min)
        angulo = math.radians(180 - 180 * proporcion)
        xp = self.cx + self.radio * math.cos(angulo)
        yp = self.cy - self.radio * math.sin(angulo)
        self.lienzo.coords(self.aguja, self.cx, self.cy, xp, yp)
        self.lbl_valor.config(text=f"{valor:.1f} {self.unidad}")


class TableroCanvas:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Lab Tk-3 — Tablero de Indicadores")
        self.raiz.geometry("760x420")
        self.raiz.configure(bg=FONDO)

        self.nivel_tanque = 50.0
        self.temperatura = 25.0
        self.presion = 1013.0
        self.aviso_enviado = False

        self._construir_leds()
        self._construir_tanque()

        # Actividad 8: usar la clase DialAnalogico para dos dials
        contenedor_dials = tk.Frame(self.raiz, bg=FONDO)
        contenedor_dials.grid(row=0, column=2, columnspan=2, sticky="n")
        self.dial_temp = DialAnalogico(contenedor_dials, "Temperatura", "°C", "#f87171", 0, 100)
        self.dial_pres = DialAnalogico(contenedor_dials, "Presión", "hPa", CIAN, 950, 1050)

        self._construir_controles()
        self._corriendo = False

    # ── LEDs de estado ───────────────────────────────────────────
    def _construir_leds(self):
        marco = tk.LabelFrame(self.raiz, text="Estado del sistema", bg=FONDO,
                                fg=TEXTO_SEC, font=("Segoe UI", 9))
        marco.grid(row=0, column=0, padx=14, pady=12, sticky="nw")

        self.led_conexion = LED(marco, "Conexión serial", 0)
        self.led_sensor = LED(marco, "Sensor OK", 1)
        self.led_alarma = LED(marco, "Alarma activa", 2)

    # ── Barra de tanque (Actividades 9 y 10) ────────────────────
    def _construir_tanque(self):
        marco = tk.LabelFrame(self.raiz, text="Nivel de tanque", bg=FONDO,
                                fg=TEXTO_SEC, font=("Segoe UI", 9))
        marco.grid(row=0, column=1, padx=8, pady=12, sticky="n")

        self.lienzo_tanque = tk.Canvas(marco, width=80, height=170, bg=PANEL, highlightthickness=0)
        self.lienzo_tanque.pack(padx=10, pady=8)
        self.lienzo_tanque.create_rectangle(10, 8, 70, 160, outline="#52525b", width=2)
        self.barra = self.lienzo_tanque.create_rectangle(12, 158, 68, 158, fill=MORADO, outline="")

        self.lbl_nivel = tk.Label(marco, text="50 %", bg=FONDO, fg=MORADO, font=("Consolas", 12, "bold"))
        self.lbl_nivel.pack()

        # Actividad 10: botones Llenar / Vaciar
        fila_botones = tk.Frame(marco, bg=FONDO)
        fila_botones.pack(pady=6)
        tk.Button(fila_botones, text="▲ Llenar", command=lambda: self._ajustar_nivel(10),
                   bg="#166534", fg="white", relief=tk.FLAT, padx=6).pack(side=tk.LEFT, padx=3)
        tk.Button(fila_botones, text="▼ Vaciar", command=lambda: self._ajustar_nivel(-10),
                   bg="#7f1d1d", fg="white", relief=tk.FLAT, padx=6).pack(side=tk.LEFT, padx=3)

        self._dibujar_tanque()

    def _ajustar_nivel(self, delta):
        self.nivel_tanque = max(0, min(100, self.nivel_tanque + delta))
        self._dibujar_tanque()

    def _dibujar_tanque(self):
        pct = self.nivel_tanque
        altura_total = 150
        y_top = 158 - altura_total * (pct / 100)
        color = "#4ade80" if pct > 50 else ("#fbbf24" if pct > 20 else "#f87171")
        self.lienzo_tanque.coords(self.barra, 12, y_top, 68, 158)
        self.lienzo_tanque.itemconfig(self.barra, fill=color)
        self.lbl_nivel.config(text=f"{pct:.0f} %", fg=color)

        # Actividad 9: aviso cuando baja del 15%
        if pct < 15 and not self.aviso_enviado:
            self.aviso_enviado = True
            messagebox.showwarning("Nivel bajo", f"El tanque está al {pct:.0f}%. ¡Revisa el suministro!")
        elif pct >= 15:
            self.aviso_enviado = False

    # ── Controles de simulación ──────────────────────────────────
    def _construir_controles(self):
        marco = tk.Frame(self.raiz, bg=FONDO)
        marco.grid(row=1, column=0, columnspan=4, pady=10)
        self.boton_sim = tk.Button(
            marco, text="▶ Iniciar simulación", command=self._alternar_simulacion,
            bg=MORADO, fg="#18181b", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=14, pady=6,
        )
        self.boton_sim.pack()

    def _alternar_simulacion(self):
        self._corriendo = not self._corriendo
        self.boton_sim.config(text="⏸ Pausar" if self._corriendo else "▶ Iniciar simulación")
        if self._corriendo:
            self._tick()

    def _tick(self):
        if not self._corriendo:
            return
        self.temperatura = max(15, min(95, self.temperatura + random.uniform(-0.6, 0.9)))
        self.presion = max(950, min(1050, self.presion + random.uniform(-1.0, 1.0)))
        self.nivel_tanque = max(0, min(100, self.nivel_tanque + random.uniform(-1.2, 1.2)))

        self.dial_temp.actualizar(self.temperatura)
        self.dial_pres.actualizar(self.presion)
        self._dibujar_tanque()

        self.led_conexion.estado("verde")
        self.led_sensor.estado("verde")
        self.led_alarma.estado("rojo" if self.temperatura > 70 else "apagado")

        self.raiz.after(250, self._tick)

    # ------------------------------------------------------------------
    def ejecutar(self):
        self.raiz.mainloop()


if __name__ == "__main__":
    TableroCanvas().ejecutar()