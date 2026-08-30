"""
techniques.py
=============
Técnicas (ataques y habilidades) del universo Dragon Ball.

Cada :class:`Technique` describe un ataque: qué razas pueden usarlo, su coste de
Ki, el multiplicador de daño y efectos especiales. Se utilizarán en la Fase 2
para el sistema de combate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .races import Race


@dataclass
class Technique:
    name: str
    user_races: list[Race] = field(default_factory=list)
    ki_cost: int = 0
    damage_multiplier: float = 1.0
    effects: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.name} (x{self.damage_multiplier}, {self.ki_cost} Ki)"


KAMEHAMEHA = Technique(
    "Kamehameha", [Race.HUMAN, Race.SAIYAN], ki_cost=500, damage_multiplier=3.0,
    effects=["onda de energía", "carga concentrada"])

FINAL_FLASH = Technique(
    "Final Flash", [Race.SAIYAN], ki_cost=1200, damage_multiplier=5.0,
    effects=["gran área", "tiempo de carga"])

GALICK_GUN = Technique(
    "Galick Gun", [Race.SAIYAN], ki_cost=600, damage_multiplier=3.2,
    effects=["rayo púrpura"])

SPECIAL_BEAM_CANNON = Technique(
    "Makankosappo (Cañón Especial)", [Race.NAMEKIAN], ki_cost=700,
    damage_multiplier=4.0, effects=["perforante", "espiral"])

DESTRUCTO_DISC = Technique(
    "Kienzan (Disco Destructor)", [Race.HUMAN], ki_cost=400,
    damage_multiplier=6.0, effects=["cortante", "corte limpio"])

GENKI_DAMA = Technique(
    "Genki Dama (Bomba Espiritual)", [Race.HUMAN, Race.SAIYAN], ki_cost=2000,
    damage_multiplier=10.0, effects=["energía prestada", "muy poderosa"])

HAKAI = Technique(
    "Hakai (Destrucción)", [Race.GOD], ki_cost=5000, damage_multiplier=99.0,
    effects=["borra de la existencia"])

INSTANT_TRANSMISSION = Technique(
    "Teletransportación", [Race.SAIYAN, Race.HUMAN], ki_cost=100,
    damage_multiplier=0.0, effects=["movilidad", "rastreo de Ki"])

MAFUBA = Technique(
    "Mafuba (Onda del Encierro Demoníaco)", [Race.HUMAN], ki_cost=1500,
    damage_multiplier=0.0, effects=["sella al enemigo", "riesgo vital"])

SPIRIT_BOMB = GENKI_DAMA  # alias


ALL_TECHNIQUES = {
    "KAMEHAMEHA": KAMEHAMEHA,
    "FINAL_FLASH": FINAL_FLASH,
    "GALICK_GUN": GALICK_GUN,
    "SPECIAL_BEAM_CANNON": SPECIAL_BEAM_CANNON,
    "DESTRUCTO_DISC": DESTRUCTO_DISC,
    "GENKI_DAMA": GENKI_DAMA,
    "HAKAI": HAKAI,
    "INSTANT_TRANSMISSION": INSTANT_TRANSMISSION,
    "MAFUBA": MAFUBA,
}
