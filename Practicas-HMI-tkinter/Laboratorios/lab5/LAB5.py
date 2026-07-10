"""
Lab Tk-5 — Menús, diálogos y eventos de teclado
Programación de Interfaces y Puertos

Elementos que cubre este laboratorio (ver rúbrica):
  - Menú de barra completo: Archivo, Ver, Herramientas, Ayuda
  - filedialog para abrir/guardar archivos
  - Ventana secundaria (Toplevel) con una calculadora CRC-16
  - Atajos de teclado (Ctrl+N/O/S/E/Q, F5)
  - colorchooser para cambiar el tema
"""
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox, scrolledtext
import json
import os
from datetime import datetime


class AppHMI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('HMI — Interfaces y Puertos (Lab Tk-5)')
        self.root.geometry('700x450')
        self.archivo_config = None
        self._construir()
        self._atajos()

    # ══════════════════════════════════════════════════════════
    # Construcción de la interfaz
    # ══════════════════════════════════════════════════════════
    def _construir(self):
        # ── Barra de menú ────────────────────────────────────
        menubar = tk.Menu(self.root)

        # Menú Archivo
        m_archivo = tk.Menu(menubar, tearoff=0)
        m_archivo.add_command(label='Nueva sesión', command=self.nueva_sesion,
                               accelerator='Ctrl+N')
        m_archivo.add_command(label='Abrir config…', command=self.abrir_config,
                               accelerator='Ctrl+O')
        m_archivo.add_command(label='Guardar config…', command=self.guardar_config,
                               accelerator='Ctrl+S')
        m_archivo.add_separator()
        m_archivo.add_command(label='Exportar CSV…', command=self.exportar_csv,
                               accelerator='Ctrl+E')
        m_archivo.add_separator()
        m_archivo.add_command(label='Salir', command=self.salir, accelerator='Ctrl+Q')
        menubar.add_cascade(label='Archivo', menu=m_archivo)

        # Menú Ver
        m_ver = tk.Menu(menubar, tearoff=0)
        self.var_log = tk.BooleanVar(value=True)
        m_ver.add_checkbutton(label='Mostrar log', variable=self.var_log,
                               command=self.toggle_log)
        m_ver.add_command(label='Tema…', command=self.cambiar_tema)
        menubar.add_cascade(label='Ver', menu=m_ver)

        # Menú Herramientas
        m_tools = tk.Menu(menubar, tearoff=0)
        m_tools.add_command(label='Calculadora CRC-16…', command=self.abrir_crc)
        m_tools.add_command(label='Convertidor de escala…', command=self.abrir_conversor)
        menubar.add_cascade(label='Herramientas', menu=m_tools)

        # Menú Ayuda
        m_ayuda = tk.Menu(menubar, tearoff=0)
        m_ayuda.add_command(label='Documentación', command=self.abrir_docs)
        m_ayuda.add_command(label='Acerca de…', command=self.acerca_de)
        menubar.add_cascade(label='Ayuda', menu=m_ayuda)

        self.root.config(menu=menubar)

        # ── Área principal ───────────────────────────────────
        self.frame_main = tk.Frame(self.root, bg='#f0f4f8')
        self.frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(self.frame_main, text='Área de trabajo del HMI',
                 bg='#f0f4f8', font=('Arial', 12)).pack(expand=True)

        # ── Log inferior ─────────────────────────────────────
        self.frame_log = tk.Frame(self.root)
        self.frame_log.pack(fill=tk.X, side=tk.BOTTOM)
        self.log = scrolledtext.ScrolledText(self.frame_log, height=5,
                                              bg='#0f172a', fg='#64748b',
                                              font=('Courier New', 8))
        self.log.pack(fill=tk.X)
        self._log('Sistema iniciado')

    def _log(self, msg):
        ts = datetime.now().strftime('%H:%M:%S')
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, f'[{ts}] {msg}\n')
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    # ══════════════════════════════════════════════════════════
    # Atajos de teclado
    # ══════════════════════════════════════════════════════════
    def _atajos(self):
        self.root.bind('<Control-n>', lambda e: self.nueva_sesion())
        self.root.bind('<Control-o>', lambda e: self.abrir_config())
        self.root.bind('<Control-s>', lambda e: self.guardar_config())
        self.root.bind('<Control-e>', lambda e: self.exportar_csv())
        self.root.bind('<Control-q>', lambda e: self.salir())
        self.root.bind('<F5>', lambda e: self._log('F5: Reiniciando...'))

    # ══════════════════════════════════════════════════════════
    # Comandos de Archivo
    # ══════════════════════════════════════════════════════════
    def nueva_sesion(self):
        if messagebox.askyesno('Nueva sesión', '¿Descartar la sesión actual?'):
            self._log('Nueva sesión iniciada')

    def abrir_config(self):
        ruta = filedialog.askopenfilename(
            title='Abrir configuración',
            filetypes=[('JSON config', '*.json'), ('Todos', '*.*')])
        if ruta:
            self.archivo_config = ruta
            with open(ruta) as f:
                cfg = json.load(f)
            self._log(f'Config cargada: {os.path.basename(ruta)}')
            self._log(str(cfg))

    def guardar_config(self):
        ruta = filedialog.asksaveasfilename(
            title='Guardar configuración',
            defaultextension='.json',
            filetypes=[('JSON config', '*.json')])
        if ruta:
            cfg = {'puerto': 'COM3', 'baud': 115200, 'umbral': 35.0}
            with open(ruta, 'w') as f:
                json.dump(cfg, f, indent=2)
            self._log(f'Config guardada: {os.path.basename(ruta)}')

    def exportar_csv(self):
        ruta = filedialog.asksaveasfilename(
            title='Exportar datos',
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv')])
        if ruta:
            with open(ruta, 'w') as f:
                f.write('timestamp,temp,pres,hum\n')
                f.write('2026-01-01 00:00:00,23.4,1013.2,55.1\n')
            self._log(f'CSV exportado: {os.path.basename(ruta)}')

    # ══════════════════════════════════════════════════════════
    # Comandos de Ver
    # ══════════════════════════════════════════════════════════
    def toggle_log(self):
        if self.var_log.get():
            self.frame_log.pack(fill=tk.X, side=tk.BOTTOM)
        else:
            self.frame_log.pack_forget()

    def cambiar_tema(self):
        color = colorchooser.askcolor(title='Color de fondo del área de trabajo')
        if color[1]:
            self.frame_main.configure(bg=color[1])
            self._log(f'Tema cambiado a {color[1]}')

    # ══════════════════════════════════════════════════════════
    # Ventanas secundarias (Toplevel)
    # ══════════════════════════════════════════════════════════
    def abrir_crc(self):
        win = tk.Toplevel(self.root)
        win.title('Calculadora CRC-16 Modbus')
        win.geometry('400x200')
        win.resizable(False, False)

        tk.Label(win, text='Datos (hex, separados por espacio):',
                 font=('Arial', 10)).pack(pady=(16, 4))
        var = tk.StringVar(value='01 03 00 64 00 02')
        tk.Entry(win, textvariable=var, width=36, font=('Courier New', 11)).pack()

        lbl_res = tk.Label(win, text='CRC: --', font=('Courier New', 14, 'bold'),
                            fg='#2E75B6')
        lbl_res.pack(pady=10)

        def calcular():
            try:
                bs = bytes(int(x, 16) for x in var.get().split())
                crc = 0xFFFF
                for b in bs:
                    crc ^= b
                    for _ in range(8):
                        crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
                lbl_res.config(text=f'CRC: {crc:04X}h ({crc & 0xFF:02X}h {crc >> 8:02X}h)')
            except Exception:
                lbl_res.config(text='Error en los datos')

        tk.Button(win, text='Calcular', command=calcular,
                  bg='#2E75B6', fg='white', font=('Arial', 10), relief=tk.FLAT
                  ).pack(pady=4)

    def abrir_conversor(self):
        win = tk.Toplevel(self.root)
        win.title('Conversor de escala lineal')
        win.geometry('380x220')

        campos = [('Valor ADC:', '0'), ('ADC mín:', '0'), ('ADC máx:', '1023'),
                  ('Escala mín:', '0.0'), ('Escala máx:', '100.0')]
        vars_ = []
        for i, (lbl, val) in enumerate(campos):
            tk.Label(win, text=lbl, width=12, anchor='e').grid(row=i, column=0, pady=3, padx=8)
            v = tk.StringVar(value=val)
            tk.Entry(win, textvariable=v, width=12).grid(row=i, column=1, pady=3)
            vars_.append(v)

        lbl_res = tk.Label(win, text='Resultado: --', font=('Arial', 11, 'bold'))
        lbl_res.grid(row=5, column=0, columnspan=2, pady=8)

        def convertir():
            try:
                x, x0, x1, y0, y1 = [float(v.get()) for v in vars_]
                y = y0 + (x - x0) / (x1 - x0) * (y1 - y0)
                lbl_res.config(text=f'Resultado: {y:.4f}')
            except Exception:
                lbl_res.config(text='Error en valores')

        tk.Button(win, text='Convertir', command=convertir,
                  bg='#1E5E2E', fg='white', relief=tk.FLAT
                  ).grid(row=6, column=0, columnspan=2, pady=4)

    # ══════════════════════════════════════════════════════════
    # Ayuda / salida
    # ══════════════════════════════════════════════════════════
    def abrir_docs(self):
        import webbrowser
        webbrowser.open('https://tkdocs.com')

    def acerca_de(self):
        messagebox.showinfo('Acerca de',
                             'HMI Monitor v1.0\nProgramación de Interfaces y Puertos\n\n'
                             'Desarrollado con Python 3 + Tkinter')

    def salir(self):
        if messagebox.askyesno('Salir', '¿Cerrar la aplicación?'):
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    AppHMI().run()