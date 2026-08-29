"""
ainulindale_engine.modules.add_scale_sign
=========================================
THE ADD:SCALE:SIGN DATATYPE — a value type for the tier-0 floor
Aff(1,ℝ) = ADD ⋊ (SCALE × SIGN), with its own manipulation surface
(compose / invert / residual / decompose), its own decomposition type
(`ASSWord`), an orthogonal-Smith-chart read-out in the maths language it
was built on, two lineage orderings (chrono / zeta), and the firing order
recorded (the three-phase camshaft; `[SCALE, ADD] = ADD`).

Canonical decomposition maths (four-question test, roll-down, AFF1
metadata): VAPMIP/add_scale_sign.py — NOT duplicated here.

Version: 0.1
"""
from .maths import (
    ASS, ASSWord,
    IDENTITIES, BRACKET, CAMSHAFT,
    compose, from_map, word, ground,
)
from .tools import AddScaleSignModule

__all__ = [
    "ASS", "ASSWord",
    "IDENTITIES", "BRACKET", "CAMSHAFT",
    "compose", "from_map", "word", "ground",
    "AddScaleSignModule",
]
