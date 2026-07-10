# Lab Tk-2: Panel de control con grid y pestañas
# Incluye actividades 5, 6 y 7 resueltas
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random

root = tk.Tk()
root.title('Lab Tk-2 — Layout (con actividades)')
root.geometry('560x460')

# ── NOTEBOOK (pestañas) ───────────────────────────────────────
nb = ttk.Notebook(root)
nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ── PESTAÑA 1: formulario con grid ───────────────────────────
tab1 = tk.Frame(nb, bg='#f5f5f5')
nb.add(tab1, text=' 📋 Configuración ')

# LabelFrame agrupa widgets con un borde y título
grp_sensor = tk.LabelFrame(tab1, text='Parámetros del sensor',
    bg='#f5f5f5', fg='#1a3a5c', font=('Arial', 10, 'bold'), pady=8, padx=10)
grp_sensor.grid(row=0, column=0, padx=16, pady=12, sticky='ew')

# Widgets en grid — row, column, sticky='w' para alinear a la izquierda
campos = [
    ('Puerto serial:', 'COM3'),
    ('Período (ms):', '500'),
    ('Umbral T° (°C):', '35.0'),
]
vars_config = {}
for i, (lbl, default) in enumerate(campos):
    tk.Label(grp_sensor, text=lbl, bg='#f5f5f5',
        font=('Arial', 10), anchor='w').grid(
        row=i, column=0, sticky='w', pady=4)
    var = tk.StringVar(value=default)
    vars_config[lbl] = var
    tk.Entry(grp_sensor, textvariable=var, width=18,
        font=('Arial', 10)).grid(row=i, column=1, padx=8, pady=4)

# ---- Actividad 6: Combobox para baud rate ----
tk.Label(grp_sensor, text='Baud rate:', bg='#f5f5f5',
    font=('Arial', 10), anchor='w').grid(
    row=len(campos), column=0, sticky='w', pady=4)

var_baud = tk.StringVar(value='115200')
combo_baud = ttk.Combobox(grp_sensor, textvariable=var_baud,
    values=['9600', '19200', '38400', '57600', '115200'],
    state='readonly', width=16, font=('Arial', 10))
combo_baud.grid(row=len(campos), column=1, padx=8, pady=4)
vars_config['Baud rate:'] = var_baud

# Checkbutton
var_guardar = tk.BooleanVar(value=True)
tk.Checkbutton(tab1, text='Guardar log automáticamente',
    variable=var_guardar, bg='#f5f5f5', font=('Arial', 10)
    ).grid(row=1, column=0, sticky='w', padx=16, pady=4)

# Radiobuttons — protocolo
grp_proto = tk.LabelFrame(tab1, text='Protocolo', bg='#f5f5f5',
    font=('Arial', 10, 'bold'), padx=10, pady=6)
grp_proto.grid(row=2, column=0, padx=16, pady=6, sticky='ew')
var_proto = tk.StringVar(value='ASCII')
for proto in ['ASCII', 'Binario', 'Modbus RTU']:
    tk.Radiobutton(grp_proto, text=proto, variable=var_proto,
        value=proto, bg='#f5f5f5', font=('Arial', 10)
        ).pack(side=tk.LEFT, padx=12)

# Botón aplicar
def aplicar_config():
    resumen = '\n'.join(f'{k} {v.get()}' for k, v in vars_config.items())
    messagebox.showinfo('Configuración aplicada', resumen)

tk.Button(tab1, text='Aplicar configuración', command=aplicar_config,
    bg='#2E75B6', fg='white', font=('Arial', 11, 'bold'),
    relief=tk.FLAT, pady=6
    ).grid(row=3, column=0, padx=16, pady=12, sticky='ew')

# ── PESTAÑA 2: indicadores con place ─────────────────────────
tab2 = tk.Frame(nb, bg='#1e2736')
nb.add(tab2, text=' 📊 Monitor ')

# ---- Actividad 7: estilos de color para la Progressbar ----
style = ttk.Style()
style.theme_use('default')
style.configure('Verde.Horizontal.TProgressbar', background='#22c55e')
style.configure('Amarillo.Horizontal.TProgressbar', background='#eab308')
style.configure('Rojo.Horizontal.TProgressbar', background='#ef4444')

tk.Label(tab2, text='Temperatura', bg='#1e2736', fg='#94a3b8',
    font=('Arial', 9)).place(x=20, y=20)
pb_temp = ttk.Progressbar(tab2, length=300, maximum=100, mode='determinate',
    style='Verde.Horizontal.TProgressbar')
