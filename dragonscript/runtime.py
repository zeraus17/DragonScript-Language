"""
runtime.py
==========
Runtime base de DragonScript: tipos internos y funciones built-in.

Aquí se definen:

* :class:`Technique` — representación en tiempo de ejecución de una función
  definida por el usuario (con su cierre / closure).
* :class:`BuiltinFunction` — envoltorio de funciones nativas de Python
  expuestas a DragonScript.
* :func:`ds_repr` — conversión de valores DragonScript a texto para SCOUTER.
* :func:`register_builtins` — registra las funciones matemáticas y utilidades
  básicas en el ámbito global.
"""

from __future__ import annotations

import math
import sys
from typing import Any, Callable

from . import board as board_mod
from .errors import ArgumentError, TypeErrorDS

# Intentamos importar TableroGUI; si estamos en el navegador (Pyodide), Tkinter no existe
try:
    from .gui_tablero import TableroGUI
    HAS_TKINTER = True
except ModuleNotFoundError:
    TableroGUI = None
    HAS_TKINTER = False

VERSION = "1.0.0"

# Variable de módulo para almacenar la instancia de la GUI
gui_instance: list = [None]


class ReturnSignal(Exception):
    """Señal interna usada para propagar el valor de un RETURN."""

    def __init__(self, value: Any):
        self.value = value
        super().__init__("return")


class Technique:
    """Función definida por el usuario con TECHNIQUE."""

    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure  # Environment donde se definió (closure)

    @property
    def name(self) -> str:
        return self.declaration.name

    @property
    def arity(self) -> int:
        return len(self.declaration.params)

    def __repr__(self) -> str:
        return f"<technique {self.name}({', '.join(self.declaration.params)})>"


class BuiltinFunction:
    """Función nativa de Python expuesta a DragonScript."""

    def __init__(self, name: str, fn: Callable[..., Any], arity: int | None = None):
        self.name = name
        self.fn = fn
        self.arity = arity  # None = número variable de argumentos

    def call(self, args: list[Any]):
        if self.arity is not None and len(args) != self.arity:
            raise ArgumentError(
                f"La función '{self.name}' esperaba {self.arity} argumento(s), "
                f"recibió {len(args)}."
            )
        return self.fn(*args)

    def __repr__(self) -> str:
        return f"<builtin {self.name}>"


def ds_repr(value: Any) -> str:
    """Convierte un valor DragonScript a su representación textual."""
    if value is None:
        return "NULL"
    if value is True:
        return "TRUE"
    if value is False:
        return "FALSE"
    if isinstance(value, float):
        # Mostramos 3.0 como 3 si es entero exacto.
        if value.is_integer():
            return str(int(value))
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(ds_repr(v) for v in value) + "]"
    return str(value)


def is_truthy(value: Any) -> bool:
    """Reglas de veracidad de DragonScript."""
    if value is None or value is False:
        return False
    if value == 0:
        return False
    if isinstance(value, str) and value == "":
        return False
    if isinstance(value, list) and len(value) == 0:
        return False
    return True


