"""
environment.py
==============
Sistema de entornos (scopes) anidados de DragonScript.

Un :class:`Environment` almacena los enlaces nombre -> valor de un ámbito. Los
ámbitos se encadenan mediante ``parent``: el ámbito global no tiene padre y cada
llamada a una técnica crea un ámbito local cuyo padre es el ámbito donde se
definió la técnica (closures básicos).
"""

from __future__ import annotations

from typing import Any, Optional

from .errors import UndefinedVariableError


class Environment:
    def __init__(self, parent: Optional["Environment"] = None):
        self.parent = parent
        self.values: dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        """Define (o redefine) una variable en ESTE ámbito."""
        self.values[name] = value

    def get(self, name: str, line: int | None = None) -> Any:
        """Busca una variable subiendo por la cadena de ámbitos."""
        env: Optional[Environment] = self
        while env is not None:
            if name in env.values:
                return env.values[name]
            env = env.parent
        raise UndefinedVariableError(name, line)

    def assign(self, name: str, value: Any, line: int | None = None) -> None:
        """Reasigna una variable existente en la cadena de ámbitos."""
        env: Optional[Environment] = self
        while env is not None:
            if name in env.values:
                env.values[name] = value
                return
            env = env.parent
        raise UndefinedVariableError(name, line)

    def exists(self, name: str) -> bool:
        env: Optional[Environment] = self
        while env is not None:
            if name in env.values:
                return True
            env = env.parent
        return False
