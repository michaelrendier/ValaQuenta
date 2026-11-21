"""
bao_mass_gap: DEPRECATED name, kept for one release.

The engine was renamed ``inductive_onset_residual`` on 2026-11-21: no BAO data, scale or measurement
enters its residual. This shim re-exports the constants and :func:`validate` from the new module.
Use ``from ValaQuenta.modules.inductive_onset_residual import maths``.
"""
import math
import warnings

from .modules.inductive_onset_residual import maths as _m

warnings.warn("ValaQuenta.bao_mass_gap is renamed ValaQuenta.modules.inductive_onset_residual", DeprecationWarning, stacklevel=2)

OMEGA_ZS = _m.OMEGA_ZS
D_STAR = _m.D_STAR_RUN
LN10 = _m.LN10
GAP = OMEGA_ZS - D_STAR * LN10


def validate() -> dict:
    """The new module's checks.

    :returns: the check results of ``inductive_onset_residual.maths.validate``
    """
    return _m.validate()
