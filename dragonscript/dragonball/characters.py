"""
characters.py
=============
Personajes (guerreros) del universo Dragon Ball.

La clase :class:`Warrior` modela a un combatiente con sus estadísticas. Se
incluyen instancias predefinidas de personajes canónicos que se usarán como
datos del runtime a partir de la Fase 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .races import Race


@dataclass
class Warrior:
    name: str
    race: Race
    ki: int
    max_ki: int
    health: int = 100
    stamina: int = 100
    power: int = 0
    speed: int = 0
    defense: int = 0
    transformation: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.name} [{self.race}] - Poder: {self.power}, Ki: {self.ki}/{self.max_ki}"


# --- Personajes canónicos predefinidos ---
GOKU = Warrior("Goku", Race.SAIYAN, ki=9000, max_ki=15000,
               health=150, stamina=150, power=9000, speed=95, defense=85)

VEGETA = Warrior("Vegeta", Race.SAIYAN, ki=8500, max_ki=14000,
                 health=140, stamina=140, power=8500, speed=92, defense=82)

PICCOLO = Warrior("Piccolo", Race.NAMEKIAN, ki=5000, max_ki=8000,
                  health=130, stamina=120, power=5000, speed=80, defense=88)

KRILLIN = Warrior("Krillin", Race.HUMAN, ki=3000, max_ki=4000,
                  health=100, stamina=100, power=3000, speed=78, defense=70)

GOHAN = Warrior("Gohan", Race.SAIYAN, ki=7000, max_ki=20000,
                health=135, stamina=130, power=7000, speed=90, defense=80)

FRIEZA = Warrior("Freezer", Race.FRIEZA_RACE, ki=12000, max_ki=18000,
                 health=160, stamina=150, power=12000, speed=90, defense=90)

CELL = Warrior("Cell", Race.ANDROID, ki=11000, max_ki=16000,
               health=155, stamina=200, power=11000, speed=88, defense=92)

BUU = Warrior("Majin Buu", Race.MAJIN, ki=10000, max_ki=17000,
              health=300, stamina=250, power=10000, speed=75, defense=95)

BEERUS = Warrior("Bills (Beerus)", Race.GOD, ki=50000, max_ki=60000,
                 health=400, stamina=350, power=50000, speed=99, defense=99)

WHIS = Warrior("Whis", Race.ANGEL, ki=60000, max_ki=70000,
               health=450, stamina=400, power=60000, speed=100, defense=100)


ALL_CHARACTERS = {
    "GOKU": GOKU,
    "VEGETA": VEGETA,
    "PICCOLO": PICCOLO,
    "KRILLIN": KRILLIN,
    "GOHAN": GOHAN,
    "FRIEZA": FRIEZA,
    "CELL": CELL,
    "BUU": BUU,
    "BEERUS": BEERUS,
    "WHIS": WHIS,
}
