"""
errors.py
=========
Excepciones temáticas de DragonScript.

Todos los errores del lenguaje (léxicos, sintácticos y de ejecución) heredan
de :class:`DragonScriptError` y muestran mensajes inspirados en Dragon Ball.
"""

from __future__ import annotations


class DragonScriptError(Exception):
    """Clase base para todos los errores de DragonScript."""

    def __init__(self, message: str, line: int | None = None,
                 column: int | None = None):
        self.raw_message = message
        self.line = line
        self.column = column
        super().__init__(self._format())

    def _format(self) -> str:
        if self.line is not None:
            return f"{self.message_prefix} {self.raw_message} en línea {self.line}"
        return f"{self.message_prefix} {self.raw_message}"

    @property
    def message_prefix(self) -> str:
        return "¡Error de DragonScript!"


class LexerError(DragonScriptError):
    """Error durante la tokenización (el Scouter explota)."""

    @property
    def message_prefix(self) -> str:
        return "¡El Scouter explotó!"


class ParserError(DragonScriptError):
    """Error de sintaxis (Ki sintáctico inestable)."""

    @property
    def message_prefix(self) -> str:
        return "¡Error de Ki Sintáctico!"


class RuntimeError_(DragonScriptError):
    """Error genérico en tiempo de ejecución."""

    @property
    def message_prefix(self) -> str:
        return "¡Error de combate!"


class UndefinedVariableError(RuntimeError_):
    """Se referencia una variable que no existe."""

    def __init__(self, name: str, line: int | None = None):
        super().__init__(f"El Scouter no detecta '{name}'! Variable no definida.",
                         line)

    @property
    def message_prefix(self) -> str:
        return "¡Alerta!"


class DivisionByZeroError(RuntimeError_):
    """División entre cero."""

    def __init__(self, line: int | None = None):
        super().__init__("Ni Vegeta divide entre cero.", line)

    @property
    def message_prefix(self) -> str:
        return "¡Imposible!"


class TypeErrorDS(RuntimeError_):
    """Operación entre tipos incompatibles."""

    @property
    def message_prefix(self) -> str:
        return "¡Error de transformación de tipo!"


class StackOverflowError_(RuntimeError_):
    """Demasiada recursión."""

    def __init__(self, line: int | None = None):
        super().__init__("Stack overflow: recursión infinita.", line)

    @property
    def message_prefix(self) -> str:
        return "¡El poder es demasiado!"


class ArgumentError(RuntimeError_):
    """Número de argumentos incorrecto en una técnica."""

    def __init__(self, detail: str = "Número de argumentos incorrecto.",
                 line: int | None = None):
        super().__init__(detail, line)

    @property
    def message_prefix(self) -> str:
        return "¡Técnica fallida!"
