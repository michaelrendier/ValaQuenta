"""
ValaQuenta.modules.witches_hat
==============================
THE WITCH'S HAT ENGINE (core): static snapshots of the virtual brim, the hat potential and the paths of action, adjustable by size and
shape; focus, aim and defocus; the exchange-hole (fermion) and bunching (boson) waveforms; the zeta pair correlation.  Plain data out,
no rendering: renderers (the spatial-simulation skill) bridge from the snapshot.

Version: 0.1
"""
from .tools import WitchesHatModule
from .maths import (sm_hat, pair_correlation, hat_shape, quartic_family, turning_radius, trace, snapshot, focus_resolution,
                    defocus_curve, energy_regimes, unfold, zeta_pair_correlation, shape_table, verify)

__all__ = ["WitchesHatModule"]
