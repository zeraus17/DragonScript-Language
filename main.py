#!/usr/bin/env python3
"""
main.py
=======
Punto de entrada de DragonScript.

Uso::

    python main.py programa.ds        # ejecuta un archivo .ds
    python main.py --repl             # modo interactivo (REPL)
    python main.py --version          # muestra la versión
    python main.py --help             # muestra esta ayuda
"""

from __future__ import annotations

import sys

from dragonscript import __version__, tokenize, parse
from dragonscript.interpreter import Interpreter
from dragonscript.errors import DragonScriptError


BANNER = r"""
   ____                              ____            _       _
  |  _ \ _ __ __ _  __ _  ___  _ __ / ___|  ___ _ __(_)_ __ | |_
  | | | | '__/ _` |/ _` |/ _ \| '_ \\___ \ / __| '__| | '_ \| __|
  | |_| | | | (_| | (_| | (_) | | | |___) | (__| |  | | |_) | |_
  |____/|_|  \__,_|\__, |\___/|_| |_|____/ \___|_|  |_| .__/ \__|
                   |___/                              |_|
"""

HELP_TEXT = """DragonScript — un lenguaje inspirado en Dragon Ball 🐉

Uso:
  python main.py <archivo.ds>   Ejecuta un programa DragonScript
  python main.py --repl         Inicia el modo interactivo (REPL)
  python main.py --version      Muestra la versión
  python main.py --help         Muestra esta ayuda
"""


def run_file(path: str) -> int:
    """Ejecuta un archivo .ds. Devuelve el código de salida del proceso."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"¡El Scouter no encuentra el archivo '{path}'!", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Error al leer '{path}': {exc}", file=sys.stderr)
        return 2

    try:
        tokens = tokenize(source)
        program = parse(tokens)
        Interpreter().interpret(program)
        return 0
    except DragonScriptError as exc:
        print(str(exc), file=sys.stderr)
        return 1


def repl() -> int:
    """Modo interactivo básico. Cada línea se ejecuta en un mismo intérprete."""
    print(BANNER)
    print(f"DragonScript {__version__} — REPL interactivo")
    print('Escribe código DragonScript. Usa "salir" o Ctrl+D para terminar.\n')

    interpreter = Interpreter()
    buffer: list[str] = []

    while True:
        try:
            prompt = "... " if buffer else ">>> "
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\n¡Hasta la próxima, guerrero!")
            return 0

        if not buffer and line.strip() in ("salir", "exit", "quit"):
            print("¡Hasta la próxima, guerrero!")
            return 0

        buffer.append(line)

        # Ejecutamos cuando las llaves están balanceadas.
        joined = "\n".join(buffer)
        if joined.count("{") > joined.count("}"):
            continue

        buffer = []
        if not joined.strip():
            continue

        try:
            tokens = tokenize(joined)
            program = parse(tokens)
            interpreter.interpret(program)
        except DragonScriptError as exc:
            print(str(exc), file=sys.stderr)
        except Exception as exc:  # pragma: no cover - salvaguarda del REPL
            print(f"Error inesperado: {exc}", file=sys.stderr)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(HELP_TEXT)
        return 0

    arg = argv[1]
    if arg in ("--version", "-v"):
        print(f"DragonScript {__version__}")
        return 0
    if arg in ("--help", "-h"):
        print(HELP_TEXT)
        return 0
    if arg == "--repl":
        return repl()

    return run_file(arg)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
