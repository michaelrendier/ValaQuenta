"""
ainulindale_engine.modules.translator_vsa
===========================================
The Translator, version 2 of 2 — VSA / hyperdimensional computing
(bind, bundle, permute). See translator_discocat for version 1, and
translator_common for the shared substrate that lets the two be combined.

Version: 0.111
"""

from .tools import VSATranslatorModule
from .maths import (
    permute, bind, bundle, role_vector, ROLE_NAMES,
    fold_to_channels, VSATranslator,
    verify_vsa_identities, capacity_probe, unbind_probe,
)