pb_temp.place(x=20, y=42)
lbl_temp_val = tk.Label(tab2, text='-- °C', bg='#1e2736',
    fg='#ef4444', font=('Courier New', 20, 'bold'))
lbl_temp_val.place(x=340, y=32)

tk.Label(tab2, text='Humedad', bg='#1e2736', fg='#94a3b8',
    font=('Arial', 9)).place(x=20, y=80)
pb_hum = ttk.Progressbar(tab2, length=300, maximum=100, mode='determinate')
pb_hum.place(x=20, y=102)
lbl_hum_val = tk.Label(tab2, text='-- %', bg='#1e2736',
    fg='#22c55e', font=('Courier New', 20, 'bold'))
lbl_hum_val.place(x=340, y=92)

# Label para alerta de temperatura (Actividad - Alerta de Umbral)
lbl_alerta = tk.Label(tab2, text='✅ Sistema OK', bg='#1e2736',
    fg='#22c55e', font=('Arial', 12, 'bold'))
lbl_alerta.place(x=20, y=142)

def color_para_temp(t):
    # Actividad 7: verde (<30), amarillo (30-40), rojo (>40)
    if t < 30:
        return 'Verde.Horizontal.TProgressbar'
    elif t < 40:
        return 'Amarillo.Horizontal.TProgressbar'
    else:
        return 'Rojo.Horizontal.TProgressbar'

# Simular actualización de valores
def simular():
    t = random.uniform(20, 45)
    h = random.uniform(30, 90)
    pb_temp['value'] = t
    pb_temp['style'] = color_para_temp(t)  # Actividad 7
    pb_hum['value'] = h
    lbl_temp_val.config(text=f'{t:.1f} °C')
    lbl_hum_val.config(text=f'{h:.1f} %')
    
    # Obtener umbral de temperatura de la configuración
    try:
        umbral = float(vars_config['Umbral T° (°C):'].get())
    except ValueError:
        umbral = 35.0
        
    if t > umbral:
        lbl_alerta.config(text=f'⚠️ ¡ALERTA: T° ALTA (> {umbral:.1f} °C)!', fg='#ef4444')
    else:
        lbl_alerta.config(text='✅ Sistema OK', fg='#22c55e')
        
    # Obtener el período de actualización de la configuración (con fallback a 800 ms)
    try:
        periodo = int(vars_config['Período (ms):'].get())
        if periodo <= 0:
            periodo = 800
    except ValueError:
        periodo = 800
        
    root.after(periodo, simular)  # repetir según configuración

simular()

# ── PESTAÑA 3: Ayuda (Actividad 5) ────────────────────────────
tab3 = tk.Frame(nb, bg='#f5f5f5')
nb.add(tab3, text=' ❓ Ayuda ')

tk.Label(tab3, text='Instrucciones de uso', bg='#f5f5f5',
    fg='#1a3a5c', font=('Arial', 12, 'bold')).pack(anchor='w', padx=16, pady=(14, 6))

texto_ayuda = scrolledtext.ScrolledText(tab3, wrap=tk.WORD, font=('Arial', 10),
    bg='white', fg='#333333', relief=tk.FLAT, padx=10, pady=10)
texto_ayuda.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

instrucciones = """BIENVENIDO AL PANEL DE CONTROL DEL SENSOR

1. Pestaña Configuración
   - Ingrese el puerto serial donde está conectado el dispositivo (ej: COM3).
   - Defina el período de muestreo en milisegundos.
   - Establezca el umbral de temperatura que dispara una alerta.
   - Seleccione el baud rate de comunicación desde la lista desplegable.
   - Marque la casilla si desea guardar un log automático de las lecturas.
   - Elija el protocolo de comunicación (ASCII, Binario o Modbus RTU).
   - Presione "Aplicar configuración" para confirmar los cambios.

2. Pestaña Monitor
   - Muestra en tiempo real la temperatura y humedad simuladas.
   - La barra de temperatura cambia de color según el valor:
       • Verde:   temperatura menor a 30 °C
       • Amarillo: temperatura entre 30 °C y 40 °C
       • Rojo:    temperatura mayor a 40 °C

3. Recomendaciones
   - Verifique que el puerto serial seleccionado corresponda al dispositivo
     físico conectado antes de aplicar la configuración.
   - Si la temperatura se mantiene en rojo por mucho tiempo, revise el
     sensor o el ambiente donde está instalado.

Para más ayuda, contacte al administrador del sistema.
"""
texto_ayuda.insert(tk.END, instrucciones)
texto_ayuda.config(state=tk.DISABLED)  # solo lectura

root.mainloop()