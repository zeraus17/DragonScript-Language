import time
import tkinter as tk
from tkinter import ttk


class TableroGUI:

  def __init__(self, ancho=3, alto=3, cell_size=90):
    self.ancho = ancho
    self.alto = alto
    self.cell_size = cell_size

    # Estados de control de reproducción
    self.is_playing = False
    self.delay = 0.3
    self.reset_requested = False

    self.root = tk.Tk()
    self.root.title("🐉 DragonScript - Tablero Educativo")

    # Canvas para la grilla
    canvas_width = self.ancho * self.cell_size
    canvas_height = self.alto * self.cell_size
    self.canvas = tk.Canvas(
        self.root, width=canvas_width, height=canvas_height, bg="#1e1e2e"
    )
    self.canvas.pack(padx=15, pady=10)

    # Panel Inferior de Controles
    control_frame = ttk.Frame(self.root)
    control_frame.pack(fill="x", padx=15, pady=10)

    self.btn_play = ttk.Button(
        control_frame, text="▶ Play", command=self.toggle_play
    )
    self.btn_play.pack(side="left", padx=5)

    self.btn_reset = ttk.Button(
        control_frame, text="↺ Reset", command=self.reset
    )
    self.btn_reset.pack(side="left", padx=5)

    ttk.Label(control_frame, text="Velocidad:").pack(side="left", padx=(15, 5))
    self.speed_slider = ttk.Scale(
        control_frame,
        from_=0.05,
        to=1.0,
        value=0.3,
        command=self._update_speed,
    )
    self.speed_slider.pack(side="left", fill="x", expand=True, padx=5)

  def toggle_play(self):
    self.is_playing = not self.is_playing
    self.btn_play.config(text="⏸ Pausa" if self.is_playing else "▶ Play")

  def reset(self):
    self.reset_requested = True
    self.is_playing = False
    self.btn_play.config(text="▶ Play")

  def _update_speed(self, val):
    # Deslizar a la derecha disminuye el delay (más rápido)
    self.delay = 1.05 - float(val)

  def _esperar_paso(self):
    """Pausa la ejecución mientras esté en Pausa o aguarda el delay en Play."""
    while not self.is_playing and not self.reset_requested:
      self.root.update()
      time.sleep(0.05)

    if self.reset_requested:
      return

    self.root.update()
    time.sleep(self.delay)

  def renderizar(self, guerrero_pos, celdas):
        self.canvas.delete("all")

        # Símbolos de estrellas para cada Esfera del Dragón
        ESTRELLAS_TXT = {1: "★", 2: "2★", 3: "3★", 4: "4★"}

        # Posiciones relativas fijas dentro de la celda (x_offset, y_offset)
        OFFSETS = {
            1: (0.30, 0.70),  # Superior Izquierda (1 estrella)
            2: (0.30, 0.30),  # Superior Derecha (2 estrellas)
            3: (0.70, 0.30),  # Inferior Izquierda (3 estrellas)
            4: (0.70, 0.70),  # Inferior Derecha (4 estrellas)
        }

        for x in range(self.ancho):
            for y in range(self.alto):
                canvas_x1 = x * self.cell_size
                canvas_y1 = (self.alto - 1 - y) * self.cell_size
                canvas_x2 = canvas_x1 + self.cell_size
                canvas_y2 = canvas_y1 + self.cell_size

                # Grilla
                self.canvas.create_rectangle(
                    canvas_x1,
                    canvas_y1,
                    canvas_x2,
                    canvas_y2,
                    outline="#45475a",
                    width=2,
                    fill="#313244",
                )

                # Coordenadas
                self.canvas.create_text(
                    canvas_x1 + 15,
                    canvas_y2 - 10,
                    text=f"({x},{y})",
                    fill="#6c7086",
                    font=("Consolas", 7),
                )

                # Esferas del Dragón (Sub-grilla 2x2)
                esferas = celdas.get((x, y), {})
                if isinstance(esferas, dict):
                    radio = self.cell_size * 0.16

                    for esfera_id in range(1, 5):
                        cant = esferas.get(esfera_id, 0)
                        if cant > 0:
                            ox, oy = OFFSETS[esfera_id]

                            # Coordenadas del centro de cada cuadrante
                            cx = canvas_x1 + (self.cell_size * ox)
                            cy = canvas_y1 + (self.cell_size * oy)

                            # Dibujar Esfera Naranja estilo Dragon Ball
                            self.canvas.create_oval(
                                cx - radio,
                                cy - radio,
                                cx + radio,
                                cy + radio,
                                fill="#fab387",  # Naranja Esfera
                                outline="#fe640b",  # Borde Naranja Oscuro
                                width=1.5,
                            )

                            # Texto: Muestra la cantidad y las estrellas correspondientes (ej: "1★ x2" o "1★")
                            texto_esfera = (
                                f"{ESTRELLAS_TXT[esfera_id]}"
                                if cant == 1
                                else f"{cant}x{ESTRELLAS_TXT[esfera_id]}"
                            )
                            self.canvas.create_text(
                                cx,
                                cy,
                                text=texto_esfera,
                                fill="#d20f39",  # Rojo Dragón
                                font=("Arial", 7, "bold"),
                            )

                # GOKU (pixel art simplificado)
                if (x, y) == guerrero_pos:
                    self.canvas.create_rectangle(
                        canvas_x1 + 3,
                        canvas_y1 + 3,
                        canvas_x2 - 3,
                        canvas_y2 - 3,
                        outline="#a6e3a1",
                        width=2,
                    )
                    # Mini sprite 7x9 centrado
                    cols, rows = 7, 9
                    pw = (self.cell_size - 16) / cols
                    ph = (self.cell_size - 20) / rows
                    ox = canvas_x1 + (self.cell_size - cols * pw) / 2
                    oy = canvas_y1 + 14
                    # mapa: 0 vacío, h pelo, s piel, e ojo, g gi naranja, b azul, r cinturón, o bota
                    sprite = [
                        "0hh0hh0",
                        "hhhhhhh",
                        "0hsssh0",
                        "0seses0",
                        "0sssss0",
                        "0ggggg0",
                        "0gbrbg0",
                        "0b0b0b0",
                        "0o0o0o0",
                    ]
                    colors = {
                        "h": "#1a1a2e",
                        "s": "#f0c27a",
                        "e": "#111111",
                        "g": "#f5a623",
                        "b": "#1e88e5",
                        "r": "#c62828",
                        "o": "#5d4037",
                    }
                    for ry, row in enumerate(sprite):
                        for cx2, ch in enumerate(row):
                            if ch == "0":
                                continue
                            self.canvas.create_rectangle(
                                ox + cx2 * pw,
                                oy + ry * ph,
                                ox + (cx2 + 1) * pw,
                                oy + (ry + 1) * ph,
                                fill=colors[ch],
                                outline=colors[ch],
                            )
                    self.canvas.create_text(
                        (canvas_x1 + canvas_x2) / 2,
                        canvas_y1 + 9,
                        text="GOKU",
                        fill="#a6e3a1",
                        font=("Arial", 7, "bold"),
                    )

        self._esperar_paso()

  def mantener_abierto(self):
    self.root.mainloop()