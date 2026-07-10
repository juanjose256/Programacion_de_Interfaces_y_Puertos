# Lab Tk-7: Tkinter + threading + pyserial
# El MCU debe enviar líneas CSV: 'N,temp,pres,hum,alt\n'

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import serial
import serial.tools.list_ports
import threading
import queue
import time

from datetime import datetime
from collections import deque


# ═══════════════════════════════════════════════════════════════
# HILO DE LECTURA SERIAL
# ═══════════════════════════════════════════════════════════════

class HiloSerial(threading.Thread):
    """Corre en hilo separado — NUNCA toca la UI directamente."""

    def __init__(self, q_datos: queue.Queue, q_log: queue.Queue):
        super().__init__(daemon=True)

        # daemon=True: muere con la app
        self.q_datos = q_datos
        self.q_log = q_log
        self.ser = None
        self.activo = threading.Event()  # flag thread-safe

    def conectar(self, puerto: str, baud: int) -> bool:
        try:
            self.ser = serial.Serial(puerto, baud, timeout=2)
            time.sleep(2)  # esperar reset del Arduino

            self.activo.set()  # señal para que run() empiece a leer
            self.q_log.put(("INFO", f"Conectado a {puerto} @ {baud}"))
            return True

        except serial.SerialException as e:
            self.q_log.put(("ERROR", str(e)))
            return False

    def desconectar(self):
        self.activo.clear()

        if self.ser and self.ser.is_open:
            self.ser.close()

        self.q_log.put(("INFO", "Desconectado"))

    def enviar(self, cmd: str):
        if self.ser and self.ser.is_open and self.activo.is_set():
            self.ser.write((cmd.strip() + "\n").encode())

    def run(self):
        fallos = 0

        while True:
            self.activo.wait()  # esperar hasta que se conecte

            if not self.ser or not self.ser.is_open:
                time.sleep(0.1)
                continue

            try:
                raw = self.ser.readline().decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                if not raw or raw.startswith("#"):
                    continue

                partes = raw.split(",")

                if len(partes) >= 4:
                    dato = {
                        "n": int(partes[0]),
                        "temp": float(partes[1]),
                        "pres": float(partes[2]),
                        "hum": float(partes[3]),
                        "alt": float(partes[4]) if len(partes) > 4 else 0.0,
                        "ts": datetime.now().isoformat(timespec="seconds")
                    }

                    self.q_datos.put(dato)  # → cola thread-safe
                    fallos = 0

            except (serial.SerialException, TypeError, OSError) as e:
                if self.activo.is_set():
                    fallos += 1
                    self.q_log.put(("ERROR", f"Serial: {e}"))

                    if fallos >= 5:
                        self.desconectar()
                else:
                    # Ignorar errores esperados al desconectar intencionalmente
                    pass

            except ValueError:
                pass  # ignorar líneas mal formadas


# ═══════════════════════════════════════════════════════════════
# APLICACIÓN UI
# ═══════════════════════════════════════════════════════════════