def register_builtins(global_env, output=None) -> None:
    """Registra las funciones built-in en el ámbito global dado.

    ``output`` es el flujo de salida (el mismo que usa SCOUTER) para que
    MOSTRAR_TABLERO se pueda capturar en los tests.
    """
    out = output if output is not None else sys.stdout

    def _num(x, fname):
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeErrorDS(f"'{fname}' requiere un número.")
        return x

    def _lista(x, fname):
        if not isinstance(x, list):
            raise TypeErrorDS(f"'{fname}' requiere un grupo (lista).")
        return x

    def _cabeza(lista):
        _lista(lista, "CABEZA")
        if not lista:
            raise TypeErrorDS("CABEZA no funciona con un grupo vacío.")
        return lista[0]

    def _cola(lista):
        _lista(lista, "COLA")
        if not lista:
            raise TypeErrorDS("COLA no funciona con un grupo vacío.")
        return lista[1:]

    def _rango(a, b):
        for v in (a, b):
            if isinstance(v, bool) or not isinstance(v, int):
                raise TypeErrorDS("RANGO requiere números enteros.")
        return list(range(a, b + 1))

    builtins = {
        # Matemáticas básicas
        "ABS": BuiltinFunction("ABS", lambda x: abs(_num(x, "ABS")), 1),
        "SQRT": BuiltinFunction("SQRT", lambda x: math.sqrt(_num(x, "SQRT")), 1),
        "POW": BuiltinFunction("POW", lambda x, y: math.pow(_num(x, "POW"), _num(y, "POW")), 2),
        "MAX": BuiltinFunction("MAX", lambda *xs: max(xs)),
        "MIN": BuiltinFunction("MIN", lambda *xs: min(xs)),
        "ROUND": BuiltinFunction("ROUND", lambda x: round(_num(x, "ROUND")), 1),
        "FLOOR": BuiltinFunction("FLOOR", lambda x: math.floor(_num(x, "FLOOR")), 1),
        "CEIL": BuiltinFunction("CEIL", lambda x: math.ceil(_num(x, "CEIL")), 1),
        # Utilidades
        "LEN": BuiltinFunction("LEN", lambda x: len(x), 1),
        "STR": BuiltinFunction("STR", lambda x: ds_repr(x), 1),
        "NUM": BuiltinFunction("NUM", lambda x: float(x) if not isinstance(x, bool) else x, 1),
        "INPUT": BuiltinFunction("INPUT", lambda prompt: input(ds_repr(prompt)), 1),
        # Manipulación de grupos (listas) — temáticas Dragon Ball
        "ABSORBER": BuiltinFunction(
            "ABSORBER", lambda lista, x: _lista(lista, "ABSORBER") + [x], 2
        ),
        "CABEZA": BuiltinFunction("CABEZA", _cabeza, 1),
        "COLA": BuiltinFunction("COLA", _cola, 1),
        "LONGITUD": BuiltinFunction("LONGITUD", lambda x: len(_lista(x, "LONGITUD")), 1),
        "ESTA_VACIA": BuiltinFunction(
            "ESTA_VACIA", lambda x: len(_lista(x, "ESTA_VACIA")) == 0, 1
        ),
        "RANGO": BuiltinFunction("RANGO", _rango, 2),
    }
    for name, fn in builtins.items():
        global_env.define(name, fn)

    # --------------------------------------------------------------
    # TABLERO estilo Gobstones (temática Dragon Ball)
    tablero = board_mod.Board()

    # --------------------------------------------------------------
    # TABLERO estilo Gobstones (temática Dragon Ball)
    tablero = board_mod.Board()

    def _actualizar_gui():
        # 1. Escritorio (Tkinter)
        if HAS_TKINTER and gui_instance[0] is not None:
            gui_instance[0].renderizar((tablero.x, tablero.y), tablero.celdas)

        # 2. Web (vía Pyodide / JS)
        try:
            import json
            import time

            try:
                import js  # type: ignore[import-not-found]
            except ImportError:
                return

            celdas_json = json.dumps({str(k): v for k, v in tablero.celdas.items()})
            js.actualizarTableroJS(tablero.ancho, tablero.alto, tablero.x, tablero.y, celdas_json)

            # Si estamos en la web, pausamos unos milisegundos para permitir que el navegador renderice el frame
            time.sleep(0.3)  # Pausa de 300ms entre movimiento/acción
        except Exception:
            pass

    def _iniciar(ancho, alto):
        tablero.reiniciar(ancho, alto)
        if HAS_TKINTER and TableroGUI is not None:
            gui_instance[0] = TableroGUI(ancho, alto)
        _actualizar_gui()
        return None

    def _volar(direccion):
        tablero.volar(direccion)
        _actualizar_gui()
        return None

    def _cargar(esfera):
        tablero.cargar(esfera)
        _actualizar_gui()
        return None

    def _drenar(esfera):
        tablero.drenar(esfera)
        _actualizar_gui()
        return None

    def _mostrar_tablero():
        out.write(tablero.render() + "\n")
        _actualizar_gui()
        return None

    board_builtins = {
        "INICIAR_TABLERO": BuiltinFunction("INICIAR_TABLERO", _iniciar, 2),
        "VOLAR": BuiltinFunction("VOLAR", _volar, 1),
        "PUEDE_VOLAR": BuiltinFunction("PUEDE_VOLAR", tablero.puede_volar, 1),
        "CARGAR": BuiltinFunction("CARGAR", _cargar, 1),
        "DRENAR": BuiltinFunction("DRENAR", _drenar, 1),
        "HAY": BuiltinFunction("HAY", tablero.hay, 1),
        "CUANTAS": BuiltinFunction("CUANTAS", tablero.cuantas, 1),
        "POSICION_X": BuiltinFunction("POSICION_X", lambda: tablero.x, 0),
        "POSICION_Y": BuiltinFunction("POSICION_Y", lambda: tablero.y, 0),
        "MOSTRAR_TABLERO": BuiltinFunction("MOSTRAR_TABLERO", _mostrar_tablero, 0),
    }
    for name, fn in board_builtins.items():
        global_env.define(name, fn)

    # Constantes del tablero (valores globales que se pueden usar sin comillas).
    global_env.define("NORTE", board_mod.NORTE)
    global_env.define("SUR", board_mod.SUR)
    global_env.define("ESTE", board_mod.ESTE)
    global_env.define("OESTE", board_mod.OESTE)
    for clave, nombre in board_mod.NOMBRE_ESFERA.items():
        global_env.define(nombre, nombre)  # ESFERA_1 == "ESFERA_1"
    # El GUERRERO es el cabezal: apunta al tablero mismo.
    global_env.define("GUERRERO", tablero)