"""
board.py
========
Tablero estilo *Gobstones* para DragonScript, con temática Dragon Ball.

Idea pedagógica
---------------
Igual que en Gobstones, hay un **tablero** rectangular de celdas y un
**cabezal** que se para sobre una celda y se mueve por ella. En DragonScript
el cabezal es el **GUERRERO** (que *vuela* por el tablero) y, en vez de
"bolitas de colores", las celdas guardan **Esferas del Dragón** de 4 tipos,
identificadas por su número de estrellas:

    ESFERA_1  ->  ★         (1 estrella)
    ESFERA_2  ->  ★★        (2 estrellas)
    ESFERA_3  ->  ★★★       (3 estrellas)
    ESFERA_4  ->  ★★★★      (4 estrellas)

El origen ``(0, 0)`` está en la esquina **inferior izquierda** (como en
Gobstones). VOLAR NORTE sube (aumenta ``y``), VOLAR ESTE va a la derecha
(aumenta ``x``).

Este módulo NO conoce nada de DragonScript: sólo modela el tablero. El puente
hacia el lenguaje (funciones VOLAR, CARGAR, etc.) se arma en ``runtime.py``.
"""

from __future__ import annotations

from .errors import RuntimeError_, TypeErrorDS

# --- Direcciones ---------------------------------------------------------
NORTE = "NORTE"
SUR = "SUR"
ESTE = "ESTE"
OESTE = "OESTE"
DIRECCIONES = (NORTE, SUR, ESTE, OESTE)

# --- Esferas (los 4 "colores") ------------------------------------------
# Clave interna 1..4 ; nombre expuesto "ESFERA_n".
ESFERAS = (1, 2, 3, 4)
NOMBRE_ESFERA = {
    1: "ESFERA_1",
    2: "ESFERA_2",
    3: "ESFERA_3",
    4: "ESFERA_4",
}
ESTRELLAS = {1: "★", 2: "★★", 3: "★★★", 4: "★★★★"}

# Símbolos cortos para el render compacto de cada celda.
SIMBOLO = {1: "1", 2: "2", 3: "3", 4: "4"}


def esfera_desde_valor(valor):
    """Traduce un valor DragonScript (``"ESFERA_1"`` o ``1``) a la clave 1..4."""
    if isinstance(valor, bool):
        raise TypeErrorDS("Eso no es una Esfera del Dragón válida.")
    if isinstance(valor, (int, float)) and int(valor) in ESFERAS:
        return int(valor)
    if isinstance(valor, str):
        v = valor.strip().upper()
        for clave, nombre in NOMBRE_ESFERA.items():
            if v == nombre or v == str(clave):
                return clave
    raise TypeErrorDS(
        "Esa no es una Esfera del Dragón válida. Usá ESFERA_1..ESFERA_4.")


