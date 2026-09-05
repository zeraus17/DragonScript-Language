"""
DragonScript
============
Un lenguaje de programación interpretado inspirado en el universo de
Dragon Ball, implementado en Python.

Flujo de ejecución::

    Código DragonScript -> Lexer -> Tokens -> Parser -> AST -> Interpreter

Uso rápido::

    from dragonscript import run_source
    run_source('SCOUTER "¡Hola, Guerrero!"')
"""

from __future__ import annotations

import io

from .lexer import Lexer, tokenize
from .parser import Parser, parse
from .interpreter import Interpreter, run
from .errors import DragonScriptError
from .runtime import VERSION

__version__ = VERSION
__all__ = [
    "Lexer", "tokenize", "Parser", "parse", "Interpreter", "run",
    "run_source", "run_source_capture", "DragonScriptError", "__version__",
]


def run_source(source: str, output=None) -> None:
    """Tokeniza, parsea e interpreta código fuente DragonScript."""
    tokens = tokenize(source)
    program = parse(tokens)
    Interpreter(output=output).interpret(program)


def run_source_capture(source: str) -> str:
    """Ejecuta código y devuelve todo lo que SCOUTER imprimió como cadena."""
    buffer = io.StringIO()
    run_source(source, output=buffer)
    return buffer.getvalue()
