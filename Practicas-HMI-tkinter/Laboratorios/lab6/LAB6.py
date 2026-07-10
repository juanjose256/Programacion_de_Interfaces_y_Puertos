#!/usr/bin/env python3
"""
Lab Tk-6: Gráfica de tiempo real embebida en Tkinter
FigureCanvasTkAgg + deque + root.after() — sin bloquear la UI

No requiere Arduino: los datos se simulan con random.gauss()
para poder probar el patrón de actualización. En Tk-7/Tk-8 esos
mismos datos vendrán del puerto serial vía una queue.Queue.
"""
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from collections import deque
import random

MAX_PTS = 200  # puntos visibles en la gráfica

root = tk.Tk()
root.title('Lab Tk-6 — Gráfica Tiempo Real')
root.geometry('900x520')
root.configure(bg='#1e2736')

# ── Datos simulados ───────────────────────────────────────────
hist_temp = deque(maxlen=MAX_PTS)
hist_pres = deque(maxlen=MAX_PTS)

# ── Figura matplotlib (tema oscuro) ──────────────────────────
fig = Figure(figsize=(9, 4.2), dpi=88, facecolor='#0f172a')
fig.subplots_adjust(left=0.07, right=0.93, top=0.88, bottom=0.12)

ax1 = fig.add_subplot(111)  # eje principal: temperatura
ax2 = ax1.twinx()           # eje secundario: presión

# Estilo del eje 1
ax1.set_facecolor('#111827')
ax1.tick_params(colors='#94a3b8', labelsize=8)
ax1.spines[:].set_color('#1e2736')
ax1.set_ylabel('Temperatura (°C)', color='#ef4444', fontsize=9)
ax1.tick_params(axis='y', labelcolor='#ef4444')
ax1.grid(True, alpha=0.15, color='#374151')
ax1.set_title('Tendencia de proceso — Temperatura y Presión',
               color='#e2e8f0', fontsize=9, pad=8)

# Estilo del eje 2
ax2.tick_params(colors='#94a3b8', labelsize=8)
ax2.spines[:].set_color('#1e2736')
ax2.set_ylabel('Presión (hPa)', color='#3b82f6', fontsize=9)
ax2.tick_params(axis='y', labelcolor='#3b82f6')

# Líneas vacías al inicio
linea_t, = ax1.plot([], [], '#ef4444', lw=1.5, label='Temperatura')
linea_p, = ax2.plot([], [], '#3b82f6', lw=1.5, label='Presión', alpha=0.8)
linea_umb = ax1.axhline(y=35, color='#fbbf24', ls='--', lw=1, alpha=0.7, label='Umbral T°')

# Leyenda combinada de ambos ejes
lin1, lab1 = ax1.get_legend_handles_labels()
lin2, lab2 = ax2.get_legend_handles_labels()
ax1.legend(lin1 + lin2, lab1 + lab2, loc='upper left', fontsize=7,
           facecolor='#1e2736', labelcolor='#e2e8f0')

# ── Canvas Tkinter ────────────────────────────────────────────
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 0))

# Barra de navegación de matplotlib (zoom, pan, guardar)
toolbar_frame = tk.Frame(root, bg='#1e2736')
toolbar_frame.pack(fill=tk.X, padx=8)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.config(bg='#1e2736')
toolbar.update()

# ── Panel de controles ────────────────────────────────────────
ctrl = tk.Frame(root, bg='#111827', height=44)
ctrl.pack(fill=tk.X, padx=0, pady=0)
ctrl.pack_propagate(False)

var_umbral = tk.DoubleVar(value=35.0)
tk.Label(ctrl, text='Umbral T°:', bg='#111827', fg='#94a3b8',
          font=('Arial', 9)).pack(side=tk.LEFT, padx=(12, 4), pady=10)
tk.Scale(ctrl, variable=var_umbral, from_=10, to=80, resolution=0.5,
         orient=tk.HORIZONTAL, bg='#111827', fg='#e2e8f0', length=120,
         highlightthickness=0, troughcolor='#374151'
         ).pack(side=tk.LEFT, pady=8)

lbl_t_val = tk.Label(ctrl, text='T: -- °C', bg='#111827', fg='#ef4444',
                      font=('Courier New', 11, 'bold'))
lbl_t_val.pack(side=tk.LEFT, padx=20)

lbl_p_val = tk.Label(ctrl, text='P: -- hPa', bg='#111827', fg='#3b82f6',
                      font=('Courier New', 11, 'bold'))
lbl_p_val.pack(side=tk.LEFT, padx=4)

corriendo = True


def pausar():
    global corriendo
    corriendo = not corriendo
    btn_pausa.config(text='\u25b6 Reanudar' if not corriendo else '\u23f8 Pausar')


btn_pausa = tk.Button(ctrl, text='\u23f8 Pausar', command=pausar,
                       bg='#374151', fg='white', font=('Arial', 9), relief=tk.FLAT, padx=10)
btn_pausa.pack(side=tk.RIGHT, padx=12, pady=8)

btn_clear = tk.Button(ctrl, text='\U0001F5D1 Limpiar',
                       command=lambda: [hist_temp.clear(), hist_pres.clear()],
                       bg='#374151', fg='white', font=('Arial', 9), relief=tk.FLAT, padx=10)
btn_clear.pack(side=tk.RIGHT, padx=4, pady=8)

# ── Loop de actualización ─────────────────────────────────────
t_sim = 25.0  # temperatura simulada
p_sim = 1013.25


def actualizar():
    global t_sim, p_sim
    if corriendo:
        t_sim += random.gauss(0, 0.3)
        t_sim = max(15, min(85, t_sim))
        p_sim += random.gauss(0, 0.1)

        hist_temp.append(t_sim)
        hist_pres.append(p_sim)

        if hist_temp:
            x = list(range(len(hist_temp)))
            linea_t.set_data(x, list(hist_temp))
            linea_p.set_data(x, list(hist_pres))

            ax1.set_xlim(0, max(len(hist_temp), 10))
            margin = 3
            ax1.set_ylim(min(hist_temp) - margin, max(hist_temp) + margin)
            ax2.set_ylim(min(hist_pres) - 1, max(hist_pres) + 1)

            # Actualizar línea de umbral
            linea_umb.set_ydata([var_umbral.get(), var_umbral.get()])

            lbl_t_val.config(text=f'T: {hist_temp[-1]:.1f} °C')
            lbl_p_val.config(text=f'P: {hist_pres[-1]:.2f} hPa')

            canvas.draw_idle()  # redibujar sin bloquear

    root.after(150, actualizar)  # siguiente actualización en 150 ms


actualizar()
root.mainloop()
