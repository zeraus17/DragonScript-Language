"""
transformations.py
==================
Transformaciones del universo Dragon Ball.

Cada :class:`Transformation` describe un estado potenciado: su coste de Ki, el
multiplicador de poder que otorga y los requisitos para acceder a él. Los
multiplicadores son valores de balance del lenguaje (no cifras oficiales).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .races import Race


@dataclass
class Transformation:
    name: str
    ki_cost: int
    power_multiplier: float
    races: list[Race] = field(default_factory=list)
    requirements: str = ""

    def __str__(self) -> str:
        return f"{self.name} (x{self.power_multiplier})"


# --- Transformaciones Saiyan ---
SUPER_SAIYAN = Transformation(
    "Super Saiyan", ki_cost=1000, power_multiplier=50.0,
    races=[Race.SAIYAN], requirements="Ira intensa o entrenamiento extremo")

SUPER_SAIYAN_2 = Transformation(
    "Super Saiyan 2", ki_cost=2000, power_multiplier=100.0,
    races=[Race.SAIYAN], requirements="Dominar el Super Saiyan")

SUPER_SAIYAN_3 = Transformation(
    "Super Saiyan 3", ki_cost=4000, power_multiplier=400.0,
    races=[Race.SAIYAN], requirements="Enorme control de Ki")

SUPER_SAIYAN_GOD = Transformation(
    "Super Saiyan God", ki_cost=8000, power_multiplier=1000.0,
    races=[Race.SAIYAN], requirements="Ritual con 6 Saiyans de corazón puro")

SUPER_SAIYAN_BLUE = Transformation(
    "Super Saiyan Blue", ki_cost=10000, power_multiplier=2000.0,
    races=[Race.SAIYAN], requirements="Super Saiyan God + Super Saiyan")

ULTRA_INSTINCT_SIGN = Transformation(
    "Ultra Instinto (Signo)", ki_cost=15000, power_multiplier=4000.0,
    races=[Race.SAIYAN, Race.GOD], requirements="Separar mente y cuerpo")

ULTRA_INSTINCT = Transformation(
    "Ultra Instinto (Dominado)", ki_cost=25000, power_multiplier=8000.0,
    races=[Race.SAIYAN, Race.GOD], requirements="Dominar el Ultra Instinto")

GREAT_APE = Transformation(
    "Oozaru (Mono Gigante)", ki_cost=500, power_multiplier=10.0,
    races=[Race.SAIYAN], requirements="Cola de Saiyan y luna llena (Blutz)")

# --- Otras razas ---
GOLDEN_FRIEZA = Transformation(
    "Golden Freezer", ki_cost=9000, power_multiplier=1500.0,
    races=[Race.FRIEZA_RACE], requirements="Entrenamiento de la forma dorada")

PERFECT_CELL = Transformation(
    "Cell Perfecto", ki_cost=7000, power_multiplier=900.0,
    races=[Race.ANDROID], requirements="Absorber a los Androides 17 y 18")

SUPER_BUU = Transformation(
    "Super Buu", ki_cost=6000, power_multiplier=800.0,
    races=[Race.MAJIN], requirements="Absorción de guerreros poderosos")


# Registro accesible por nombre.
ALL_TRANSFORMATIONS = {
    "SUPER_SAIYAN": SUPER_SAIYAN,
    "SUPER_SAIYAN_2": SUPER_SAIYAN_2,
    "SUPER_SAIYAN_3": SUPER_SAIYAN_3,
    "SUPER_SAIYAN_GOD": SUPER_SAIYAN_GOD,
    "SUPER_SAIYAN_BLUE": SUPER_SAIYAN_BLUE,
    "ULTRA_INSTINCT_SIGN": ULTRA_INSTINCT_SIGN,
    "ULTRA_INSTINCT": ULTRA_INSTINCT,
    "GREAT_APE": GREAT_APE,
    "GOLDEN_FRIEZA": GOLDEN_FRIEZA,
    "PERFECT_CELL": PERFECT_CELL,
    "SUPER_BUU": SUPER_BUU,
}