class App:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lab Tk-7 — Serial + Threading")
        self.root.geometry("720x480")
        self.root.configure(bg="#1e2736")
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

        # Colas thread-safe
        self.q_datos = queue.Queue(maxsize=500)
        self.q_log = queue.Queue()

        # Hilo serial
        self.hilo = HiloSerial(self.q_datos, self.q_log)
        self.hilo.start()

        self._ui()
        self._poll()

    def _ui(self):

        # ── Barra de conexión ───────────────────────────────────

        bar = tk.Frame(self.root, bg="#111827", height=48)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)

        puertos = [p.device for p in serial.tools.list_ports.comports()]

        self.var_pto = tk.StringVar(value=puertos[0] if puertos else "")
        self.var_baud = tk.StringVar(value="115200")

        tk.Label(
            bar,
            text="Puerto:",
            bg="#111827",
            fg="#94a3b8",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(12, 2), pady=12)

        ttk.Combobox(
            bar,
            textvariable=self.var_pto,
            values=puertos,
            width=12
        ).pack(side=tk.LEFT, padx=2, pady=10)

        tk.Label(
            bar,
            text="Baud:",
            bg="#111827",
            fg="#94a3b8",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(8, 2))

        ttk.Combobox(
            bar,
            textvariable=self.var_baud,
            values=["9600", "19200", "57600", "115200"],
            width=8
        ).pack(side=tk.LEFT, padx=2)

        self.btn_cx = tk.Button(
            bar,
            text="Conectar",
            command=self._conectar,
            bg="#1E5E2E",
            fg="white",
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            padx=12
        )

        self.btn_cx.pack(side=tk.LEFT, padx=10)

        self.lbl_cx = tk.Label(
            bar,
            text="● Desconectado",
            bg="#111827",
            fg="#ef4444",
            font=("Arial", 9, "bold")
        )

        self.lbl_cx.pack(side=tk.LEFT, padx=6)

        # ── Panel de indicadores ────────────────────────────────

        pan = tk.Frame(self.root, bg="#0f172a")
        pan.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        self.lbls = {}

        defs = [
            ("temp", "Temperatura", "°C", "#ef4444"),
            ("pres", "Presión", "hPa", "#3b82f6"),
            ("hum", "Humedad", "%", "#22c55e"),
            ("alt", "Altitud", "m", "#a855f7"),
        ]

        for i, (key, nombre, uni, color) in enumerate(defs):

            f = tk.Frame(pan, bg="#1e2736")
            f.grid(row=0, column=i, padx=8, pady=12, sticky="nsew")

            pan.columnconfigure(i, weight=1)

            tk.Label(
                f,
                text=nombre,
                bg="#1e2736",
                fg="#94a3b8",
                font=("Arial", 9)
            ).pack(anchor="w", padx=10, pady=(8, 0))

            lbl = tk.Label(
                f,
                text=f"-- {uni}",
                bg="#1e2736",
                fg=color,
                font=("Courier New", 20, "bold")
            )

            lbl.pack(anchor="w", padx=10, pady=(0, 8))

            self.lbls[key] = (lbl, uni, color)

        # ── Área de comandos ────────────────────────────────────

        cmd_f = tk.Frame(self.root, bg="#111827")
        cmd_f.pack(fill=tk.X, padx=8, pady=2)

        comandos = [
            ("LED Verde ON", "SET:LED:0:1"),
            ("LED Verde OFF", "SET:LED:0:0"),
            ("LED Rojo ON", "SET:LED:1:1"),
            ("LED Rojo OFF", "SET:LED:1:0"),
            ("LED Azul ON", "SET:LED:2:1"),
            ("LED Azul OFF", "SET:LED:2:0"),
            ("PING", "PING"),
        ]

        for txt, cmd in comandos:
            tk.Button(
                cmd_f,
                text=txt,
                command=lambda c=cmd: self.hilo.enviar(c),
                bg="#1F4E79",
                fg="white",
                font=("Arial", 8),
                relief=tk.FLAT,
                padx=8,
                pady=4
            ).pack(side=tk.LEFT, padx=4, pady=6)

        # ── Log ─────────────────────────────────────────────────

        self.log = scrolledtext.ScrolledText(
            self.root,
            height=6,
            bg="#0d1520",
            fg="#64748b",
            font=("Courier New", 8),
            relief=tk.FLAT,
            state=tk.DISABLED
        )

        self.log.pack(fill=tk.X, padx=8, pady=(0, 6))

        self.log.tag_config("INFO", foreground="#22c55e")
        self.log.tag_config("ERROR", foreground="#ef4444")

    def _log(self, nivel, msg):
        ts = datetime.now().strftime("%H:%M:%S")

        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, f"[{ts}] {msg}\n", nivel)
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def _conectar(self):
        if self.hilo.activo.is_set():
            self.hilo.desconectar()
            self.btn_cx.config(text="Conectar", bg="#1E5E2E")
        else:
            if self.hilo.conectar(
                self.var_pto.get(),
                int(self.var_baud.get())
            ):
                self.btn_cx.config(
                    text="Desconectar",
                    bg="#922B21"
                )

    # ── POLL ───────────────────────────────────────────────────

    def _poll(self):

        while not self.q_log.empty():
            nivel, msg = self.q_log.get_nowait()

            self._log(nivel, msg)

            if nivel == "INFO" and "Conectado" in msg:
                self.lbl_cx.config(
                    text="● Conectado",
                    fg="#22c55e"
                )

            elif nivel == "INFO" and "Desconectado" in msg:
                self.lbl_cx.config(
                    text="● Desconectado",
                    fg="#ef4444"
                )

                self.btn_cx.config(
                    text="Conectar",
                    bg="#1E5E2E"
                )

        while not self.q_datos.empty():
            d = self.q_datos.get_nowait()

            for key, (lbl, uni, _) in self.lbls.items():
                lbl.config(text=f"{d[key]:.2f} {uni}")

        self.root.after(100, self._poll)

    def cerrar(self):
        self.hilo.desconectar()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()