#!/usr/bin/env python3
"""
Lab Tk-4: Traducción fiel del mockup Figma -> Tkinter
Basado en el diseño con paleta #1e2736 / #0f172a / #2E75B6

No requiere Arduino ni sensores: esta práctica es puramente de
diseño de interfaz (Figma) y su traducción a código Tkinter.
Los placeholders (indicadores en '--', gráfica vacía) se conectan
a datos reales hasta los laboratorios Tk-6, Tk-7 y Tk-8.
"""
import tkinter as tk
from tkinter import scrolledtext

# ── Constantes de diseño (copiadas del inspector de Figma) ───
BG_ROOT = '#1e2736'   # fondo general
BG_PANEL = '#0f172a'  # fondo de paneles / tarjetas
BG_STRIP = '#111827'  # barra superior e inferior
ACENTO = '#2E75B6'    # botones, bordes activos
VERDE = '#22c55e'     # estado normal
ROJO = '#ef4444'      # alarma
AMARILLO = '#fbbf24'  # advertencia
TXT_PRI = '#e2e8f0'   # texto principal
TXT_SEC = '#94a3b8'   # texto secundario

FONT_TITLE = ('Arial', 11, 'bold')
FONT_VALUE = ('Courier New', 22, 'bold')
FONT_LABEL = ('Arial', 9)
FONT_BTN = ('Arial', 10, 'bold')

root = tk.Tk()
root.title('HMI Monitor — Interfaces y Puertos')
root.geometry('800x500')
root.resizable(False, False)
root.configure(bg=BG_ROOT)

# ── BARRA SUPERIOR ────────────────────────────────────────────
barra_top = tk.Frame(root, bg=BG_STRIP, height=44)
barra_top.pack(fill=tk.X)
barra_top.pack_propagate(False)

tk.Label(barra_top, text='\u2699 HMI Monitor de Proceso',
          bg=BG_STRIP, fg=TXT_PRI, font=('Arial', 12, 'bold')
          ).pack(side=tk.LEFT, padx=14, pady=10)

lbl_estado_cx = tk.Label(barra_top, text='\u25cf Desconectado',
                          bg=BG_STRIP, fg=ROJO, font=('Arial', 9, 'bold'))
lbl_estado_cx.pack(side=tk.RIGHT, padx=14)

# ── ÁREA PRINCIPAL ────────────────────────────────────────────
main = tk.Frame(root, bg=BG_ROOT)
main.pack(fill=tk.BOTH, expand=True)

# ── PANEL IZQUIERDO — indicadores ────────────────────────────
panel_izq = tk.Frame(main, bg=BG_PANEL, width=200)
panel_izq.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 4), pady=8)
panel_izq.pack_propagate(False)


def indicador(parent, etiqueta, unidad, color):
    f = tk.Frame(parent, bg=BG_PANEL)
    f.pack(fill=tk.X, padx=10, pady=6)
    tk.Label(f, text=etiqueta, bg=BG_PANEL, fg=TXT_SEC, font=FONT_LABEL
              ).pack(anchor='w')
    lbl = tk.Label(f, text=f'-- {unidad}', bg=BG_PANEL, fg=color, font=FONT_VALUE)
    lbl.pack(anchor='w')
    return lbl


lbl_temp = indicador(panel_izq, 'TEMPERATURA', '\u00b0C', ROJO)
lbl_pres = indicador(panel_izq, 'PRESI\u00d3N', 'hPa', ACENTO)
lbl_hum = indicador(panel_izq, 'HUMEDAD', '%', VERDE)
lbl_alt = indicador(panel_izq, 'ALTITUD', 'm', AMARILLO)

# ── PANEL CENTRAL — reservado para gráfica ───────────────────
panel_centro = tk.Frame(main, bg=BG_PANEL)
panel_centro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=8)

tk.Label(panel_centro, text='Gr\u00e1fica de tendencia',
          bg=BG_PANEL, fg=TXT_SEC, font=FONT_LABEL).pack(anchor='nw', padx=10, pady=6)

# Placeholder gris — se reemplaza con matplotlib en Lab Tk-6
cv_placeholder = tk.Canvas(panel_centro, bg='#0d1520', highlightthickness=0)
cv_placeholder.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
cv_placeholder.create_text(
    180, 100,
    text='[ Gr\u00e1fica \u2014 se a\u00f1ade en Lab Tk-6 ]',
    fill='#374151', font=('Arial', 10, 'italic'))

# ── PANEL DERECHO — controles ────────────────────────────────
panel_der = tk.Frame(main, bg=BG_PANEL, width=190)
panel_der.pack(side=tk.LEFT, fill=tk.Y, padx=(4, 8), pady=8)
panel_der.pack_propagate(False)

tk.Label(panel_der, text='CONTROL', bg=BG_PANEL, fg=TXT_SEC,
          font=FONT_LABEL).pack(anchor='w', padx=10, pady=(10, 4))

for txt, color in [('Conectar', VERDE), ('LED Verde ON', ACENTO),
                    ('LED Rojo ON', '#c55a11'), ('Desconectar', ROJO)]:
    tk.Button(panel_der, text=txt, bg=color, fg='white',
              font=('Arial', 9, 'bold'), relief=tk.FLAT, pady=5,
              cursor='hand2').pack(fill=tk.X, padx=10, pady=3)

tk.Label(panel_der, text='Umbral T\u00b0 (\u00b0C)', bg=BG_PANEL,
          fg=TXT_SEC, font=FONT_LABEL).pack(anchor='w', padx=10, pady=(16, 0))

tk.Scale(panel_der, from_=10, to=80, orient=tk.HORIZONTAL,
         bg=BG_PANEL, fg=TXT_PRI, highlightthickness=0,
         troughcolor='#374151', activebackground=ACENTO
         ).pack(fill=tk.X, padx=10)

# ── BARRA INFERIOR — log ─────────────────────────────────────
barra_bot = tk.Frame(root, bg=BG_STRIP, height=90)
barra_bot.pack(fill=tk.X, side=tk.BOTTOM)
barra_bot.pack_propagate(False)

log = scrolledtext.ScrolledText(barra_bot, height=4, bg='#0d1520',
                                 fg='#64748b', font=('Courier New', 8), relief=tk.FLAT)
log.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
log.insert(tk.END, '[00:00:00] Sistema iniciado\n')
log.insert(tk.END, '[00:00:00] Esperando conexi\u00f3n serial...\n')

root.mainloop()