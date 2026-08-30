"""
dragonball
==========
Capa temática de DragonScript: estructuras de datos del universo Dragon Ball
(personajes, transformaciones, técnicas, razas, esferas del dragón, fusiones y
universos).

En la Fase 1 son datos preparados para su uso; en la Fase 2 se integrarán con
el runtime del lenguaje para habilitar mecánicas de combate, transformaciones
y deseos.
"""

from __future__ import annotations

from .races import Race
from .characters import Warrior, ALL_CHARACTERS
from .transformations import Transformation, ALL_TRANSFORMATIONS
from .techniques import Technique, ALL_TECHNIQUES
from .dragon_balls import DragonBallSystem, ALL_DRAGON_BALL_SYSTEMS
from .fusions import Fusion, FusionMethod, ALL_FUSIONS
from .universes import Universe, ALL_UNIVERSES

__all__ = [
    "Race",
    "Warrior", "ALL_CHARACTERS",
    "Transformation", "ALL_TRANSFORMATIONS",
    "Technique", "ALL_TECHNIQUES",
    "DragonBallSystem", "ALL_DRAGON_BALL_SYSTEMS",
    "Fusion", "FusionMethod", "ALL_FUSIONS",
    "Universe", "ALL_UNIVERSES",
]
