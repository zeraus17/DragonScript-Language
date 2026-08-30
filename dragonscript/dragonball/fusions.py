"""
fusions.py
==========
Fusiones del universo Dragon Ball.

Define los métodos de fusión (:class:`FusionMethod`) y la representación de una
fusión concreta (:class:`Fusion`). Se usarán en la Fase 2 para combinar
guerreros.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class FusionMethod(Enum):
    FUSION_DANCE = "Danza de la Fusión"
    POTARA = "Pendientes Potara"

    def __str__(self) -> str:
        return self.value


@dataclass
class Fusion:
    participants: list[str]
    method: FusionMethod
    result_name: str
    duration: str = ""  # p. ej. "30 minutos" para la Danza

    def __str__(self) -> str:
        quienes = " + ".join(self.participants)
        return f"{quienes} => {self.result_name} ({self.method})"


# Fusiones canónicas de ejemplo.
GOTENKS = Fusion(["Goten", "Trunks"], FusionMethod.FUSION_DANCE, "Gotenks",
                 duration="30 minutos")

GOGETA = Fusion(["Goku", "Vegeta"], FusionMethod.FUSION_DANCE, "Gogeta",
                duration="30 minutos")

VEGITO = Fusion(["Goku", "Vegeta"], FusionMethod.POTARA, "Vegito",
                duration="permanente (mortales: 1 hora)")


ALL_FUSIONS = {
    "GOTENKS": GOTENKS,
    "GOGETA": GOGETA,
    "VEGITO": VEGITO,
}
