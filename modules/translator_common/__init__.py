"""
ainulindale_engine.modules.translator_common
==============================================
The Translator — shared substrate for both Translator versions.

NOT a registered engine: no tools.py, no EquationModule, absent from the
registry by design. Provides the derived vector space, the prime-channel
encoder, the TranslatorEngine interface and the combination harness that
translator_discocat and translator_vsa share.

Version: 0.111
"""

from .maths import (
    PRIME_CHANNELS, N_CHANNELS, N_HARMONICS, D_HYPER,
    channel_signature, hypervector, verify_harmonic_reduction,
    dot, norm, cosine,
    TranslatorEngine, compare_engines,
)