class Board:
    """Un tablero rectangular con un cabezal (el GUERRERO)."""

    def __init__(self, ancho: int = 4, alto: int = 4):
        self.reiniciar(ancho, alto)

    # ------------------------------------------------------------------
    def reiniciar(self, ancho: int = 4, alto: int = 4) -> None:
        if (isinstance(ancho, bool) or isinstance(alto, bool)
                or not isinstance(ancho, int) or not isinstance(alto, int)):
            raise TypeErrorDS("El tamaño del tablero debe ser en números enteros.")
        if ancho < 1 or alto < 1:
            raise RuntimeError_("El tablero debe tener al menos 1x1 celdas.")
        self.ancho = ancho
        self.alto = alto
        # celdas[(x, y)] -> dict {esfera: cantidad}
        self.celdas: dict[tuple[int, int], dict[int, int]] = {
            (x, y): {1: 0, 2: 0, 3: 0, 4: 0}
            for x in range(ancho) for y in range(alto)
        }
        self.x = 0
        self.y = 0

    # ------------------------------------------------------ movimiento
    def _delta(self, direccion: str):
        d = str(direccion).strip().upper()
        if d == NORTE:
            return (0, 1)
        if d == SUR:
            return (0, -1)
        if d == ESTE:
            return (1, 0)
        if d == OESTE:
            return (-1, 0)
        raise TypeErrorDS(
            f"'{direccion}' no es una dirección. Usá NORTE, SUR, ESTE u OESTE.")

    def puede_volar(self, direccion: str) -> bool:
        dx, dy = self._delta(direccion)
        nx, ny = self.x + dx, self.y + dy
        return 0 <= nx < self.ancho and 0 <= ny < self.alto

    def volar(self, direccion: str) -> None:
        if not self.puede_volar(direccion):
            raise RuntimeError_(
                f"El GUERRERO se estrelló contra el borde: no puede VOLAR {direccion}.")
        dx, dy = self._delta(direccion)
        self.x += dx
        self.y += dy

    # -------------------------------------------------------- esferas
    def _celda(self):
        return self.celdas[(self.x, self.y)]

    def cargar(self, esfera) -> None:
        clave = esfera_desde_valor(esfera)
        self._celda()[clave] += 1

    def drenar(self, esfera) -> None:
        clave = esfera_desde_valor(esfera)
        if self._celda()[clave] <= 0:
            raise RuntimeError_(
                f"No hay {NOMBRE_ESFERA[clave]} en esta celda para DRENAR.")
        self._celda()[clave] -= 1

    def hay(self, esfera) -> bool:
        clave = esfera_desde_valor(esfera)
        return self._celda()[clave] > 0

    def cuantas(self, esfera) -> int:
        clave = esfera_desde_valor(esfera)
        return self._celda()[clave]

    def __str__(self) -> str:
        return f"GUERRERO (cabezal del tablero) en (x={self.x}, y={self.y})"

    # --------------------------------------------------------- render
    # --------------------------------------------------------- render
    def render(self) -> str:
        """Dibuja el tablero en ASCII dividiendo cada celda en una sub-grilla 2x2 (E1..E4)."""
        lineas = []
        lineas.append(
            f"  TABLERO {self.ancho}x{self.alto}   "
            f"Cabezal GUERRERO en (x={self.x}, y={self.y}) 🐉"
        )
        lineas.append(
            "  Sub-grilla 2x2 por celda = [E1 E2] / [E3 E4]  (E1=1★ E2=2★ E3=3★"
            " E4=4★)"
        )
        lineas.append("")

        borde_horizontal = "  +" + "-----+ " * self.ancho

        for y in range(self.alto - 1, -1, -1):  # De arriba hacia abajo
            lineas.append(borde_horizontal)

            # Línea superior de la celda: E1 (Arriba-Izq) y E2 (Arriba-Der)
            fila_superior = []
            # Línea inferior de la celda: E3 (Abajo-Izq) y E4 (Abajo-Der)
            fila_inferior = []

            for x in range(self.ancho):
                c = self.celdas[(x, y)]
                e1 = str(c[1]) if c[1] > 0 else " "
                e2 = str(c[2]) if c[2] > 0 else " "
                e3 = str(c[3]) if c[3] > 0 else " "
                e4 = str(c[4]) if c[4] > 0 else " "

                # Indicador de cabezal si el guerrero está en esta celda
                es_cabezal = x == self.x and y == self.y
                izq = ">" if es_cabezal else " "
                der = "<" if es_cabezal else " "

                fila_superior.append(f"{izq}{e1} {e2}{der}")
                fila_inferior.append(f"{izq}{e3} {e4}{der}")

            lineas.append(f"y{y} | " + " | ".join(fila_superior) + " |")
            lineas.append(f"   | " + " | ".join(fila_inferior) + " |")

        lineas.append(borde_horizontal)

        # Etiquetas de columnas (Eje X)
        etiquetas_x = "   " + " ".join(f"  x{x}  " for x in range(self.ancho))
        lineas.append(etiquetas_x)

        return "\n".join(lineas)
