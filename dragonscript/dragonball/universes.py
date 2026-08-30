"""
universes.py
============
Los 12 universos de Dragon Ball Super.

Cada :class:`Universe` recoge los datos conocidos del material oficial: su
número, su Dios de la Destrucción, su Ángel, su Kaio-Shin (Supremo Kai) y el
nivel mortal medido antes del Torneo del Poder.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Universe:
    number: int
    name: str
    god_of_destruction: str
    angel: str
    supreme_kai: str
    mortal_level: Optional[float] = None

    def __str__(self) -> str:
        return f"Universo {self.number} ({self.name}) - Hakaishin: {self.god_of_destruction}"


ALL_UNIVERSES = {
    1: Universe(1, "Sin nombre", "Iwne", "Awamo", "Kai del Universo 1", 7.03),
    2: Universe(2, "Sin nombre", "Helles (Jerez)", "Sour (Vados menor)",
                "Pell", 6.23),
    3: Universe(3, "Sin nombre", "Mosco (Mule)", "Camparri", "Ea", 6.42),
    4: Universe(4, "Sin nombre", "Quitela", "Cognac", "Kuru", 5.5),
    5: Universe(5, "Sin nombre", "Arak", "Cukatail", "Ogma", None),
    6: Universe(6, "Universo Hermano", "Champa", "Vados", "Fuwa", 3.18),
    7: Universe(7, "Universo de Goku", "Bills (Beerus)", "Whis", "Shin", 3.18),
    8: Universe(8, "Sin nombre", "Liquiir", "Korn", "Ill", None),
    9: Universe(9, "Sin nombre", "Sidra", "Mojito", "Roh", 1.86),
    10: Universe(10, "Sin nombre", "Rumsshi", "Kusu", "Gowasu", 2.62),
    11: Universe(11, "Universo de la Justicia", "Vermoud", "Marcarita",
                 "Kai del Universo 11", 5.5),
    12: Universe(12, "Sin nombre", "Geene", "Martinu", "Agu", 6.85),
}
