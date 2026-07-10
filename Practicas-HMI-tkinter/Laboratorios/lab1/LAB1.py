"""
Lab Tk-1 — Ventana de Bienvenida (versión propia)
Programación de Interfaces y Puertos

Objetivo: ventana principal + widgets esenciales (Label, Entry, Button,
messagebox) usando una estructura orientada a objetos.

Incluye las 4 actividades del manual ya resueltas:
  1) Botón que muestra el nombre en mayúsculas
  2) Contador de veces que se presionó "Saludar"
  3) askretrycancel en vez de showwarning para campo vacío
  4) Color rojo en el resultado si el nombre tiene menos de 3 caracteres
"""

import tkinter as tk
from tkinter import messagebox


class VentanaBienvenida:
    # Paleta propia (tonos verdes/grises, distinta a la del manual)
    COLOR_FONDO = "#0d1b2a"
    COLOR_PANEL = "#1b263b"
    COLOR_ACENTO = "#2a9d8f"
    COLOR_TEXTO = "#e0e1dd"
    COLOR_ALERTA = "#e76f51"
    COLOR_OK = "#2a9d8f"

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Registro de Visitante — Lab Tk-1")
        self.ventana.geometry("440x320")
        self.ventana.configure(bg=self.COLOR_FONDO)
        self.ventana.resizable(False, False)

        # Variables de control
        self.txt_nombre = tk.StringVar()
        self.txt_resultado = tk.StringVar(value="Escribe tu nombre y presiona Saludar")
        self.contador_saludos = 0

        self._crear_widgets()
        self._configurar_atajos()

    # ------------------------------------------------------------------
    def _crear_widgets(self):
        tk.Label(
            self.ventana, text="Registro de Visitante",
            font=("Segoe UI", 15, "bold"),
            bg=self.COLOR_FONDO, fg=self.COLOR_ACENTO,
        ).pack(pady=(22, 4))

        tk.Label(
            self.ventana, text="Nombre completo:",
            font=("Segoe UI", 10), bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO,
        ).pack()

        self.entry_nombre = tk.Entry(
            self.ventana, textvariable=self.txt_nombre,
            font=("Segoe UI", 12), width=26, justify="center",
            bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO,
            insertbackground=self.COLOR_TEXTO, relief=tk.FLAT,
        )
        self.entry_nombre.pack(pady=10, ipady=5)
        self.entry_nombre.focus()

        panel_botones = tk.Frame(self.ventana, bg=self.COLOR_FONDO)
        panel_botones.pack(pady=6)

        self._boton(panel_botones, "Saludar", self.accion_saludar, self.COLOR_ACENTO).grid(row=0, column=0, padx=4)
        self._boton(panel_botones, "MAYÚSCULAS", self.accion_mayusculas, "#457b9d").grid(row=0, column=1, padx=4)
        self._boton(panel_botones, "Limpiar", self.accion_limpiar, "#495057").grid(row=0, column=2, padx=4)
        self._boton(panel_botones, "Salir", self.accion_salir, self.COLOR_ALERTA).grid(row=0, column=3, padx=4)

        self.lbl_resultado = tk.Label(
            self.ventana, textvariable=self.txt_resultado,
            font=("Segoe UI", 11, "italic"), bg=self.COLOR_FONDO, fg=self.COLOR_OK,
            wraplength=380, justify="center",
        )
        self.lbl_resultado.pack(pady=14)

        # Actividad 2: contador de saludos
        self.lbl_contador = tk.Label(
            self.ventana, text="Saludos enviados: 0",
            font=("Segoe UI", 9), bg=self.COLOR_FONDO, fg="#778da9",
        )
        self.lbl_contador.pack(pady=(0, 10))

    def _boton(self, parent, texto, comando, color):
        return tk.Button(
            parent, text=texto, command=comando,
            bg=color, fg="white", font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT, padx=10, pady=6, cursor="hand2",
            activebackground=color, activeforeground="white",
        )

    def _configurar_atajos(self):
        self.ventana.bind("<Return>", lambda e: self.accion_saludar())
        self.ventana.bind("<Escape>", lambda e: self.accion_salir())

    # ------------------------------------------------------------------
    # Callbacks
    def accion_saludar(self):
        nombre = self.txt_nombre.get().strip()

        # Actividad 3: askretrycancel en vez de showwarning
        if not nombre:
            reintentar = messagebox.askretrycancel(
                "Falta el nombre",
                "No escribiste ningún nombre.\n¿Quieres intentarlo de nuevo?",
            )
            if reintentar:
                self.entry_nombre.focus()
            return

        self.contador_saludos += 1
        self.lbl_contador.config(text=f"Saludos enviados: {self.contador_saludos}")

        self.txt_resultado.set(f"¡Hola, {nombre}! Bienvenido al laboratorio.")

        # Actividad 4: rojo si el nombre tiene menos de 3 caracteres
        if len(nombre) < 3:
            self.lbl_resultado.config(fg=self.COLOR_ALERTA)
        else:
            self.lbl_resultado.config(fg=self.COLOR_OK)

    def accion_mayusculas(self):
        nombre = self.txt_nombre.get().strip()
        if not nombre:
            messagebox.showinfo("Sin datos", "Escribe un nombre primero.")
            return
        self.txt_resultado.set(nombre.upper())
        self.lbl_resultado.config(fg=self.COLOR_ACENTO)

    def accion_limpiar(self):
        self.txt_nombre.set("")
        self.txt_resultado.set("Escribe tu nombre y presiona Saludar")
        self.lbl_resultado.config(fg=self.COLOR_OK)
        self.entry_nombre.focus()

    def accion_salir(self):
        if messagebox.askyesno("Confirmar salida", "¿Seguro que deseas cerrar la ventana?"):
            self.ventana.destroy()

    # ------------------------------------------------------------------
    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    VentanaBienvenida().ejecutar()
