"""
objects.py
==========
Tipos del runtime para la Programación Orientada a Objetos (POO) de DragonScript.

En DragonScript, las *clases* se declaran con ``WARRIOR`` (un guerrero es un
molde del que salen combatientes concretos) y las *instancias* se crean con
``CREATE``. La herencia se expresa con ``EVOLVES`` (un guerrero evoluciona a
partir de otro), soportando herencia múltiple mediante linealización C3
(el mismo algoritmo de MRO que usa Python).

Este módulo define:

* :class:`DSClass`    — una clase de DragonScript.
* :class:`DSInstance` — una instancia (objeto) de una clase.
* :class:`BoundMethod` — un método ligado a una instancia (lleva su ``SELF``).
* :func:`c3_linearize` — orden de resolución de métodos (MRO) para herencia.

La convención de encapsulación es sencilla y predecible: los miembros cuyo
nombre empieza por ``_`` se consideran **privados** y solo pueden accederse
desde dentro de la propia clase mediante ``SELF``.
"""

from __future__ import annotations

from typing import Any, Optional


# Mapa de operador -> nombre del método mágico para sobrecarga de operadores.
OPERATOR_DUNDERS = {
    "+": "__add__",
    "-": "__sub__",
    "*": "__mul__",
    "/": "__div__",
    "%": "__mod__",
    "==": "__eq__",
    "!=": "__neq__",
    "<": "__lt__",
    ">": "__gt__",
    "<=": "__lte__",
    ">=": "__gte__",
}


def c3_linearize(cls: "DSClass") -> list["DSClass"]:
    """Calcula el MRO (Method Resolution Order) mediante linealización C3.

    Es el mismo algoritmo que utiliza Python para resolver la herencia
    múltiple de forma consistente y determinista.
    """

    def merge(sequences: list[list["DSClass"]]) -> list["DSClass"]:
        result: list["DSClass"] = []
        sequences = [list(seq) for seq in sequences if seq]
        while sequences:
            head = None
            for seq in sequences:
                candidate = seq[0]
                # Un candidato es válido si no aparece en la "cola" de
                # ninguna otra secuencia.
                if not any(candidate in s[1:] for s in sequences):
                    head = candidate
                    break
            if head is None:
                raise ValueError(
                    "¡Fusión imposible de linaje! No se puede resolver el "
                    "orden de herencia (MRO inconsistente).")
            result.append(head)
            new_sequences = []
            for s in sequences:
                filtered = [c for c in s if c is not head]
                if filtered:
                    new_sequences.append(filtered)
            sequences = new_sequences
        return result

    parent_linearizations = [c3_linearize(p) for p in cls.parents]
    return [cls] + merge(parent_linearizations + [list(cls.parents)])


class DSClass:
    """Representa una clase (``WARRIOR``) de DragonScript."""

    def __init__(self, name: str, parents: list["DSClass"],
                 methods: dict, static_methods: dict, class_attributes: dict):
        self.name = name
        self.parents = parents
        self.methods = methods                # nombre -> Technique (instancia)
        self.static_methods = static_methods  # nombre -> Technique (estático)
        self.class_attributes = class_attributes  # nombre -> valor (compartido)
        # Orden de resolución de métodos (incluye a la propia clase).
        self.mro = c3_linearize(self)

    # --------------------------------------------------------- resolución
    def find_method(self, name: str) -> Optional[Any]:
        """Busca un método de instancia recorriendo el MRO."""
        for klass in self.mro:
            if name in klass.methods:
                return klass.methods[name]
        return None

    def find_static(self, name: str) -> Optional[Any]:
        """Busca un método estático recorriendo el MRO."""
        for klass in self.mro:
            if name in klass.static_methods:
                return klass.static_methods[name]
        return None

    def find_class_attr(self, name: str):
        """Busca un atributo de clase recorriendo el MRO.

        Devuelve una tupla ``(encontrado, valor)`` para poder distinguir un
        atributo con valor ``NULL`` de la ausencia del atributo.
        """
        for klass in self.mro:
            if name in klass.class_attributes:
                return True, klass.class_attributes[name]
        return False, None

    def set_class_attr(self, name: str, value: Any) -> bool:
        """Asigna un atributo de clase ya existente en el MRO. Devuelve
        ``True`` si se encontró y actualizó."""
        for klass in self.mro:
            if name in klass.class_attributes:
                klass.class_attributes[name] = value
                return True
        return False

    def __repr__(self) -> str:
        return f"<warrior {self.name}>"

    def __str__(self) -> str:
        return f"<warrior {self.name}>"


class DSInstance:
    """Representa una instancia (objeto) de una clase de DragonScript."""

    def __init__(self, klass: DSClass):
        self.klass = klass
        self.fields: dict[str, Any] = {}

    def __repr__(self) -> str:
        return self._default_str()

    def __str__(self) -> str:
        return self._default_str()

    def _default_str(self) -> str:
        # Representación por defecto cuando la clase no define __str__.
        if self.fields:
            campos = ", ".join(f"{k}={v}" for k, v in self.fields.items()
                               if not k.startswith("_"))
            return f"<{self.klass.name} {campos}>" if campos else f"<{self.klass.name}>"
        return f"<{self.klass.name}>"


class BoundMethod:
    """Un método de instancia ligado a su objeto (transporta ``SELF``)."""

    __slots__ = ("instance", "technique")

    def __init__(self, instance: DSInstance, technique: Any):
        self.instance = instance
        self.technique = technique

    @property
    def name(self) -> str:
        return self.technique.name

    def __repr__(self) -> str:
        return f"<bound method {self.technique.name} of {self.instance.klass.name}>"


class UnboundMethod:
    """Un método de instancia accedido a través de la clase (no ligado).

    Permite llamadas explícitas al método de una clase padre pasando la
    instancia como primer argumento, al estilo ``Padre.__init__(SELF, ...)``.
    """

    __slots__ = ("klass", "technique")

    def __init__(self, klass: DSClass, technique: Any):
        self.klass = klass
        self.technique = technique

    @property
    def name(self) -> str:
        return self.technique.name

    def __repr__(self) -> str:
        return f"<unbound method {self.technique.name} of {self.klass.name}>"
