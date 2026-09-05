"""
dragon_balls.py
===============
Sistemas de Esferas del Dragón.

Cada :class:`DragonBallSystem` describe un conjunto de esferas, el dragón que
invocan y cuántos deseos concede. Se usarán en la Fase 2 para la mecánica de
deseos.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DragonBallSystem:
    name: str
    ball_count: int
    dragon_name: str
    wish_count: int
    notes: str = ""

    def __str__(self) -> str:
        return (f"{self.name}: {self.ball_count} esferas, invoca a "
                f"{self.dragon_name} ({self.wish_count} deseo/s)")


EARTH_BALLS = DragonBallSystem(
    "Esferas de la Tierra", ball_count=7, dragon_name="Shenron", wish_count=1,
    notes="Creadas por Kami-sama / Dende")

NAMEK_BALLS = DragonBallSystem(
    "Esferas de Namek", ball_count=7, dragon_name="Porunga", wish_count=3,
    notes="Del tamaño de balones, creadas por el Gran Patriarca")

SUPER_DRAGON_BALLS = DragonBallSystem(
    "Super Esferas del Dragón", ball_count=7, dragon_name="Super Shenron",
    wish_count=1, notes="Del tamaño de planetas, un deseo ilimitado")


ALL_DRAGON_BALL_SYSTEMS = {
    "EARTH_BALLS": EARTH_BALLS,
    "NAMEK_BALLS": NAMEK_BALLS,
    "SUPER_DRAGON_BALLS": SUPER_DRAGON_BALLS,
}
