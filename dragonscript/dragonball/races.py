"""
races.py
========
Razas del universo Dragon Ball.

Estas estructuras se usarán a partir de la Fase 2 para dar semántica a los
personajes (qué transformaciones y técnicas puede usar cada raza).
"""

from __future__ import annotations

from enum import Enum


class Race(Enum):
    """Razas disponibles en DragonScript."""

    SAIYAN = "Saiyan"
    NAMEKIAN = "Namekiano"
    HUMAN = "Humano"
    FRIEZA_RACE = "Raza de Freezer"
    ANDROID = "Androide"
    MAJIN = "Majin"
    GOD = "Dios"
    ANGEL = "Ángel"
    UNKNOWN = "Desconocida"

    def __str__(self) -> str:
        return self.value
