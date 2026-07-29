"""
ainulindale_engine.modules.translator_discocat
================================================
The Translator, version 1 of 2 — DisCoCat (pregroup grammar + tensor
contraction). See translator_vsa for version 2, and translator_common for
the shared substrate that lets the two be combined.

Version: 0.111
"""

from .tools import DisCoCatTranslatorModule
from .maths import (
    PregroupType, N, S, TRANSITIVE_VERB,
    reduce_type, is_grammatical, MeaningSpace, DisCoCatTranslator,
    verify_reduction_algebra, word_order_sensitivity,
)
